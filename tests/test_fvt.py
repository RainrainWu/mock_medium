import requests

def get_users() -> object:
    resp = requests.get(
        "http://localhost:8000/cms/v1/users/"
    )
    print(resp.json())
    return resp

def add_user(user_id: str="", intro: str="") -> object:
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

def get_following(user_id: str="") -> object:
    resp = requests.get(
        "http://localhost:8000/cms/v1/users/{USER_ID}/followingusers/".format(
            USER_ID=user_id
        )
    )
    print(resp.json())
    return resp

def add_following(user_id: str="", to_user: str="") -> object:
    payload = {"to_user": to_user}
    resp = requests.post(
        "http://localhost:8000/cms/v1/users/{USER_ID}/followingusers/".format(
            USER_ID=user_id
        ),
        json=payload
    )
    print(resp.json())
    return resp

def get_following_user(user_id: str="", to_user: str="") -> object:
    resp = requests.get(
        "http://localhost:8000/cms/v1/users/{USER_ID}/followingusers/{TO_USER}".format(
            USER_ID=user_id,
            TO_USER=to_user
        )
    )
    print(resp.json())
    return resp

def delete_following_user(user_id: str="", to_user: str="") -> object:
    resp = requests.delete(
        "http://localhost:8000/cms/v1/users/{USER_ID}/followingusers/{TO_USER}".format(
            USER_ID=user_id,
            TO_USER=to_user
        )
    )
    print(resp.json())
    return resp

def get_publications() -> object:
    resp = requests.get(
        "http://localhost:8000/cms/v1/publications/"
    )
    print(resp.json())
    return resp

def add_publication(name: str="", intro: str="", owner: str="") -> object:
    payload = {"name": name, "introduction": intro, "owner": owner}
    resp = requests.post(
        "http://localhost:8000/cms/v1/publications/",
        json=payload
    )
    print(resp.json())
    return resp

def get_publication(pub_id: str="") -> object:
    resp = requests.get(
        "http://localhost:8000/cms/v1/publications/{PUB_ID}/".format(
            PUB_ID=pub_id
        )
    )
    print(resp.json())
    return resp

def update_publication(pub_id: str="", payload: object={}) -> object:
    resp = requests.put(
        "http://localhost:8000/cms/v1/publications/{PUB_ID}/".format(
            PUB_ID=pub_id
        ),
        json=payload
    )
    print(resp.json())
    return resp

def delete_publication(pub_id: str="") -> object:
    resp = requests.delete(
        "http://localhost:8000/cms/v1/publications/{PUB_ID}/".format(
            PUB_ID=pub_id
        )
    )
    print(resp.json())
    return resp

def get_publication_members(pub_id: str="") -> object:
    resp = requests.get(
        "http://localhost:8000/cms/v1/publications/{PUB_ID}/members/?level={LEVEL}".format(
            PUB_ID=pub_id,
            LEVEL="editor"
        )
    )
    print(resp.json())
    return resp

def add_publication_members(pub_id: str="", user_id: str="", level: str="") -> object:
    payload = {"user_id": user_id, "level": level}
    resp = requests.post(
        "http://localhost:8000/cms/v1/publications/{PUB_ID}/members/".format(
            PUB_ID=pub_id
        ),
        json=payload
    )
    print(resp.json())
    return resp

get_publications()
get_publication_members("journal")
add_publication_members("journal", "Rain2", "editor")
get_publication_members("journal")
