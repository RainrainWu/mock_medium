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
            payload = resp.generate_error(code=409, message="user already exist")
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
            payload = resp.generate_acknowledge(data=model_to_dict(user))
            return JsonResponse(payload, status=200)
        
        except models.User.DoesNotExist:
            payload = resp.generate_error(code=404, message="user not found")
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
                message="invalid attribute \"{ATTRIBUTE}\"".format(
                    ATTRIBUTE=str(err)
                ),
            )
            return JsonResponse(payload, status=400)
        
        except models.User.DoesNotExist:
            payload = resp.generate_error(code=404, message="user not found")
            return JsonResponse(payload, status=404)

    def delete(self, request, *args, **kwargs):

        try:
            models.User.objects.get(name=self.kwargs["user_id"]).delete()
            payload = resp.generate_acknowledge(
                message="user deleted"
            )
            return JsonResponse(payload, status=200)
        
        except models.User.DoesNotExist:
            payload = resp.generate_error(code=404, message="user not found")
            return JsonResponse(payload, status=404)


class FollowingUsers(View):

    def get(self, request, *args, **kwargs):

        try:
            user = models.User.objects.get(name=self.kwargs["user_id"])
            followings = models.FollowingUser.objects.filter(from_user=user).values(
                "from_user__name",
                "to_user__name"
            )
            payload = resp.generate_collection(collection=list(followings))
            return JsonResponse(payload, status=200)
        
        except models.User.DoesNotExist:
            payload = resp.generate_error(code=404, message="user not found")
            return JsonResponse(payload, status=404)

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)

        try:
            from_user = models.User.objects.get(name=self.kwargs["user_id"])
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


class FollowingUser(View):

    def get(self, request, *args, **kwargs):

        try:
            from_user = models.User.objects.get(name=self.kwargs["user_id"])
            to_user = models.User.objects.get(name=self.kwargs["to_user"])
            followings = models.FollowingUser.objects.filter(
                from_user=from_user,
                to_user=to_user
            ).values(
                "from_user__name",
                "to_user__name"
            )
            payload = resp.generate_acknowledge(data=list(followings)[0])
            return JsonResponse(payload, status=200)

        except models.User.DoesNotExist:
            payload = resp.generate_error(code=404, message="user not found")
            return JsonResponse(payload, status=404)
        
        except IndexError:
            payload = resp.generate_error(code=404, message="user not followed")
            return JsonResponse(payload, status=404)

    def delete(self, request, *args, **kwargs):

        try:
            from_user = models.User.objects.get(name=self.kwargs["user_id"])
            to_user = models.User.objects.get(name=self.kwargs["to_user"])
            from_user.following_users.remove(to_user)
            payload = resp.generate_acknowledge(message="user unfollowed")
            return JsonResponse(payload, status=200)
        
        except models.User.DoesNotExist:
            payload = resp.generate_error(code=404, message="user not found")
            return JsonResponse(payload, status=404)


class Publications(View):

    def get(self, request, *args, **kwargs):
        pubs = models.Publication.objects.all()
        pubs = [model_to_dict(x, fields=["name", "introduction"]) for x in pubs]
        payload = resp.generate_collection(collection=pubs)
        return JsonResponse(payload, status=200)

    def post(self, request, *args, **kwargs):
        try:
            json_data = json.loads(request.body)
            pubs = models.Publication.objects.filter(name=json_data["name"])
            if pubs.count() != 0:
                payload = resp.generate_error(code=409, message="publication already exist")
                return JsonResponse(payload, status=409)
            
            user = models.User.objects.get(name=json_data["owner"])
            pub = models.Publication(
                name=json_data["name"],
                introduction=json_data["introduction"],
                owner=user
            )
            pub.save()
            payload = resp.generate_acknowledge(
                code=201,
                message="publication created",
                data=model_to_dict(pub)
            )
            return JsonResponse(payload, status=201)

        except models.User.DoesNotExist:
            payload = resp.generate_error(code=404, message="user not found")
            return JsonResponse(payload, status=404)


