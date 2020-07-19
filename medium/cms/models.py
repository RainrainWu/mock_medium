from django.db import models

# Create your models here.

class User(models.Model):

    name = models.CharField(max_length=40)
    introduction = models.CharField(max_length=200)
    following_users = models.ManyToManyField(
        "self",
        through="FollowingUser",
        symmetrical=False,
        related_name="following_user"
    )
    following_publications = models.ManyToManyField(
        "Publication",
        through="FollowingPublication",
        symmetrical=False,
        related_name="following_publication"
    )


class FollowingUser(models.Model):

    from_user = models.ForeignKey("User", related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey("User", related_name="to_user", on_delete=models.CASCADE)


class FollowingPublication(models.Model):

    user = models.ForeignKey("User", related_name="user", on_delete=models.CASCADE)
    publication = models.ForeignKey("Publication", related_name="publication", on_delete=models.CASCADE)


class Publication(models.Model):

    name = models.CharField(max_length=40)
    introduction = models.CharField(max_length=200)
    owner = models.ForeignKey("User", on_delete=models.CASCADE)
    members = models.ManyToManyField(
        "User",
        through="PublicationMember",
        symmetrical=False,
        related_name="editors"
    )


class PublicationMember(models.Model):

    publication = models.ForeignKey("Publication", related_name="publication_editor", on_delete=models.CASCADE)
    user = models.ForeignKey("User", related_name="editor", on_delete=models.CASCADE)
    level = models.CharField(max_length=32)

# class Story(models.Model):
    
#     title = models.CharField(max_length=40)
#     content = models.CharField(max_length=2000)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
