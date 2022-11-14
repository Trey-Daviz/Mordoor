import pymysql
from queries import Queries
from dept import Dept
import keyboard, time

class Door:
    def __init__(self, door_name = None):
        self.door_name = door_name
        self.door_id = None
        if door_name is not None:
            self.door_name = self.door_name.upper()
            self.set_door_id(self.door_name)


    def set_door_id(self, doorname):
        self.door_id = self.grab_door_id()
    def get_door_id(self):
        return self.door_id

    def set_door_name(self, door_name):
        self.door_name = door_name
    def get_door_name(self):
        return self.door_name


    def get_connection(self):
        return pymysql.connect(host='localhost',
                                     user='trey',
                                     password='trey',
                                     database='mordoor',
                                     cursorclass=pymysql.cursors.DictCursor)

    def grab_door_id(self):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "SELECT doorID FROM door WHERE doorname = %s"
                    database.execute(sql, (self.door_name))
                    doorID = database.fetchone()
                    if doorID is None:
                        return None
                    else:
                        return(doorID["doorID"])
                except Exception as error:
                    return {"error": error}

    def add_door_to_user(self, uid):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    door_valid = self.does_door_exist()
                    if door_valid is True:
                        sql = "INSERT INTO elevateddoor VALUES (%s, %s)"
                        database.execute(sql, (uid, self.door_id))
                        connection.commit()
                    else:
                        print(door_valid)
                        return door_valid
                except Exception as error:
                    return {"error": error}

    def check_lock_state(self):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "SELECT locked_state FROM door WHERE doorname = %s"
                    database.execute(sql, (self.door_name))
                    sql_val = database.fetchone()["locked_state"]
                    if sql_val == 1: locked_state = True
                    else: locked_state = False
                    return locked_state
                except Exception as error:
                    return {"error": error}

    def change_locked_state(self, user):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    locked_state = self.check_lock_state()
                    if locked_state == True: locked_state = 0
                    else: return {"error": "That door is already unlocked"}

                    sql = "UPDATE door SET locked_state = %s WHERE doorname = %s"
                    database.execute(sql, (locked_state, self.door_name))
                    connection.commit()

                    uid = user.get_uid()
                    username = user.get_username()

                    self.write_log(uid, username)

                except Exception as error:
                    return {"error": error}

    def create_door(self, deptID, door_name):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "SELECT doorname FROM door WHERE doorname = %s"
                    database.execute(sql, (door_name))
                    sql_val = database.fetchone()

                    if sql_val is None:
                        sql = "INSERT INTO door(doorname) VALUES (%s)"
                        database.execute(sql, (door_name))
                        connection.commit()
                        self.set_door_name(door_name)
                        self.set_door_id(door_name)

                        if isinstance(deptID, int):
                            dept = Dept(deptID)
                            dept.add_dept_to_door(self.door_id)
                        else:
                            for id in deptID:
                                dept = Dept(id)
                                dept.add_dept_to_door(self.door_id)
                    else:
                        raise ValueError("That door already exists")

                except Exception as error:
                    return {"error": error}

    def write_log(self, uid, username):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "INSERT INTO logs(userID, username, doorID, doorname) VALUES(%s, %s, %s, %s)"
                    database.execute(sql, (uid, username, self.door_id, self.door_name))
                    connection.commit()

                except Exception as error:
                    return {"error": error}

    def does_door_exist(self):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "SELECT doorID FROM door WHERE doorID = %s"
                    database.execute(sql, (self.door_id))
                    value = database.fetchone()
                    if value is None:
                        return {"error": "The door does not exist"}
                    else:
                        return True
                except Exception as error:
                    return {"error": error}

    def remove_door(self):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "DELETE FROM door WHERE doorID = %s"
                    database.execute(sql, (self.door_id))
                    connection.commit()
                    sql = "DELETE FROM elevateddoor WHERE doorID = %s"
                    database.execute(sql, (self.door_id))
                    connection.commit()
                    sql = "DELETE FROM deptdoor WHERE doorID = %s"
                    database.execute(sql, (self.door_id))
                    connection.commit()
                except Exception as error:
                    return {"error": error}