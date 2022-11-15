import MordoorSystem as ms
import Credentials as c
import sys
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import http
import json
import socket
from api_dec import api
from verify import verify

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
@api
@verify
def login(to_return, creds, info):
    print('hit')
    return to_return


@app.post("/admin/create_user", status_code=http.HTTPStatus.ACCEPTED)
@api
@verify
def create_user(to_return, creds, info):
    system = ms.MordoorSystem(creds)
    try:
        to_return = system.create_user(info["first"], info["last"], info["r"], info["uname"], info["pwd"])
    except Exception as e:
        return str(e)
    return to_return


@app.post("/admin/add_door", status_code=http.HTTPStatus.ACCEPTED)
@api
@verify
def create_user(to_return, creds, info):
    system = ms.MordoorSystem(creds)
    try:
        return system.add_door(info["d"])
    except Exception as e:
        return str(e)


@app.post("/admin/create_dept", status_code=http.HTTPStatus.ACCEPTED)
@api
@verify
def create_dept(to_return, creds, info):
    system = ms.MordoorSystem(creds)
    try:
        to_return = system.create_dept(info["name"])
    except Exception as e:
        return str(e)
    return to_return


@app.delete("/admin/remove_door", status_code=http.HTTPStatus.ACCEPTED)
@api
@verify
def remove_door(to_return, creds, info):
    system = ms.MordoorSystem(creds)
    try:
        to_return = system.remove_door(info["id"])
    except Exception as e:
        return str(e)
    return to_return


@app.delete("/admin/remove_dept", status_code=http.HTTPStatus.ACCEPTED)
@api
@verify
def remove_dept(to_return, creds, info):
    system = ms.MordoorSystem(creds)
    try:
        to_return = system.remove_dept(info["id"])
    except Exception as e:
        return str(e)
    return to_return


@app.delete("/admin/remove_user", status_code=http.HTTPStatus.ACCEPTED)
@api
@verify
def remove_user(to_return, creds, info):
    system = ms.MordoorSystem(creds)
    try:
        to_return = system.remove_user(info["id"])
    except Exception as e:
        return str(e)
    return to_return


@app.post("/admin/add_door_to_elevated", status_code=http.HTTPStatus.ACCEPTED)
@api
@verify
def add_door_to_elevated(to_return, creds, info):
    system = ms.MordoorSystem(creds)
    try:
        to_return = system.add_door_to_elevated(info["did"], info["uid"])
    except Exception as e:
        return str(e)
    return to_return

@app.post("/admin/add_dept_to_user", status_code=http.HTTPStatus.ACCEPTED)
@api
@verify
def add_dept_to_user(to_return, creds, info):
    system = ms.MordoorSystem(creds)
    try:
        to_return = system.add_dept_to_user(info["did"], info["uid"])
    except Exception as e:
        return str(e)
    return to_return

@app.post("/admin/add_dept_to_door", status_code=http.HTTPStatus.ACCEPTED)
@api
@verify
def add_dept_to_door(to_return, creds, info):
    system = ms.MordoorSystem(creds)
    try:
        to_return = system.add_dept_to_door(info["dept"], info["door"])
    except Exception as e:
        return str(e)
    return to_return

@app.post("/user/open_door", status_code=http.HTTPStatus.ACCEPTED)
@api
@verify
def open_door(to_return, creds, info):
    system = ms.MordoorSystem(creds)
    try:
        to_return = system.open_door(info["door"])
    except Exception as e:
        return str(e)
    return to_return

def main():
    uvicorn.run("MordoorDriver:app", host=ip)


if __name__ == "__main__":
    main()

    # try:
    #     system.open_door(4)
    # except Exception as e:
    #     sys.exit(e)

    # try:
    #     system.view_logs()
    # except Exception as e:
    #     sys.exit(e)
