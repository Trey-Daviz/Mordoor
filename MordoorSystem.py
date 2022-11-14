import Access
import Functions as f
import NoAccess as na
import AdminUser as au
import ElevatedUser as eu
import NormalUser as nu


class MordoorSystem:

    def __init__(self, user):
        self._user = user
        self._functions = f.Functions(user)
        self.na_obj = na.NoAccess(user)
        self._access = self.na_obj.instance(user)
        self.login(self._user)

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    def remove_user(self):
        if self._access.remove_user(self):
            self._functions.remove_user()
        else:
            print("Removing user not allowed")

    def remove_door(self, did):
        if self._access.remove_door(self):
            self._functions.remove_door(did)
        else:
            print("Removing door not allowed")

    def add_door(self, name):
        if self._access.add_door(self):
            self._functions.add_door(name)
        else:
            print("Adding door not allowed")

    def create_user(self, firstname, lastname, role, username, passwd):
        if self._access.create_user(self):
            self._functions.create_user(firstname, lastname, role, username, passwd)
        else:
            print("Creating user not allowed")

    def add_door_to_elevated(self, did, uid):
        if self._access.add_door_to_elevated(self):
            self._functions.add_door_to_elevated(did, uid)
        else:
            print("Adding door to elevated user is not allowed")

    def view_logs(self):
        return False

    def add_dept_to_user(self, did, uid):
        if self._access.add_dept_to_user(self):
            self._functions.add_dept_to_user(did, uid)
        else:
            print("Adding dept to user not allowed")

    def add_dept_to_door(self, dept_id, door_id):
        if self._access.add_dept_to_door(self):
            self._functions.add_dept_to_door(dept_id, door_id)
        else:
            print("Adding dept to door not allowed")


    def create_dept(self, name):
        if self._access.create_dept(self):
            self._functions.create_dept(name)
        else:
            print("Create department not allowed")

    def remove_dept(self, did):
        if self._access.remove_dept(self):
            self._functions.remove_dept(did)
        else:
            print("Removing dept not allowed")

    def login(self, user):
        if user.role == '0':
            self.change_state(au.AdminUser())
        elif user.role == '1':
            self.change_state(eu.ElevatedAccess())
        elif user.role == '2':
            self.change_state(nu.NormalUser())

    def open_door(self, did):
        if self._access.open_door(self):
            self._functions.open_door(self._user, did)
        else:
            print("Open door not allowed")


    def change_state(self, new_state):
        self._access = new_state
