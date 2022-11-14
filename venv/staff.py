import pymysql
from queries import Queries
import keyboard, time
from door import Door

class Staff:

    def __init__(self, username=None):
        self.uid = None
        self.username = username
        self.password = None
        self.role = None
        if username is not None:
            self.fill_out_info()

    def get_connection(self):
        return pymysql.connect(host='localhost',
                                     user='trey',
                                     password='trey',
                                     database='mordoor',
                                     cursorclass=pymysql.cursors.DictCursor)

    def set_username(self, username):
        self.username = username
    def get_username(self):
        return self.username

    def set_password(self, password):
        self.password = password
    def get_password(self):
        return self.password

    def set_uid(self, uid):
        self.uid = uid
    def get_uid(self):
        return self.uid

    def set_role(self):
        self.role = self.get_access_level(self.get_uid())
    def get_role(self):
        return self.role

    def check_access(self, doorID):
        if self.role == "admin":
            return("The user has access")
        elif self.role == "elevated":
            has_access = self.check_user_access_elevated(self.uid, doorID)
            if has_access is True:
                return ("The user has access"), True
            else:
                has_access = self.check_user_access_dept(self.uid, doorID)
                if has_access is True: return ("The user has access"), True
                else: return("The user does not have access"), False

        elif self.role == "employee":
            has_access = self.check_user_access_dept(self.uid, doorID)
            if has_access is True: return ("The user has access"), True
            else: return("The user does not have access"), False

    def check_user_access_dept(self, uid, doorID):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "SELECT deptID FROM deptdoor WHERE doorID = %s"
                    database.execute(sql, (doorID))
                    department = database.fetchall()
                    for i in department:
                        sql = "SELECT * FROM employeedept WHERE userID = %s AND deptID = %s"
                        database.execute(sql, (uid, i["deptID"]))
                        user_in_department = database.fetchone()
                        if user_in_department is not None:
                            break
                    if user_in_department is None:
                        print("The user is not a part of a department with access to that door")
                        return ("The user is not a part of a department with access to that door")
                    else:
                        return True
                except Exception as error:
                    return {"error": error}

    def check_user_access_elevated(self, uid, doorID):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "SELECT * FROM elevateddoor WHERE userID = %s AND doorID = %s"
                    database.execute(sql, (uid, doorID))
                    value = database.fetchone()
                    if value is None:
                        return {"The user does not have access to that door"}
                    else:
                        return True
                except Exception as error:
                    return {"error": error}

    def get_access_level(self, uid):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "SELECT role FROM staff WHERE userID = %s"
                    database.execute(sql, (uid))
                    role = database.fetchone()["role"]
                    roles = {
                        '0': "admin",
                        '1': "elevated",
                        '2': "employee"
                    }
                    return roles[role]
                except Exception as error:
                    return {"error": error}

    def fill_out_info(self):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "SELECT userID FROM staff WHERE username = %s"
                    database.execute(sql, (self.username))
                    self.set_uid(database.fetchone()["userID"])

                    sql = "SELECT password FROM staff WHERE userID = %s"
                    database.execute(sql, (self.uid))
                    self.set_password(database.fetchone()["password"])

                    self.set_role()

                except Exception as error:
                    return {"error": error}

    def remove_user(self):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "DELETE FROM staff WHERE userID = %s"
                    database.execute(sql, (self.uid))
                    connection.commit()

                except Exception as error:
                    return {"error": error}