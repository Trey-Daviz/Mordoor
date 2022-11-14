import Access as a


class AdminUser(a.Access):
    def __init__(self, user):
        self._user = user

    def remove_user(self, sys_obj):
        return True