class Publication(View):

    def get(self, request, *args, **kwargs):
        try:
            pub = models.Publication.objects.get(name=self.kwargs["pub_id"])
            payload = resp.generate_acknowledge(data=model_to_dict(pub))
            return JsonResponse(payload, status=200)
        
        except models.Publication.DoesNotExist:
            payload = resp.generate_error(code=404, message="publication not found")
            return JsonResponse(payload, status=404)

    def put(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        try:
            pub = models.Publication.objects.get(name=self.kwargs["pub_id"])
            for key in json_data:
                if key not in ["introduction"]:
                    raise AttributeError(key)
                setattr(pub, key, json_data[key])
            pub.save()
            payload = resp.generate_acknowledge(
                message="publication updated",
                data=model_to_dict(pub)
            )
            return JsonResponse(payload, status=200)
        
        except AttributeError as err:
            payload = resp.generate_error(
                code=400,
                message="invalid attribute \"{ATTRIBUTE}\"".format(
                    ATTRIBUTE=str(err)
                ),
            )
            return JsonResponse(payload, status=400)
        
        except models.Publication.DoesNotExist:
            payload = resp.generate_error(code=404, message="publication not found")
            return JsonResponse(payload, status=404)

    def delete(self, request, *args, **kwargs):
        try:
            models.Publication.objects.get(name=self.kwargs["pub_id"]).delete()
            payload = resp.generate_acknowledge(
                message="publication deleted"
            )
            return JsonResponse(payload, status=200)
        
        except models.Publication.DoesNotExist:
            payload = resp.generate_error(code=404, message="publicaiton not found")
            return JsonResponse(payload, status=404)


class PublicationMembers(View):

    def get(self, request, *args, **kwargs):
        try:
            pub = models.Publication.objects.get(name=self.kwargs["pub_id"])
            level = request.GET.get("level")
            if level is not None:
                members = models.PublicationMember.objects.filter(
                    publication=pub,
                    level=level
                ).values(
                    "user__name",
                    "level"
                )
            else:
                members = models.PublicationMember.objects.filter(
                    publication=pub
                ).values(
                    "user__name",
                    "level"
                )
            payload = resp.generate_collection(collection=list(members))
            return JsonResponse(payload, status=200)

        except models.Publication.DoesNotExist:
            payload = resp.generate_error(code=404, message="publication not found")
            return JsonResponse(payload, status=404)

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)

        try:
            pub = models.Publication.objects.get(name=self.kwargs["pub_id"])
            user = models.User.objects.get(name=json_data["user_id"])
            members = models.PublicationMember.objects.filter(
                publication=pub,
                user=user
            )
            if members.count() != 0:
                payload = resp.generate_error(
                    code=409,
                    message="user already register as " + list(members)[0].level
                )
                return JsonResponse(payload, status=409)

            member = models.PublicationMember(
                publication=pub,
                user=user,
                level=json_data["level"]
            )
            member.save()
            payload = resp.generate_acknowledge(
                code=201,
                message="user registered",
                data=model_to_dict(member, fields=["name", "introduction"])
            )
            return JsonResponse(payload, status=201)

        except models.Publication.DoesNotExist:
            payload = resp.generate_error(code=404, message="publication not found")
            return JsonResponse(payload, status=404)

        except models.User.DoesNotExist:
            payload = resp.generate_error(code=404, message="user not found")
            return JsonResponse(payload, status=404)


