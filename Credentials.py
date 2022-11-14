class Credentials:
    def __init__(self, name, passwd):
        self._name = name
        self._passwd = passwd

    @property
    def name(self):
        return self._name

    def validate(self, passwd):
        return self._passwd == passwd

    def is_admin(self):
        return self._passwd == "AdminPass"

    def is_normal(self):
        return self._passwd == "NormalPass"

    def is_elevated(self):
        return self._passwd == "ElevatedPass"

