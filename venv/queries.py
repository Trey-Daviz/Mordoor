import pymysql
import keyboard, time

class Queries:
    def __init__(self, message):
        self.message = message

    def check_validity(self, user):
        try:
            # Check for username and password validity
            username_valid = self.check_username(user.get_username())
            if username_valid is True:
                password_valid = self.check_passwd(user.get_username(), user.get_password())
                if password_valid is True:
                    return True
                else:
                    return("Incorrect Password!")
            else:
                return("Incorrect Username!")
        except Exception as error:
            return {"error": error}



    def get_connection(self):
        return pymysql.connect(host='localhost',
                                     user='trey',
                                     password='trey',
                                     database='mordoor',
                                     cursorclass=pymysql.cursors.DictCursor)

    def check_username(self, username):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "SELECT username FROM staff WHERE username = %s"
                    database.execute(sql, (username))
                    value = database.fetchone()
                    if value is None:
                        return None
                    value = value["username"]
                    return True
                except Exception as error:
                    return {"error": error}

    def check_passwd(self, username, password):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "SELECT password FROM staff WHERE username = %s"
                    database.execute(sql, (username))
                    passwd = database.fetchone()["password"]
                    if passwd != password:
                        raise ValueError("The password is incorrect")
                    else:
                        return True

                except Exception as error:
                    return {"error": error}

    def grab_uid(self, username):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "SELECT userID FROM staff WHERE username = %s"
                    database.execute(sql, (username))
                    uid = database.fetchone()["userID"]
                    return uid
                except Exception as error:
                    return {"error": error}

    def create_user(self, fName, lName, role, uName, pwd):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "SELECT username FROM staff WHERE username = %s"
                    database.execute(sql, (uName))
                    sql_val = database.fetchone()

                    if sql_val is None:
                        sql = "INSERT INTO staff (firstname, lastname, role, username, password) VALUES(%s, %s, %s, %s, %s)"
                        database.execute(sql, (fName,lName,role,uName,pwd))
                        connection.commit()
                    else:
                        raise ValueError("The username given is already taken.  Try again")
                except Exception as error:
                    return {"error": error}

    def view_logs(self):
        connection = self.get_connection()
        with connection:
            with connection.cursor() as database:
                try:
                    sql = "SELECT * FROM logs ORDER BY time DESC LIMIT 10"
                    database.execute(sql)
                    view = database.fetchall()
                    return view

                except Exception as error:
                    return {"error": error}


