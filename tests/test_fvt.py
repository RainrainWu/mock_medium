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

def get_publication_members(pub_id: str="", level: str="") -> object:
    if level == "":
        resp = requests.get(
            "http://localhost:8000/cms/v1/publications/{PUB_ID}/members/".format(
                PUB_ID=pub_id
            )
        )
    else:
        resp = requests.get(
            "http://localhost:8000/cms/v1/publications/{PUB_ID}/members/?level={LEVEL}".format(
                PUB_ID=pub_id,
                LEVEL=level
            )
        )
    print(resp.json())
    return resp

def add_publication_member(pub_id: str="", user_id: str="", level: str="") -> object:
    payload = {"user_id": user_id, "level": level}
    resp = requests.post(
        "http://localhost:8000/cms/v1/publications/{PUB_ID}/members/".format(
            PUB_ID=pub_id
        ),
        json=payload
    )
    print(resp.json())
    return resp

def get_publication_member(pub_id: str="", user_id: str="") -> object:
    resp = requests.get(
        "http://localhost:8000/cms/v1/publications/{PUB_ID}/members/{USER_ID}/".format(
            PUB_ID=pub_id,
            USER_ID=user_id
        )
    )
    print(resp.json())
    return resp

def update_publication_member(pub_id: str="", user_id: str="", level: str="") -> object:
    payload = {"level": level}
    resp = requests.put(
        "http://localhost:8000/cms/v1/publications/{PUB_ID}/members/{USER_ID}/".format(
            PUB_ID=pub_id,
            USER_ID=user_id
        ),
        json=payload
    )
    print(resp.json())
    return resp

def delete_publication_member(pub_id: str="", user_id: str="") -> object:
    resp = requests.delete(
        "http://localhost:8000/cms/v1/publications/{PUB_ID}/members/{USER_ID}/".format(
            PUB_ID=pub_id,
            USER_ID=user_id
        )
    )
    print(resp.json())
    return resp

def get_stories(pub_id: str="", tag: str="") -> object:
    if pub_id == "" and tag == "":
        resp = requests.get("http://localhost:8000/cms/v1/stories/")
    else:
        query_list = []
        if pub_id != "":
            query_list += ["pub_id=" + pub_id]
        if tag != "":
            query_list += ["tag=" + tag]
        query_str = "?" + "&".join(query_list)
        resp = requests.get(
            "http://localhost:8000/cms/v1/stories/{QUERY_STR}".format(
                QUERY_STR=query_str
            )
        )
    print(resp.json())
    return resp

def add_stories(title: str="", content: str="", author: str="", pub_id: str="", tag: list=[]) -> object:
    payload = {
        "title": title,
        "content": content,
        "user_id": author,
        "pub_id": pub_id,
        "tag": tag
    }
    resp = requests.post(
        "http://localhost:8000/cms/v1/stories/",
        json=payload
    )
    print(resp.json())
    return resp

def get_story(story_id: str="") -> object:
    resp = requests.get(
        "http://localhost:8000/cms/v1/stories/{STORY_ID}/".format(
            STORY_ID=story_id
        )
    )
    print(resp.json())
    return resp

# get_stories()
# add_stories("Title2", "Content2", "Rain2", "journal")
get_story("Title2")
