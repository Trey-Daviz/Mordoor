from abc import abstractproperty, ABC


class Access(object):

    def remove_user(self, sys_obj):
        return False

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
        return False

    def open_door(self, sys_obj):
        return False

    def change_state(self, sys_obj, new_state):
        sys_obj.change_state(new_state)