class PublicationMember(View):

    def get(self, request, *args, **kwargs):
        try:
            pub = models.Publication.objects.get(name=self.kwargs["pub_id"])
            user = models.User.objects.get(name=self.kwargs["user_id"])
            members = models.PublicationMember.objects.filter(
                publication=pub,
                user=user
            ).values(
                "publication__name",
                "user__name",
                "level"
            )
            if members.count() == 0:
                payload = resp.generate_error(code=404, message="user not a member")
                return JsonResponse(payload, status=404)

            payload = resp.generate_acknowledge(data=list(members)[0])
            return JsonResponse(payload, status=200)

        except models.Publication.DoesNotExist:
            payload = resp.generate_error(code=404, message="publication not found")
            return JsonResponse(payload, status=404)

        except models.User.DoesNotExist:
            payload = resp.generate_error(code=404, message="user not found")
            return JsonResponse(payload, status=404)
    
    def put(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        try:
            pub = models.Publication.objects.get(name=self.kwargs["pub_id"])
            user = models.User.objects.get(name=self.kwargs["user_id"])
            member = models.PublicationMember.objects.get(
                publication=pub,
                user=user
            )
            for key in json_data:
                if key not in ["level"]:
                    raise AttributeError(key)
                setattr(member, key, json_data[key])
            member.save()
            payload = resp.generate_acknowledge(
                message="publication member updated",
                data=model_to_dict(member)
            )
            return JsonResponse(payload, status=200)
        
        except AttributeError as err:
            payload = resp.generate_error(
                code=400,
                message="invalid attribute \"{ATTRIBUTE}\"".format(
                    ATTRIBUTE=str(err)
                ),
            )
            return JsonResponse(payload, status=400)
        
        except models.Publication.DoesNotExist:
            payload = resp.generate_error(code=404, message="publication not found")
            return JsonResponse(payload, status=404)

        except models.User.DoesNotExist:
            payload = resp.generate_error(code=404, message="user not found")
            return JsonResponse(payload, status=404)

    def delete(self, request, *args, **kwargs):
        try:
            pub = models.Publication.objects.get(name=self.kwargs["pub_id"])
            user = models.User.objects.get(name=self.kwargs["user_id"])
            models.PublicationMember.objects.get(
                publication=pub,
                user=user
            ).delete()
            payload = resp.generate_acknowledge(
                message="publication member deleted"
            )
            return JsonResponse(payload, status=200)
        
        except models.PublicationMember.DoesNotExist:
            payload = resp.generate_error(code=404, message="publicaiton member not found")
            return JsonResponse(payload, status=404)


class Stories(View):

    def get(self, request, *args, **kwargs):
        try:
            stories = models.Story.objects.all()
            pub = request.GET.get("publication")
            if pub is not None:
                stories = stories.filter(publication=pub)
            tag = request.GET.get("tag")
            if tag is not None:
                stories = stories.filter(tag=tag)
            stories = stories.values(
                "title", "content", "author__name", "publication__name"
            )
            payload = resp.generate_collection(collection=list(stories))
            return JsonResponse(payload, status=200)

        except models.Story.DoesNotExist:
            payload = resp.generate_error(code=404, message="story not found")
            return JsonResponse(payload, status=404)

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)

        try:
            user = models.User.objects.get(name=json_data["user_id"])
            pub = models.Publication.objects.get(name=json_data["pub_id"])
            stories = models.Story.objects.filter(
                title=json_data["title"]
            )
            if stories.count() != 0:
                payload = resp.generate_error(
                    code=409,
                    message="story already existed"
                )
                return JsonResponse(payload, status=409)

        except models.Publication.DoesNotExist:
            payload = resp.generate_error(code=404, message="publication not found")
            return JsonResponse(payload, status=404)

        except models.User.DoesNotExist:
            payload = resp.generate_error(code=404, message="user not found")
            return JsonResponse(payload, status=404)
        
        tags = []
        for x in json_data["tag"]:
            try:
                tags += [models.Tag.objects.get(name=x)]
            except models.Tag.DoesNotExist:
                tag = models.Tag(name=x)
                tag.save()
                tags += [models.Tag.objects.get(name=x)]
        story = models.Story(
            title=json_data["title"],
            content=json_data["content"],
            author=user,
            publication=pub
        )
        story.save()
        for tag in tags:
            story.tag.add(tag)
        story.save()

        stories = models.Story.objects.filter(
            title=json_data["title"],
            author=user,
            publication=pub
        ).values(
            "title", "content", "author__name", "publication__name"
        )
        payload = resp.generate_acknowledge(
            code=201,
            message="user registered",
            data=list(stories)[0]
        )
        return JsonResponse(payload, status=201)

class Story(View):

    def get(self, request, *args, **kwargs):
        try:
            stories = models.Story.objects.filter(
                title=self.kwargs["story_id"]
            ).values(
                "title",
                "content",
                "author__name",
                "publication__name"
            )
            payload = resp.generate_acknowledge(data=list(stories)[0])
            return JsonResponse(payload, status=200)

        except models.Story.DoesNotExist:
            payload = resp.generate_error(code=404, message="story not found")
            return JsonResponse(payload, status=404)
