def block(func):
    def handler(*args, **kwargs):
        print("Hit catch block")
        try:
            func(*args, **kwargs)
            return True
        except Exception as error:
            if error.args[0] == 1062:
                return "The field you are attempting to create already exists"
            return str(error)
    return handler
