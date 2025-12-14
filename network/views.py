from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

from .models import User, Post, Follow, Like


def index(request):
    all_posts = Post.objects.all().order_by('id').reverse()

    paginator = Paginator(all_posts, 10)
    page_no = request.GET.get('page')
    potp = paginator.get_page(page_no)
    
    all_likes = Like.objects.all()
    liked_users = []

    try:
        for like in all_likes:
            if like.user.id == request.user.id:
                liked_users.append(like.post.id)
    except:
        liked_users = []

    return render(request, "network/index.html" ,{"all_posts":all_posts,"potp":potp, "liked_users":liked_users})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "note": "Invalid username and/or password."
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
                "note": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "note": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def createPost(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    

def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    all_posts = Post.objects.filter(user=user).order_by('id').reverse() 

    following = Follow.objects.filter(user=user)
    follower = Follow.objects.filter(user_follower=user)
    
    try:
        checkfollow = follower.filter(user=User.objects.get(pk=request.user.id))
        if len(checkfollow) != 0:
            is_following = True
        else:
            is_following = False
    except:
        is_following = False

    paginator = Paginator(all_posts, 10)
    page_no = request.GET.get('page')
    potp = paginator.get_page(page_no)

    return render(request, "network/profile.html" ,{"all_posts":all_posts,"potp":potp, "userName":user.username, "follower":follower, "following":following,"is_following":is_following, "user_profile":user})


def followOption(request):
    current_user = User.objects.get(pk=request.user.id)
    follow_input = request.POST['follow_input']
    follower_data = User.objects.get(username=follow_input)
    follower = Follow(user=current_user, user_follower=follower_data)
    follower.save()

    user_id = follower_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))

def unfollowOption(request):
    current_user = User.objects.get(pk=request.user.id)
    follow_input = request.POST['follow_input']
    follower_data = User.objects.get(username=follow_input)
    follower = Follow.objects.get(user=current_user, user_follower=follower_data)
    follower.delete()

    user_id = follower_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))

def following(request):
    current_user = User.objects.get(pk=request.user.id)
    followers = Follow.objects.filter(user=current_user)
    all_posts = Post.objects.all().order_by('id').reverse()
    followingPosts = [] 
     
    for post in all_posts:
        for follower in followers:
            if follower.user_follower == post.user:
                followingPosts.append(post)
    
    paginator = Paginator(followingPosts, 10)
    page_no = request.GET.get('page')
    potp = paginator.get_page(page_no)

    all_likes = Like.objects.all()
    liked_users = []

    try:
        for like in all_likes:
            if like.user.id == request.user.id:
                liked_users.append(like.post.id)
            
    except:
        liked_users = []

    return render(request, "network/following.html" ,{"potp":potp, "liked_users":liked_users})


def editPost(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.content = data['content']
        edit_post.save()
        return JsonResponse({"note": "Post edited successfully","data":data['content']})


def addingLike(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    
    if Like.objects.filter(user=user, post=post).exists():
        count = post.likes_count
        data = {"liked":"Like", "count":count}
        return JsonResponse(data)   
         
    newLike = Like(user = user, post = post)
    newLike.save()

    post.likes_count += 1 
    post.save()

    count = post.likes_count
    data = {"isLiked":"Like", "count":count}
    return JsonResponse(data)


def removingLike(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.filter(user=user, post=post)
 
    if like:
        like.delete() 
        post.likes_count -= 1
        post.save()
    else:
        pass

    count = post.likes_count
    data = {"isLiked":"Unlike", "count":count}
    return JsonResponse(data)

