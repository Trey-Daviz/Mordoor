import Access as a


class AdminUser(a.Access):
    def remove_user(self, sys_obj):
        return True

    def remove_door(self, sys_obj):
        return True

    def add_door(self, sys_obj):
        return True

    def create_user(self, sys_obj):
        return True

    def add_door_to_elevated(self, sys_obj):
        return True

    def view_logs(self, sys_obj):
        return True

    def add_dept_to_user(self, sys_obj):
        return True

    def add_dept_to_door(self, sys_obj):
        return True

    def create_dept(self, sys_obj):
        return True

    def remove_dept(self, sys_obj):
        return True

    def login(self, sys_obj):
        return True

    def open_door(self, sys_obj):
        return True

    def change_state(self, sys_obj, new_state):
        sys_obj.change_state(new_state)

