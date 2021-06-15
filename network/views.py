from django.contrib.auth import authenticate, login, logout
from django.core import paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

from itertools import chain

from .models import User, Post, Like, Following


def index(request):
    post_list = Post.objects.order_by('-timestamp')
    paginator = Paginator(post_list, 5) #Show 5 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "network/index.html", {'page_obj': page_obj})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)

            # redirecting after authentication
            if "next" in request.POST:
                request_args = request.POST.get("next")[1:].split('/')
                return HttpResponseRedirect(reverse(
                    request_args[0], args=(request_args[1:])
                ))

            else: 
                return HttpResponseRedirect(reverse("index"))


        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def posts(request):

    # Composing a new post must be via POST

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # save post

    data = json.loads(request.body)
    text = data.get("body", "")
    user = User.objects.get(username=request.user)


    post = Post(user=user, text=text)
    post.save()

    # return render(request, "index", {
    #     "alert": alert
    # })
 
    return JsonResponse({"message": "Post created successfully."}, status=201)


def likes(request, post):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    try:
        a = len(Like.objects.filter(post_id=post))
    except Like.DoesNotExist:
        a = 0

    return JsonResponse({"a": a})


@csrf_exempt
@login_required
def liking(request, post):
    if request.method == "GET":
        try:
            liked = Like.objects.get(user=request.user, post=Post.objects.get(pk=post))
            liked.delete()
            return JsonResponse({
                "prevliked": True,
                "post": post
            })
        except Like.DoesNotExist:
            liked = Post.objects.get(pk=post)
            l = Like(user=request.user, post=liked)
            l.save()
            return JsonResponse({
                "prevliked": False,
                "post": post
            })


@csrf_exempt
@login_required
def liked(request, post):
    if request.method == "GET":
        try:
            liked = Like.objects.get(user=request.user, post=Post.objects.get(pk=post))
            return JsonResponse({
                "liked": True,
                "post": post
            })
        except Like.DoesNotExist:
            return JsonResponse({
                "liked": False,
                "post": post
            })


@csrf_exempt
@login_required(login_url="network:login")
def post(request, method, post):
    if request.method == "GET":
        if method == "one":
            try:
                post = Post.objects.get(pk=post)
                return JsonResponse(post.serialize())

            except Post.DoesNotExist:
                return JsonResponse({"mesaage": "Post does not exist"}, status=400)
            
        elif method == "delete":
            try:
                post = Post.objects.get(pk=post)
                post.delete()
                return JsonResponse({"message": "Post deleted succesfull"}, status=204)
            except Post.DoesNotExist:
                return JsonResponse({"mesaage": "Post does not exist"}, status=400)
            

    elif request.method == "PUT" and method == "edit":
        data = json.loads(request.body)
        post = Post.objects.get(pk=post)
        post.text = data["body"]
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
@login_required(login_url="login")
def user_page(request, user):
    post_list = Post.objects.filter(user_id=user)
    post_user = post_list.order_by('-timestamp')
    user = User.objects.get(pk=user)
    paginator = Paginator(post_user, 5) #Show 5 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    followers = len(Following.objects.filter(friend_id=user))


    return render(request, "network/user.html", {
        'page_obj': page_obj,
        'author': user,
        'followers': followers
        })

@csrf_exempt
@login_required(login_url="login")
def following(request, method, friend):
    if request.method == "GET":
        user = request.user
        if method == "checking":
            follow = len(Following.objects.filter(follower = user, friend = friend))
            if follow != 0:
                return JsonResponse({
                    "has_followed": True,
                    "len": follow
                })
            else:
                return JsonResponse({
                    "has_followed": False
                })
        # if method == "number":
        #     try:
        #         all_followers = len(Following.objects.filter(friend = friend))
        #     except Following.DoesNotExist:
        #         all_followers = 0    
        #     return JsonResponse({
        #         "number": all_followers
        #     })
        if method == "follow":
            follow = Following(follower = user, friend_id = friend)
            follow.save()
            return JsonResponse({
                "has_followed": True
            })
        if method == "unfollow":
            follow = Following.objects.filter(follower = user, friend = friend)
            follow.delete()
            return JsonResponse({
                "has_followed": False
            })

        if method == "all":
            current_user = User.objects.get(pk=user.id)
            arr = []

            friends = Following.objects.filter(follower=current_user)
            for friend in friends:
                post = Post.objects.filter(user_id = friend.friend_id)
                arr.append(post)

            posts = list(chain(*arr))
    
            # postfrdate = posts.order_by('-timestamp')
            paginator = Paginator(posts, 5) #Show 5 posts per page

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, "network/index.html", {
                'page_obj': page_obj
                })

        else:
            return JsonResponse({
                "error": "Checking, follow or unfollow method required."
            }, status=400)

    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)

    

