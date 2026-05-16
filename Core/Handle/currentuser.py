class CurrentUser(object):
    def __init__(self):
        pass

    @staticmethod
    def list(user=None):
        current_info = {
            'name': user.username,
            'currentAuthority': 'admin',
            'userid': user.id,
        }

        return current_info
