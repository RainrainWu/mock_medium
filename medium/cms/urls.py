from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # users resources
    path("v1/users/", views.Users.as_view(), name="users"),
    path("v1/users/<str:user_id>/", views.User.as_view(), name="user"),
    path("v1/users/<str:user_id>/followingusers/", views.FollowingUsers.as_view(), name="followingusers"),

    # publictions
    path("v1/publications/", views.publications, name="publications"),
    path("v1/publications/<str:publication_id>/", views.publication, name="publication"),

    # stories resources
    path("v1/stories/", views.stories, name="stories"),
    path("v1/stories/<str:story_id>/", views.story, name="story"),
]