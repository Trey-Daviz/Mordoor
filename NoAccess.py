import Access as a


class NoAccess(a.Access):
    def __init__(self, user):
        self._user = user
        self.instances = {}

    def instance(self, user):
        if not self.instances.keys().__contains__(user):
            self.instances[user] = NoAccess(user)
        return self.instances[user]

