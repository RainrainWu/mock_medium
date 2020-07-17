def generate_error(*, code: int = 400, message: str = ""):

    payload = {
        "status": {
            "status_code": code,
            "message": message,
        }
    }
    return payload

def generate_collection(*, code: int = 200, message: str = "", collection: list = [], links: list = []):

    payload = {
        "status": {
            "status_code": code,
            "message": message,
        },
        "collection": collection,
        "links": links
    }
    return payload

def generate_acknowledge(*, code: int = 200, message: str = "", data: object = {}, links: list = []):

    payload = {
        "status": {
            "status_code": code,
            "message": message,
        },
        "data": data,
        "links": links
    }
    return payload