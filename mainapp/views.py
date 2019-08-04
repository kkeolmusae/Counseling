from django.shortcuts import render, redirect
from .models import Post, Profile, Comment, Review #Blog모델을 가져와서 쓸꺼니깐 위에 적어줌
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from itertools import chain
# Create your views here.
 
    
def main(request):
    posts = Post.objects.all()
    #posts = chain(posts, (Post.objects.order_by('-created_at').all()))
    context={
        "posts":posts 
        }
    return render(request, 'main.html',context)

def profile(request, user):
    profile = Profile.objects.get(user = request.user)
    context={
        "profile":profile
        }   
    return render(request, 'profile.html', context)

def p_profile(request, post_id, user):
    post= Post.objects.get(id=post_id)
    user=User.objects.get(post = post)
    profile = Profile.objects.get(user = user)
    context={
        "profile":profile
        }   
    return render(request, 'profile.html', context)

def c_profile(request, comment_id, user):
    comment = Comment.objects.get(id=comment_id)
    user = User.objects.get(comment = comment)
    profile = Profile.objects.get(user= user)
    context={
        "profile":profile
        }
    return render(request, 'profile.html', context)

    
def write(request): #GET 은 검색을 위함, POST는 데이터를 전송하고 전송된 데이터에 대한 결과값을 돌려받기 위함
    if request.method == "GET":
        return render(request, 'write.html')
    
    elif request.method == "POST":
        post=Post()
        post.user = request.user
        post.title=request.POST['title']
        post.content=request.POST['content']
        post.category=request.POST['category']
        anonymous = request.POST.get('anonymous',False)  
        if anonymous == "1":
            post.anonymous = True
        try:
            post.image = request.FILES['image']
        except:
            pass
            
        post.save()

        return redirect('main')

def review(request):
    reviews = Review.objects.all()
    context={
        "reviews":reviews 
        }
    return render(request, 'review.html',context)


def r_write(request): # Review Wrtie
    if request.method =="GET":
        return render(request, 'r_write.html')
    elif request.method == "POST":
        review = Review()
        review.user = request.user
        review.title = request.POST['title']
        review.content = request.POST['content']
        try:
            review.image = request.FILES['image']
        except:
            pass

        review.save()
        return redirect('review')

def r_update(request, review_id):
    if request.method == "GET":
        review = Review.objects.get(id=review_id)
        context={
            "review":review
        }
        return render(request, "r_update.html", context)
    elif request.method=="POST":
        review = Review.objects.get(id =review_id)
        review.title= request.POST['title']
        review.content=request.POST['content']
        try:
            review.image= request.FILES['image']
        except:
            pass
        review.save()
        return redirect('review')

def r_delete(request,review_id):
    review = Review.objects.get(id = review_id)
    review.delete()
    return redirect('review')

def read(request,post_id):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.filter(post = post_id)
    context = {
        "post":post,
        "comment":comment,
    }
    return render(request,'read.html',context)

def update(request,post_id):
    if request.method =="GET":
        post = Post.objects.get(id=post_id)
        context={
            "post":post
            }
        return render(request, "update.html", context)
    elif request.method=="POST":
        post = Post.objects.get(id=post_id)
        post.title =request.POST['title']
        post.content =request.POST['content']
        post.category=request.POST['category']
        try:
            post.image = request.FILES['image']
        except:
            pass
        post.save()
        
        return redirect(read, post_id)

def update_profile(request,user):
    if request.method =="GET":
        profile = Profile.objects.get(user = request.user)
        context={
            "profile":profile
            }
        return render(request, "update_profile.html", context)
    elif request.method=="POST":
        profile = Profile.objects.get(user = request.user)
        profile.nickname = request.POST['nickname']
        profile.phone =request.POST['phone']
        try:
            profile.image = request.FILES['image']
        except:
            pass
        profile.save()
        return redirect(main)

def report(request, post_id):
    username = Profile.objects.get(user = request.user)
    post = Post.objects.get(id=post_id)
    user = User.objects.get(post = post)
    profile = Profile.objects.get(user = user)
    tempstr = str(username.user) + " "
    
    if tempstr in post.Report_list:
        message="이미 신고하였습니다."
    elif post.report_num == 4:
        post.Report_list+= tempstr
        post.report_num+=1
        post.blind=True
        post.save()
    else:
        post.Report_list+= tempstr
        post.report_num+=1
        post.save()
    return redirect(main)

def category(request, category):
    posts = Post.objects.all()
    name = str(category)
    category = posts.filter(category__icontains=category)
    context={
        "category":category,
        "name":name,
        }
    return render(request, 'category.html', context)





################################################################

def delete(request,post_id):
    post = Post.objects.get(id = post_id)
    post.delete()
    return redirect(main)


def c_create(request,post_id):
    if request.method == "POST":
        comment = Comment()
        comment.user = request.user
        comment.post = Post.objects.get(id = post_id)
        comment.content = request.POST['comment']
        anonymous = request.POST.get('anonymous', False)
        if anonymous == "y":
            comment.anonymous = True
        comment.save()
        return redirect(read,comment.post.id)

def c_delete(request,comment_id):
    comment = Comment.objects.get(id = comment_id)
    post_id = comment.post_id
    comment.delete()
    return redirect(read,post_id)

def setPLike(request, post_id):
    username = Profile.objects.get(user = request.user)
    post = Post.objects.get(id=post_id)
    user = User.objects.get(post = post)
    profile = Profile.objects.get(user = user)
    tempstr = str(username.user) + " "
    if tempstr in post.Post_list:
        message="이미 공감 혹은 비공감 하셨습니다."
    else:
        post.Post_list = post.Post_list + tempstr
        post.like_num+=1
        post.like_result+=1
        profile.like_num+=1
        profile.save()
        post.save()
    return redirect(read, post.id)

def setPdisLike(request, post_id):
    username = Profile.objects.get(user = request.user)
    post = Post.objects.get(id=post_id)
    user = User.objects.get(post = post)
    profile = Profile.objects.get(user = user)
    tempstr = str(username.user) + " "
    if tempstr in post.Post_list:
        message="이미 공감 혹은 비공감 하셨습니다."
    else:
        post.Post_list = post.Post_list + tempstr
        post.dislike_num+=1
        post.like_result-=1
        profile.dislike_num+=1
        profile.save()
        post.save()
    return redirect(read, post.id)


def setCLike(request, comment_id, post_id):
    username = Profile.objects.get(user = request.user)
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    user = User.objects.get(post = post)
    profile = Profile.objects.get(user = user)
    tempstr = str(username.user) + " "
    if tempstr in comment.Comment_list:
        message="이미 공감 혹은 비공감 하셨습니다."
    else:
        comment.like_num+=1
        comment.Comment_list+=tempstr
        profile.like_num+=1
        profile.save()
        comment.save()
    return redirect(read, post.id)

def setCdisLike(request, comment_id, post_id):
    username = Profile.objects.get(user = request.user)
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    user = User.objects.get(post = post)
    profile = Profile.objects.get(user = user)
    tempstr = str(username.user) + " "
    if tempstr in comment.Comment_list:
        message="이미 공감 혹은 비공감 하셨습니다."
    else:
        comment.dislike_num+=1
        comment.Comment_list+=tempstr
        profile.dislike_num+=1
        profile.save()
        comment.save()
    return redirect(read, post.id)