from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import kivy.core.text.markup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from staff import Staff
from dept import Dept
from queries import Queries
from door import Door
import pymysql
import time
import keyboard
from kivy.uix.image import Image


# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_file("login.kv")

# Declare both screens
class MenuScreen(Screen):
    pass


class UserScreen(Screen):
    pass


class AdminScreen(Screen):
    pass


class AdminInfoScreen(Screen):
    pass


class CreateEntry(Screen):
    pass

class CreateUser(Screen):
    pass

class CreateDoor(Screen):
    pass

class CreateDept(Screen):
    pass

class RemoveEntry(Screen):
    pass

class RemoveUser(Screen):
    pass

class RemoveDoor(Screen):
    pass

class RemoveDept(Screen):
    pass

class Info(Screen):
    pass

class AppendEntry(Screen):
    pass

class DeptToUser(Screen):
    pass

class DoorToElevated(Screen):
    pass

class DeptToDoor(Screen):
    pass

class TestApp(MDApp):

    def __init__(self):
        super().__init__()
        self.sm = None
        self.user_logged_in = None

    def get_connection(self):
        return pymysql.connect(host='localhost',
                             user='trey',
                             password='trey',
                             database='mordoor',
                             cursorclass=pymysql.cursors.DictCursor)

    def switch_to_menu(self):
        sm = self.sm
        sm.current = "menu"

    def clear(self):
        self.root.get_screen('menu').ids.username.text = ""
        self.root.get_screen('menu').ids.passwd.text = ""

    def switch_to_user(self):
        # To create the user authentication, plug in authentication with an if else here, and make it change screens
        # if properly validated else, have it alert the user of their incorrect input using MDDialog
        # also have it check for user type, and route to that type with nested if else
        sm = self.sm
        query_obj = Queries("Hello")
        user_logged_in = Staff()
        if self.root.get_screen('menu').ids.username.text == "":
            dialog = MDDialog(title="ERROR", text="The username must not be nothing")
            dialog.open()
            return "Null username"
        else:
            user_logged_in.set_username(self.root.get_screen('menu').ids.username.text)
        if self.root.get_screen('menu').ids.passwd.text == "":
            dialog = MDDialog(title="ERROR", text="The password must not be nothing")
            dialog.open()
            return "Null passwd"
        else:
            user_logged_in.set_password(self.root.get_screen('menu').ids.passwd.text)

        check_valid = query_obj.check_validity(user_logged_in)
        if check_valid is not True:
            dialog = MDDialog(title="ERROR", text=check_valid)
            dialog.open()
            return(check_valid)
        user_logged_in.fill_out_info()
        self.user_logged_in = user_logged_in
        if user_logged_in.get_role() == "admin":
            sm.current = "admin"
        else:
            sm.current = "user"


    def switch_to_admin(self):
        sm = self.sm
        sm.current = "admin"

    def switch_to_adminInfo(self):
        sm = self.sm
        sm.current = "admininfo"

    def switch_to_CreateEntry(self):
        sm = self.sm
        sm.current = "createentry"

    def switch_to_CreateUser(self):
        sm = self.sm
        sm.current = "createuser"

    def switch_to_CreateDoor(self):
        sm = self.sm
        sm.current = "createdoor"

    def switch_to_CreateDept(self):
        sm = self.sm
        sm.current = "createdept"


    def switch_to_RemoveEntry(self):
        sm = self.sm
        sm.current = "removeentry"

    def switch_to_RemoveUser(self):
        sm = self.sm
        sm.current = "removeuser"

    def switch_to_RemoveDoor(self):
        sm = self.sm
        sm.current = "removedoor"

    def switch_to_RemoveDept(self):
        sm = self.sm
        sm.current = "removedept"

    def switch_to_AppendEntry(self):
        sm = self.sm
        sm.current = "appendentry"

    def switch_to_DeptToUser(self):
        sm = self.sm
        sm.current = 'depttouser'

    def switch_to_DoorToElevated(self):
        sm = self.sm
        sm.current = 'doortoelevated'

    def switch_to_DeptToDoor(self):
        sm = self.sm
        sm.current = 'depttodoor'

    def ViewLogs(self):
        query_obj = Queries("View Logs")
        view_log = query_obj.view_logs()

        for i in view_log:
            for j in i.keys():
                if j == "time":
                    i[j] = i[j].strftime("%Y:%m:%d %H:%M:%S")
        log_string = "[color=ffaa9c]"

        for i in view_log:
            log_string += f"LogID {i['logID']}\nUser {i['username']} opened door {i['doorname']} at {i['time']}\n"
        log_string+="[/color]"

        dialog = MDDialog(title="Logs", text=log_string)
        dialog.open()

    def switch_to_Info(self):
        sm = self.sm
        sm.current = "info"

    def unlock_door(self):

        try:
            # Here, have it query to see if access is allowed to said door, if so, unlock door and notify user
            # otherwise, tell the user the door doesn't exist, or they don't have access
            user_logged_in = self.user_logged_in

            if user_logged_in.get_role() != 'admin':
                door = Door(self.root.get_screen('user').ids.DName.text)
                if door.get_door_id() is None:
                    dialog = MDDialog(title="ERROR", text="This door does not exist")
                    dialog.open()
                    return "This door does not exist"
                access_message, has_access = (user_logged_in.check_access(door.get_door_id()))
                if has_access:
                    change_lock = door.change_locked_state(user_logged_in)
                    if change_lock is not None:
                        dialog = MDDialog(title="ERROR", text=str(change_lock))
                        dialog.open()
                        return change_lock
                    else:
                        dialog = MDDialog(title="Success", text="The door has opened!")
                        dialog.open()
                else:
                    dialog = MDDialog(title="ERROR", text=str(access_message))
                    dialog.open()
                    return access_message
            else:
                door = Door(self.root.get_screen('admin').ids.DName.text)
                if door.get_door_id() is None:
                    dialog = MDDialog(title="ERROR", text="This door does not exist")
                    dialog.open()
                    return "This door does not exist"
                change_lock = door.change_locked_state(user_logged_in)
                if change_lock is not None:
                    dialog = MDDialog(title="ERROR", text=change_lock)
                    dialog.open()
                    return change_lock
                else:
                    dialog = MDDialog(title="Success", text="The door has opened!")
                    dialog.open()


        except Exception as error:
            return {"error": error}

    def create_door(self):
        # doorname = input("Enter the name for the new door: ")
        # departments = input("Enter the department IDs that should have access to this new door.  For multiple "
        #                     "departments, please separate the IDs by a comma and no space.  Hit enter when done: ")
        doorname = self.root.get_screen('createdoor').ids.door_name.text
        departments = self.root.get_screen('createdoor').ids.deptID.text

        departments = departments.split(",")
        door_to_add = Door()

        create_door = door_to_add.create_door(departments, doorname)
        if create_door is not None:
            dialog = MDDialog(title="ERROR", text=create_door)
            dialog.open()
            return create_door
        else:
            dialog = MDDialog(title="Success", text="Door Created!")
            dialog.open()

    def create_user(self):
        query_obj = Queries("Create User")
        firstname = self.root.get_screen('createuser').ids.fname.text
        lastname = self.root.get_screen('createuser').ids.lname.text
        role = self.root.get_screen('createuser').ids.role.text
        new_username = self.root.get_screen('createuser').ids.uname.text
        password = self.root.get_screen('createuser').ids.pwd.text

        create_user = query_obj.create_user(firstname, lastname, role, new_username, password)
        if create_user is not None:
            dialog = MDDialog(title="ERROR", text=create_user)
            dialog.open()
            return create_user
        else:
            dialog = MDDialog(title="Success", text="User Created!")
            dialog.open()

    def create_dept(self):
        dept_name = self.root.get_screen('createdept').ids.deptID.text
        dept = Dept()

        create_dept = dept.create_dept(dept_name)
        if create_dept is not None:
            dialog = MDDialog(title="ERROR", text=create_dept)
            dialog.open()
            return create_dept
        else:
            dialog = MDDialog(title="Success", text="Department Created!")
            dialog.open()

    def remove_door(self):
        door_to_delete = self.root.get_screen('removedoor').ids.doorName.text
        door = Door(door_to_delete)

        delete_door = door.remove_door()
        if delete_door is not None:
            dialog = MDDialog(title="ERROR", text=delete_door)
            dialog.open()
            return delete_door
        else:
            dialog = MDDialog(title="Success", text="Door Removed!")
            dialog.open()

    def remove_dept(self):
        dept_to_delete = int(self.root.get_screen('removedept').ids.deptID.text)
        dept = Dept()

        delete_dept = dept.remove_dept(dept_to_delete)
        if delete_dept is not None:
            dialog = MDDialog(title="ERROR", text=delete_dept)
            dialog.open()
            return delete_dept
        else:
            dialog = MDDialog(title="Success", text="Dept Removed!")
            dialog.open()

    def remove_user(self):
        query_obj = Queries("remove door")
        user_to_del = self.root.get_screen('removeuser').ids.username.text
        u_obj = Staff(user_to_del)

        remove_user = u_obj.remove_user()
        if remove_user is not None:
            dialog = MDDialog(title="ERROR", text=str(remove_user))
            dialog.open()
            return remove_user
        else:
            dialog = MDDialog(title="Success", text="User Removed!")
            dialog.open()

    def get_user_info(self):
        user = Staff(self.root.get_screen('info').ids.UserInfo.text)
        uid = user.get_uid()
        role = user.get_role()

        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                sql = "SELECT firstname, lastname FROM staff WHERE username = %s"
                database.execute(sql, (user.get_username()))
                names = database.fetchone()
                fName = names["firstname"]
                lName = names["lastname"]
                thing_to_print = f"Name: {fName} {lName}\n\nUserID: {uid}\n\nRole: {role}\n\nDepartments: "

                if role == "employee" or role == "elevated":
                    sql = "SELECT deptID FROM employeedept WHERE userID = %s"
                    database.execute(sql, (uid))
                    departments = database.fetchall()
                    department_names = []
                    sql = "SELECT deptname FROM dept WHERE deptID = %s"
                    for i in departments:
                        database.execute(sql, (i["deptID"]))
                        department_names.append(database.fetchone()["deptname"])
                    for counter, i in enumerate(department_names):
                        if counter == len(department_names) - 1:
                            thing_to_print = thing_to_print +  f"{i}"
                        else:
                            thing_to_print = thing_to_print +  f"{i}, "
                if role == "elevated":
                    thing_to_print = thing_to_print + "\n\nUnique Doors: "
                    sql = "SELECT doorID FROM elevateddoor WHERE userID = %s"
                    database.execute(sql, (user.get_uid()))
                    doors = database.fetchall()
                    doors_names = []
                    sql = "SELECT doorname FROM door WHERE doorID = %s"
                    for i in doors:
                        database.execute(sql, (i["doorID"]))
                        doors_names.append(database.fetchone()["doorname"])
                    for counter, i in enumerate(doors_names):
                        if counter == len(doors_names) - 1:
                            thing_to_print += f"{i}\n"
                        else:
                            thing_to_print += f"{i}, "
                if role == "admin":
                    thing_to_print+="All of them"

        dialog = MDDialog(title=user.get_username(), text=thing_to_print)
        dialog.open()

    def get_door_info(self):
        door = Door(self.root.get_screen('info').ids.DoorInfo.text)
        doorID = door.get_door_id()
        thing_to_print = f"DoorID: {doorID}\n\nDepartments: "
        sql = "SELECT deptID FROM deptdoor WHERE doorID = %s"
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                database.execute(sql, (doorID))
                departments = database.fetchall()
                department_names = []
                sql = "SELECT deptname FROM dept WHERE deptID = %s"
                for i in departments:
                    database.execute(sql, (i["deptID"]))
                    department_names.append(database.fetchone()["deptname"])

                for counter, i in enumerate(department_names):
                    if counter == len(department_names):
                        thing_to_print += f"{i}\n"
                    else:
                        thing_to_print += f"{i}, "

        dialog = MDDialog(title=door.get_door_name(), text=thing_to_print)
        dialog.open()

    def add_dept_to_user(self):
        query_obj = Queries("Add Dept to User")
        username = self.root.get_screen('depttouser').ids.username.text
        deptID = self.root.get_screen('depttouser').ids.deptID.text
        dept = Dept(deptID)
        user_exists = query_obj.check_username(username)
        if user_exists is None:
            dialog = MDDialog(title="ERROR", text="That user does not exist")
            dialog.open()
            return user_exists

        uid = query_obj.grab_uid(username)

        add_dept_to_user = dept.add_dept_to_user(uid)
        if add_dept_to_user is not None:
            dialog = MDDialog(title="ERROR", text=str(add_dept_to_user))
            dialog.open()
            return add_dept_to_user
        else:
            dialog = MDDialog(title="Success", text="Department added to User")
            dialog.open()

    def add_door_to_elevated(self):
        query_obj = Queries("Door to Elevated")
        username = (self.root.get_screen('doortoelevated').ids.username.text)
        doorname = (self.root.get_screen('doortoelevated').ids.Dname.text)
        user_exists = query_obj.check_username(username)
        if not user_exists:
            dialog = MDDialog(title="ERROR", text=user_exists)
            dialog.open()
        else:
            user = Staff(username)

            is_elevated = user.get_access_level(query_obj.grab_uid(username))
            if is_elevated != "elevated":
                dialog = MDDialog(title="ERROR", text="The username given is not attributed to an elevated user")
                dialog.open()
            else:
                door = Door(doorname)

                add_door_to_user = door.add_door_to_user(user.get_uid())
                if add_door_to_user is not None:
                    dialog = MDDialog(title="ERROR", text=str(add_door_to_user))
                    dialog.open()
                else:
                    dialog = MDDialog(title="Success", text="Door added to user")
                    dialog.open()

    def add_dept_to_door(self):
        doorname = (self.root.get_screen('depttodoor').ids.doorName.text)
        deptID = (self.root.get_screen('depttodoor').ids.deptID.text)
        door = Door(doorname)
        dept = Dept(deptID)

        add_dept_to_door = dept.add_dept_to_door(door.get_door_id())
        if add_dept_to_door is not None:
            dialog = MDDialog(title="ERROR", text=str(add_dept_to_door))
            dialog.open()
        else:
            dialog = MDDialog(title="Success", text="Dept added to door")
            dialog.open()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        # Create the screen manager
        sm = ScreenManager()
        self.sm = sm
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(UserScreen(name='user'))
        sm.add_widget(AdminScreen(name="admin"))
        sm.add_widget(AdminInfoScreen(name="admininfo"))
        sm.add_widget(CreateEntry(name="createentry"))
        sm.add_widget(CreateUser(name="createuser"))
        sm.add_widget(CreateDoor(name="createdoor"))
        sm.add_widget(CreateDept(name="createdept"))
        sm.add_widget(RemoveEntry(name="removeentry"))
        sm.add_widget(RemoveUser(name="removeuser"))
        sm.add_widget(RemoveDoor(name="removedoor"))
        sm.add_widget(RemoveDept(name="removedept"))
        sm.add_widget(AppendEntry(name="appendentry"))
        sm.add_widget(DeptToUser(name="depttouser"))
        sm.add_widget(DoorToElevated(name="doortoelevated"))
        sm.add_widget(DeptToDoor(name="depttodoor"))
        sm.add_widget(Info(name="info"))
        return sm


if __name__ == '__main__':
    TestApp().run()