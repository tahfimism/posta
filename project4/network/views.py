from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

import json

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import User, Post


def index(request):

    # get all posts
    all_posts = Post.objects.all().order_by("-timestamp")

    # paginator setup
    paginator = Paginator(all_posts, 10)  #10 post per page
    page_number = request.GET.get('page', 1) 
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "index_title" : "All Posts",
        "posts": page_obj,
    })




@login_required
def following_posts(request):
    following_posts = Post.objects.filter(user__in=request.user.following.all()).order_by("-timestamp")
    
    # paginator setup
    paginator = Paginator(following_posts, 10)  #10 post per page
    page_number = request.GET.get('page', 1) 
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "index_title" : "Following Posts",
        "posts": page_obj,
    })



def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "network/profile.html", {
            "error": "User not found."
        })

    user_posts = Post.objects.filter(user=user).order_by("-timestamp")

    # Is the logged-in user following this profile user?
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = user.followers.filter(id=request.user.id).exists()

    # paginator setup
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "user": user,
        "posts": page_obj,
        "is_following": is_following,
    })



@login_required
@csrf_exempt
def new_post(request):
    if request.method == "POST":
        # Get the content of the post from the request body
        data = json.loads(request.body)
        content = data.get("content", "").strip()

        # Ensure content is not empty
        if not content:
            return JsonResponse({"error": "Post content cannot be empty."}, status=400)

        # Create a new post
        post = Post.objects.create(
            user=request.user,
            content=content
        )
        return JsonResponse({"message": "Post created successfully!", "id": post.id}, status=201)

    return JsonResponse({"error": "POST request required."}, status=400)


@csrf_exempt
@login_required
def follow_user(request, user_id):
    if request.method == "PUT":
        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)

        # Toggle follow status
        if request.user in user_to_follow.followers.all():
            user_to_follow.followers.remove(request.user)
            message = "unfollowed"
        else:
            user_to_follow.followers.add(request.user)
            message = "followed"

        user_to_follow.save()
        return JsonResponse({"message": f"You have {message} {user_to_follow.username}.",
                                "following":True if message == "followed" else False }, status=200)

    return JsonResponse({"error": "POST request required."}, status=400)





def post_detail(request, post_id):
    pass



@csrf_exempt
@login_required
def like_post(request, post_id):
    if request.method == "PUT":
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)

        # Toggle like status
        if request.user in post.liked_by.all():
            post.liked_by.remove(request.user)
            post.like_count -= 1
        else:
            post.liked_by.add(request.user)
            post.like_count += 1

        post.save()
        return JsonResponse({"message": "Like status updated.", "like_count": post.like_count}, status=200)
    return JsonResponse({"error": "PUT request required."}, status=400)
    pass



def load_posts(request, filter="all"):
    # This function should return a list of posts in JSON format
    if filter not in ["all", "following"]:
        return JsonResponse({"error": "Invalid filter."}, status=400)

    # If filter is "following", get posts from users the current user follows
    if filter == "following":
        posts = Post.objects.filter(user__in=request.user.following.all()).order_by("-timestamp")
    else:
        posts = Post.objects.all().order_by("-timestamp")
    posts_data = []
    for post in posts:
        posts_data.append({
            "id": post.id,
            "user": post.user.username,
            "content": post.content,
            "timestamp": post.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "like_count": post.like_count,

        })

    return JsonResponse(posts_data, safe=False, json_dumps_params={"indent": 2}, status=200)



@login_required
@csrf_exempt
def edit_post(request, post_id):
    if request.method == "PUT":
        try:
            post = Post.objects.get(id=post_id, user=request.user)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found "}, status=404)

        # Get the new content from the request body
        data = json.loads(request.body)
        new_content = data.get("content", "").strip()

        # Ensure content is not empty
        if not new_content.strip():
            return JsonResponse({"error": "Post content cannot be empty."}, status=400)

        # Update the post content
        post.content = new_content
        post.save()
        
        return JsonResponse({"message": "Post updated successfully!", "id": post.id}, status=200)

    return JsonResponse({"error": "PUT request required."}, status=400)

def delete_post(request, post_id):
    pass






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
