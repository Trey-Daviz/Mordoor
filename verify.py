import Credentials as c


def verify(func):
    def handler(info):
        creds = None
        try:
            creds = c.Credentials(info["username"], info["password"])
            to_return = True
        except ValueError as v:
            to_return = str(v)
        func_ret = func(to_return, creds, info)
        return func_ret
    return handler
