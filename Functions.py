from sql_access import database_connect


class Functions():
    def __init__(self, user):
        self._user = user

    def remove_user(self):
        print("Removing user")

    @database_connect
    def remove_door(self, conn, did):
        with conn.cursor() as db:
            try:
                sql = "DELETE FROM door WHERE doorID = %s" % did
                db.execute(sql)
                print("Door removed")
            except Exception as error:
                raise

    @database_connect
    def add_door(self, conn, name):
        with conn.cursor() as db:
            try:
                sql = "INSERT INTO door(doorname) VALUES('%s')" % name
                db.execute(sql)
                print("Door added")
            except Exception as e:
                raise e

    @database_connect
    def create_user(self, conn, firstname, lastname, role, username, passwd):
        with conn.cursor() as db:
            try:
                sql = "INSERT INTO staff(firstname, lastname, role, username, password) VALUES('%s', '%s', %s, '%s', '%s')" % (
                firstname, lastname, role, username, passwd)
                db.execute(sql)
                print("Created user")
            except Exception as e:
                raise e
    @database_connect
    def add_door_to_elevated(self, conn, did, uid):
        with conn.cursor() as db:
            try:
                sql = "SELECT role FROM staff WHERE userID = %s" % uid
                db.execute(sql)
                role = db.fetchone()["role"]
                if role == '1':
                    sql = "INSERT INTO elevateddoor VALUES (%s, %s)" % (uid, did)
                    db.execute(sql)
                    print("Elevated user now has access to that door")
                else:
                    raise ValueError("You can not add an individual door to a non elevated user")
            except Exception as e:
                raise e

    def view_logs(self):
        print("Viewing Logs")

    @database_connect
    def add_dept_to_user(self, conn, did, uid):
        with conn.cursor() as db:
            try:
                sql = "SELECT role FROM staff WHERE userID = %s" % uid
                db.execute(sql)
                role = db.fetchone()["role"]
                if role == '0':
                    raise ValueError("You can not add departments to administrators")
                else:
                    sql = "INSERT INTO employeedept VALUES(%s, %s)" % (uid, did)
                    db.execute(sql)
                    print("Department has been added to that user")
            except Exception as e:
                raise e
    @database_connect
    def add_dept_to_door(self, conn, dept_id, door_id):
        with conn.cursor() as db:
            try:
                sql = "INSERT INTO deptdoor VALUES(%s, %s)" % (door_id, dept_id)
                db.execute(sql)
                print("That department has been added to that door")
            except Exception as e:
                raise e

    @database_connect
    def create_dept(self, conn, name):
        with conn.cursor() as db:
            try:
                sql = "INSERT INTO dept(deptname) VALUES('%s')" % name
                db.execute(sql)
                print("Created dept")
            except Exception as e:
                raise e
    @database_connect
    def remove_dept(self, conn, did):
        with conn.cursor() as db:
            try:
                sql = "DELETE FROM dept WHERE deptID = %s" % did
                db.execute(sql)
                print("Removed dept")
            except Exception as e:
                raise e

    @database_connect
    def open_door(self, conn, user, did):
        with conn.cursor() as db:
            try:
                open = False
                if user.role == '1' or user.role == '2':
                    sql = "SELECT * from deptdoor WHERE doorID = %s" % did
                    db.execute(sql)
                    doors = db.fetchall()
                    depts = []
                    for i in doors:
                        depts.append(i["deptID"])
                    for i in depts:
                        sql = "SELECT * FROM employeedept WHERE userID = %s and deptID = %s" % (user.uid, i)
                        db.execute(sql)
                        if db.fetchone():
                            open = True
                    if user.role == '1' and not open:
                        sql = "SELECT doorID FROM elevateddoor WHERE userID = %s" % user.uid
                        db.execute(sql)
                        result = db.fetchall()
                        doors = []
                        for i in result:
                            doors.append(i["doorID"])
                        for i in doors:
                            if i == did:
                                open = True
                elif user.role == '0':
                    open = True
                if open:
                    sql = "UPDATE door SET locked_state = 0 WHERE doorID = %s" % did
                    db.execute(sql)
                    print("Door opened")
                else:
                    raise ValueError("That user does not have access to that door")
            except Exception as e:
                raise e

    def login(self):
        print(f"Logging in {self._user}")
