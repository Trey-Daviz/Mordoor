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


    def remove_door(self, sys_obj):
        return False

    def add_door(self, sys_obj):
        return False

    def create_user(self, sys_obj):
        return False

    def add_door_to_user(self, sys_obj):
        return False

    def view_logs(self, sys_obj):
        return False

    def add_dept_to_user(self, sys_obj):
        return False

    def add_dept_to_door(self, sys_obj):
        return False

    def create_dept(self, sys_obj):
        return False

    def remove_dept(self, sys_obj):
        return False

    def login(self, sys_obj):
        if self.user.is_admin():
            self.change_state(au.AdminUser(self._user))
        elif self.user.is_elevated():
            self.change_state(eu.ElevatedAccess())
        elif self.user.is_normal():
            self.change_state(nu.NormalUser())
        else:
            print("Login not allowed")

    def change_state(self, new_state):
        self._access = new_state