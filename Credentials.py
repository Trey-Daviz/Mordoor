from sql_access import database_connect


class Credentials:
    def __init__(self, name, passwd):
        self._name = name
        self._passwd = passwd
        self._role, self._uid = self.login(self._name, self._passwd)

    @property
    def name(self):
        return self._name

    @property
    def passwd(self):
        return self._passwd

    @property
    def role(self):
        return self._role

    @property
    def uid(self):
        return self._uid

    @database_connect
    def login(self, conn, name, passwd):
        with conn.cursor() as db:
            try:
                sql = "SELECT username from staff where username = '%s'" %name
                db.execute(sql)
                if not db.fetchone():
                    raise(ValueError("That user does not exist"))
                else:
                    sql = "SELECT password FROM staff WHERE username = '%s'" % name
                    db.execute(sql)
                    if passwd != db.fetchone()["password"]:
                        raise (ValueError("That password is incorrect"))
                    else:
                        sql = "SELECT role, userID FROM staff WHERE username = '%s'" % name
                        db.execute(sql)
                        fetch = db.fetchone()
                        print("Logged in successfully")
                        return fetch["role"], fetch["userID"]
            except Exception as e:
                raise
