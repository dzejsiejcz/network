
from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"),
    path("likes/<int:post>", views.likes, name="likes"),
    path("liking/<int:post>", views.liking, name="liking"),
    path("liked/<int:post>", views.liked, name="liked"),
    path("post/<str:method>/<int:post>", views.post, name="post"),
    path("user-page/<int:user>", views.user_page, name="user-page"),
    path("following/<str:method>/<int:friend>", views.following, name="following"),
]
