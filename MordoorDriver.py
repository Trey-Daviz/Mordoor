import MordoorSystem as ms
import Credentials as c

if __name__ == "__main__":
    creds = c.Credentials("user", "AdminPass")
    system = ms.MordoorSystem(creds)
    system.remove_user()
    system.login(creds)
    system.remove_user()

