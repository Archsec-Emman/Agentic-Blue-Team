from typing import Annotated, List, Any

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, StateGraph, add_messages
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel, Field, ConfigDict

from Lib.api import get_current_time_str
from Lib.baseplaybook import LanggraphPlaybook
from PLUGINS.LLM.llmapi import LLMAPI

AGENT_NODE_SUMMARIZE = "SUMMARIZE"
AGENT_NODE_REPORT = "REPORT"
MAX_EVIDENCE_CHARS = 120000

_graph_agent_instance = None


def get_report_graph() -> CompiledStateGraph:
    global _graph_agent_instance
    if _graph_agent_instance is None:
        _graph_agent_instance = GraphAgentReport()
    return _graph_agent_instance.graph


def _normalize_content(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    return str(content)


def _build_evidence_entries(messages: List[Any]) -> List[dict]:
    entries = []
    for idx, message in enumerate(messages, 1):
        role = getattr(message, "type", message.__class__.__name__)
        content = _normalize_content(getattr(message, "content", ""))
        tool_calls = getattr(message, "tool_calls", None)
        if tool_calls:
            content = f"{content}\n\nTool calls: {tool_calls}"
        entries.append({"id": f"E{idx}", "role": role, "content": content})
    return entries


def _build_evidence_text(entries: List[dict]) -> str:
    lines = []
    for entry in entries:
        lines.append(f"{entry['id']} | role={entry['role']} | {entry['content']}")
    return "\n\n".join(lines)


def _build_citations(entries: List[dict]) -> List[dict]:
    citations = []
    for entry in entries:
        excerpt = entry["content"].replace("\n", " ").strip()
        if len(excerpt) > 500:
            excerpt = excerpt[:500] + "..."
        citations.append({"id": entry["id"], "role": entry["role"], "excerpt": excerpt})
    return citations


def _split_entries(entries: List[dict], max_chars: int) -> List[List[dict]]:
    chunks = []
    current = []
    current_len = 0
    for entry in entries:
        entry_text = f"{entry['id']} | role={entry['role']} | {entry['content']}"
        entry_len = len(entry_text) + 2
        if current and current_len + entry_len > max_chars:
            chunks.append(current)
            current = []
            current_len = 0
        current.append(entry)
        current_len += entry_len
    if current:
        chunks.append(current)
    return chunks


class AgentState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    messages: Annotated[List[Any], add_messages] = Field(default_factory=list)
    summary_digest: str = Field(default="")
    report_markdown: str = Field(default="")
    citations: List[dict] = Field(default_factory=list)


class GraphAgentReport(LanggraphPlaybook):
    def __init__(self):
        super().__init__()
        self._summary_prompt_template = self.load_system_prompt_template("summary")
        self._summary_merge_prompt_template = self.load_system_prompt_template("summary_merge")
        self._report_prompt_template = self.load_system_prompt_template("system")
        self._llm_api = LLMAPI()
        self._llm_base = self._llm_api.get_model(tag=["powerful"])
        self.graph = self._build_graph()

    def _build_graph(self) -> CompiledStateGraph:
        def summarize_node(state: AgentState):
            entries = _build_evidence_entries(state.messages)
            citations = _build_citations(entries)
            evidence_text = _build_evidence_text(entries)
            if len(evidence_text) <= MAX_EVIDENCE_CHARS:
                system_message = self._summary_prompt_template.format(
                    CURRENT_UTC_TIME=get_current_time_str(),
                    REPORT_LANGUAGE="English"
                )
                human_message = HumanMessage(content=evidence_text)
                response: AIMessage = self._llm_base.invoke([system_message, human_message])
                return {"summary_digest": response.content, "citations": citations}
            chunks = _split_entries(entries, MAX_EVIDENCE_CHARS)
            partials = []
            for chunk in chunks:
                chunk_text = _build_evidence_text(chunk)
                system_message = self._summary_prompt_template.format(
                    CURRENT_UTC_TIME=get_current_time_str(),
                    REPORT_LANGUAGE="English"
                )
                human_message = HumanMessage(content=f"PARTIAL_DIGEST: true\n\n{chunk_text}")
                response: AIMessage = self._llm_base.invoke([system_message, human_message])
                partials.append(response.content)
            merge_system_message = self._summary_merge_prompt_template.format(
                CURRENT_UTC_TIME=get_current_time_str(),
                REPORT_LANGUAGE="English"
            )
            merge_human_message = HumanMessage(content="\n\n".join(partials))
            merged: AIMessage = self._llm_base.invoke([merge_system_message, merge_human_message])
            return {"summary_digest": merged.content, "citations": citations}

        def report_node(state: AgentState):
            system_message = self._report_prompt_template.format(
                CURRENT_UTC_TIME=get_current_time_str(),
                REPORT_LANGUAGE="English"
            )
            human_message = HumanMessage(content=state.summary_digest)
            response: AIMessage = self._llm_base.invoke([system_message, human_message])
            return {
                "messages": [response],
                "report_markdown": response.content
            }

        workflow = StateGraph(AgentState)
        workflow.add_node(AGENT_NODE_SUMMARIZE, summarize_node)
        workflow.add_node(AGENT_NODE_REPORT, report_node)
        workflow.set_entry_point(AGENT_NODE_SUMMARIZE)
        workflow.add_edge(AGENT_NODE_SUMMARIZE, AGENT_NODE_REPORT)
        workflow.add_edge(AGENT_NODE_REPORT, END)
        return workflow.compile()
