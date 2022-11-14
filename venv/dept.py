import pymysql
from queries import Queries
import keyboard, time

class Dept:
    def __init__(self, dept_id = None):
        self.dept_id = dept_id

    def get_connection(self):
        return pymysql.connect(host='localhost',
                                     user='trey',
                                     password='trey',
                                     database='mordoor',
                                     cursorclass=pymysql.cursors.DictCursor)


    def add_dept_to_user(self, uid):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    dept_exist = self.does_dept_exist()
                    if dept_exist is True:
                        sql = "INSERT INTO employeedept VALUES (%s, %s)"
                        database.execute(sql, (uid, self.dept_id))
                        connection.commit()
                    else:
                        print(dept_exist)
                        return dept_exist
                except Exception as error:
                    return {"error": error}

    def add_dept_to_door(self, doorID):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "INSERT INTO deptdoor VALUES (%s, %s)"
                    database.execute(sql, (doorID, self.dept_id))
                    connection.commit()
                except Exception as error:
                    return {"error": error}

    def does_dept_exist(self):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "SELECT deptID FROM dept WHERE deptID = %s"
                    database.execute(sql, (self.dept_id))
                    value = database.fetchone()
                    if value is None:
                        return {"error": "The department does not exist"}
                    else:
                        return True
                except Exception as error:
                    return {"error": error}

    def create_dept(self, deptname):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "SELECT deptname FROM dept WHERE deptname = %s"
                    database.execute(sql, (deptname))
                    sql_val = database.fetchone()

                    if sql_val is None:
                        sql = "INSERT INTO dept(deptname) VALUES(%s)"
                        database.execute(sql, (deptname))
                        connection.commit()
                    else:
                        raise ValueError("That department already exists")

                except Exception as error:
                    return {"error": error}

    def remove_dept(self, dept_id):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "DELETE FROM dept WHERE deptID = %s"
                    database.execute(sql, (dept_id))
                    connection.commit()
                    sql = "DELETE FROM deptdoor WHERE deptID = %s"
                    database.execute(sql, (dept_id))
                    connection.commit()
                    sql = "DELETE FROM employeedept WHERE deptID = %s"
                    database.execute(sql, (dept_id))
                    connection.commit()
                except Exception as error:
                    return {"error": error}