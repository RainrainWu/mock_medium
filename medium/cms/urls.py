from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # users resources
    path("v1/users/", views.Users.as_view(), name="users"),
    path("v1/users/<str:user_id>/", views.User.as_view(), name="user"),
    path("v1/users/<str:user_id>/followingusers/", views.FollowingUsers.as_view(), name="following_users"),
    path("v1/users/<str:user_id>/followingusers/<str:to_user>", views.FollowingUser.as_view(), name="following_user"),

    # publictions
    path("v1/publications/", views.Publications.as_view(), name="publications"),
    path("v1/publications/<str:pub_id>/", views.Publication.as_view(), name="publication"),
    path("v1/publications/<str:pub_id>/members/", views.PublicationMembers.as_view(), name="publication_members"),
    path("v1/publications/<str:pub_id>/members/<str:user_id>/", views.PublicationMember.as_view(), name="publication_member"),

    # stories resources
    path("v1/stories/", views.stories, name="stories"),
    path("v1/stories/<str:story_id>/", views.story, name="story"),
]