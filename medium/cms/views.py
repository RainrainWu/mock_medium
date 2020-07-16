from django.http import JsonResponse

def index(request):
    return JsonResponse({"msg": "the index of cms"})

def users(request):
    msg = "users resource"
    return JsonResponse({"msg": msg})

def user(request, user_id):
    msg = "user resource of {USER_ID}".format(
        USER_ID=user_id
    )
    return JsonResponse({"msg": msg})

def stories(request):
    msg = "stories resource"
    return JsonResponse({"msg": msg})

def story(request, story_id):
    msg = "story resource of {STORY_ID}".format(
        STORY_ID=story_id
    )
    return JsonResponse({"msg": msg})

def publications(request):
    msg = "publications resource"
    return JsonResponse({"msg": msg})

def publication(request, publication_id):
    msg = "publication resource of {PUBLICATION_ID}".format(
        PUBLICATION_ID=publication_id
    )
    return JsonResponse({"msg": msg})
