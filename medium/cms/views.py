import json

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from . import models
from . import resp


def index(request):
    return JsonResponse({"msg": "the index of cms"})


class Users(View):

    def get(self, request, *args, **kwargs):
        users = models.User.objects.all()
        users = [model_to_dict(x, fields=["name", "introduction"]) for x in users]
        payload = resp.generate_collection(collection=users)
        return JsonResponse(payload, status=200)

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        users = models.User.objects.filter(name=json_data["name"])
        if users.count() != 0:
            payload = resp.generate_error(
                code=409,
                message="user already exist"
            )
            return JsonResponse(payload, status=409)
        
        user = models.User(
            name=json_data["name"],
            introduction=json_data["introduction"]
        )
        user.save()
        payload = resp.generate_acknowledge(
            code=201,
            message="user created",
            data=model_to_dict(user)
        )
        return JsonResponse(payload, status=201)


class User(View):

    def get(self, request, *args, **kwargs):
        try:
            user = models.User.objects.get(name=self.kwargs["user_id"])
            payload = resp.generate_acknowledge(
                data=model_to_dict(user)
            )
            return JsonResponse(payload, status=200)
        except models.User.DoesNotExist as err:
            payload = resp.generate_error(
                code=404,
                message=str(err),
            )
            return JsonResponse(payload, status=404)

    def put(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        try:
            user = models.User.objects.get(
                name=self.kwargs["user_id"]
            )
            for key in json_data:
                if not hasattr(user, key):
                    raise AttributeError(key)
                setattr(user, key, json_data[key])
            user.save()
            payload = resp.generate_acknowledge(
                message="resource updated",
                data=model_to_dict(user)
            )
            return JsonResponse(payload, status=200)
        except AttributeError as err:
            payload = resp.generate_error(
                code=400,
                message="user does not has attribute \"{ATTRIBUTE}\"".format(
                    ATTRIBUTE=str(err)
                ),
            )
            return JsonResponse(payload, status=400)
        except models.User.DoesNotExist:
            payload = resp.generate_error(
                code=404,
                message="user not found",
            )
            return JsonResponse(payload, status=404)

    def delete(self, request, *args, **kwargs):
        try:
            models.User.objects.get(name=self.kwargs["user_id"]).delete()
            payload = resp.generate_acknowledge(
                message="user deleted"
            )
            return JsonResponse(payload, status=200)
        except models.User.DoesNotExist:
            payload = resp.generate_error(
                code=404,
                message="user not found",
            )
            return JsonResponse(payload, status=404)


class FollowingUsers(View):

    def get(self, request, *args, **kwargs):
        user = models.User.objects.get(name=self.kwargs["user_id"])
        followings = models.FollowingUser.objects.filter(from_user=user).values(
            "from_user__name",
            "to_user__name"
        )
        payload = resp.generate_collection(collection=list(followings))
        return JsonResponse(payload, status=200)
    

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)

        try:
            from_user = models.User.objects.get(name=self.kwargs["user_id"])
            print(from_user)
            to_user = models.User.objects.get(name=json_data["to_user"])
            followings = models.FollowingUser.objects.filter(
                from_user=from_user,
                to_user=to_user
            )
            if followings.count() != 0:
                payload = resp.generate_error(
                    code=409,
                    message="user already followed"
                )
                return JsonResponse(payload, status=409)
            
            from_user.following_users.add(to_user)
            payload = resp.generate_acknowledge(
                code=201,
                message="user followed",
                data=model_to_dict(from_user, fields=["name", "introduction"])
            )
            return JsonResponse(payload, status=201)
        except models.User.DoesNotExist:
            payload = resp.generate_error(
                code=404,
                message="user not found",
            )
            return JsonResponse(payload, status=404)

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
