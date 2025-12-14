
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createPost", views.createPost, name="createPost"),
    path("profile/<int:user_id>",views.profile,name="profile"),
    path("followOption", views.followOption, name="followOption"),
    path("unfollowOption", views.unfollowOption, name="unfollowOption"),
    path("following", views.following, name="following"),
    path("editPost/<int:post_id>", views.editPost, name="editPost"),
    path("addingLike/<int:post_id>", views.addingLike, name="addingLike"),
    path("removingLike/<int:post_id>", views.removingLike, name="removingLike"),
]
