from django.db import models

# Create your models here.

class User(models.Model):

    name = models.CharField(max_length=40)
    introduction = models.CharField(max_length=200)
    following_users = models.ManyToManyField(
        "self",
        through="UserFollowing",
        symmetrical=False,
        related_name="following"
    )


class UserFollowing(models.Model):

    from_user = models.ForeignKey(User, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)


class Publication(models.Model):

    name = models.CharField(max_length=40)
    introduction = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    editors = models.ManyToManyField(
        User,
        through="PublicationEditor",
        symmetrical=False,
        related_name="editors"
    )
    writers = models.ManyToManyField(
        User,
        through="PublicationWriter",
        symmetrical=False,
        related_name="writers"
    )


class PublicationEditor(models.Model):

    user = models.ForeignKey(User, related_name="editor", on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, related_name="publication_editor", on_delete=models.CASCADE)


class PublicationWriter(models.Model):

    user = models.ForeignKey(User, related_name="writer", on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, related_name="publication_writer", on_delete=models.CASCADE)


# class Story(models.Model):
    
#     title = models.CharField(max_length=40)
#     content = models.CharField(max_length=2000)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
