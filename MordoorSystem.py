import Access
import Functions as f
import NoAccess as na
import AdminUser as au
import ElevatedUser as eu
import NormalUser as nu
from dataclasses import dataclass
import Credentials as c


@dataclass
class MordoorSystem:
    def __init__(self, user: c.Credentials):
        self._user = user
        self._functions = f.Functions(self.user)
        self.na_obj = na.NoAccess(self.user)
        self._access = self.na_obj.instance(self.user)
        self.login(self.user)

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    def remove_user(self, uid):
        if self._access.remove_user(self):
            self._functions.remove_user(uid)
            return True
        else:
            raise ValueError("User does not have access to that function")

    def remove_door(self, did):
        if self._access.remove_door(self):
            self._functions.remove_door(did)
            return True
        else:
            raise ValueError("User does not have access to that function")

    def add_door(self, name):
        if self._access.add_door(self):
            self._functions.add_door(name)
            return True
        else:
            raise ValueError("User does not have access to that function")

    def create_user(self, firstname, lastname, role, username, passwd):
        if self._access.create_user(self):
            self._functions.create_user(firstname, lastname, role, username, passwd)
            return True
        else:
            raise ValueError("User does not have access to that function")

    def add_door_to_elevated(self, did, uid):
        if self._access.add_door_to_elevated(self):
            self._functions.add_door_to_elevated(did, uid)
            return True
        else:
            raise ValueError("User does not have access to that function")

    def view_logs(self):
        if self._access.view_logs(self):
            self._functions.view_logs()
            return True
        else:
            raise ValueError("User does not have access to that function")

    def add_dept_to_user(self, did, uid):
        if self._access.add_dept_to_user(self):
            self._functions.add_dept_to_user(did, uid)
            return True
        else:
            raise ValueError("User does not have access to that function")

    def add_dept_to_door(self, dept_id, door_id):
        if self._access.add_dept_to_door(self):
            self._functions.add_dept_to_door(dept_id, door_id)
            return True
        else:
            raise ValueError("User does not have access to that function")

    def create_dept(self, name):
        if self._access.create_dept(self):
            self._functions.create_dept(name)
            return True
        else:
            raise ValueError("User does not have access to that function")

    def remove_dept(self, did):
        if self._access.remove_dept(self):
            self._functions.remove_dept(did)
            return True
        else:
            raise ValueError("User does not have access to that function")

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
            return True
        else:
            raise ValueError("User does not have access to that function")

    def change_state(self, new_state):
        self._access = new_state
