import requests

def get_users() -> object:
    resp = requests.get(
        "http://localhost:8000/cms/v1/users/"
    )
    print(resp.json())
    return resp

def create_user(user_id: str="", intro: str="") -> object:
    payload = {"name": user_id, "introduction": intro}
    resp = requests.post(
        "http://localhost:8000/cms/v1/users/",
        json=payload
    )
    print(resp.json())
    return resp

def get_user(user_id: str="") -> object:
    resp = requests.get(
        "http://localhost:8000/cms/v1/users/{USER_ID}/".format(
            USER_ID=user_id
        )
    )
    print(resp.json())
    return resp

def update_user(user_id: str="", payload: object={}) -> object:
    resp = requests.put(
        "http://localhost:8000/cms/v1/users/{USER_ID}/".format(
            USER_ID=user_id
        ),
        json=payload
    )
    print(resp.json())
    return resp

def delete_user(user_id: str="") -> object:
    payload = {"name": user_id}
    resp = requests.delete(
        "http://localhost:8000/cms/v1/users/{USER_ID}/".format(
            USER_ID=user_id
        ),
        json=payload
    )
    print(resp.json())
    return resp


get_users()
update_user("Rain", {"introduction_text": "New intro."})
delete_user("Rain")