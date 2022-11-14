import MordoorSystem as ms
import Credentials as c
import sys

if __name__ == "__main__":
    try:
        creds = c.Credentials("twdavis", "passwd")
    except ValueError as v:
        sys.exit(v)
    system = ms.MordoorSystem(creds)

    # try:
    #     system.add_door('IT2')
    # except Exception as e:
    #     sys.exit(e)
    #
    # try:
    #     system.create_user('Test', 'User', 2, 'TestUser', 'TestPass')
    # except Exception as e:
    #     sys.exit(e)
    #
    # try:
    #     system.create_dept('TestDept')
    # except Exception as e:
    #     sys.exit(e)
    #
    # try:
    #     system.remove_door(6)
    # except Exception as e:
    #     sys.exit(e)
    #
    # try:
    #     system.remove_dept(6)
    # except Exception as e:
    #     sys.exit(e)
    #
    # try:
    #     system.add_door_to_elevated(1,2)
    # except Exception as e:
    #     sys.exit(e)
    #
    # try:
    #     system.add_dept_to_user(1, 2)
    # except Exception as e:
    #     sys.exit(e)
    #
    # try:
    #     system.add_dept_to_door(1, 2)
    # except Exception as e:
    #     sys.exit(e)
    #
    # try:
    #     system.open_door(4)
    # except Exception as e:
    #     sys.exit(e)
