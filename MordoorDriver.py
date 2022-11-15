import MordoorSystem as ms
import Credentials as c
import sys
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import http
import json
import socket
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/noAccess/login", status_code=http.HTTPStatus.ACCEPTED)
async def login(request : Request) -> None:
    info = await request.body()
    info = info.decode("utf-8")
    info = json.loads(info)
    try:
        creds = c.Credentials(info["username"], info["password"])
    except ValueError as v:
        return(str(v))
    return True


@app.post("/admin/create_user", status_code=http.HTTPStatus.ACCEPTED)
async def login(request : Request) -> str:
    info = await request.body()
    info = info.decode("utf-8")
    info = json.loads(info)
    try:
        creds = c.Credentials(info["username"], info["password"])
    except ValueError as v:
        return(str(v))
    system = ms.MordoorSystem(creds)
    try:
        return system.create_user(info["first"], info["last"], info["r"], info["uname"], info["pwd"])
    except Exception as e:
        return (str(e))


@app.post("/admin/add_door", status_code=http.HTTPStatus.ACCEPTED)
async def add_door(request : Request) -> str:
    info = await request.body()
    info = info.decode("utf-8")
    info = json.loads(info)
    try:
        creds = c.Credentials(info["username"], info["password"])
    except ValueError as v:
        return str(v)
    system = ms.MordoorSystem(creds)
    try:
        return system.add_door(info["d"])
    except Exception as e:
        return str(e)


def main():
    uvicorn.run("MordoorDriver:app", host=ip)

if __name__ == "__main__":
    main()

    # try:
    #     system.create_user('Test', 'User', 2, 'TestUser', 'TestPass')
    # except Exception as e:
    #     sys.exit(e)

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

    # try:
    #     system.remove_user(5)
    # except Exception as e:
    #     sys.exit(e)

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

    # try:
    #     system.view_logs()
    # except Exception as e:
    #     sys.exit(e)
