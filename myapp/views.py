from django.shortcuts import render,redirect
from .forms import*
from .models import*
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.
@login_required(login_url='/')
def index(request):
   # req=Friendrequest.objects.filter(from_user=request.user)
    post=Post.objects.all()[::-1]
    return render(request,'index.html',{'post':post})
    
#-----------------------------register/login/logout/forgot-password--------------------------------------------------
  
def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form=LoginForm()
        if request.method =="POST":
            form1=LoginForm(request=request,data=request.POST)
            if form1.is_valid():
                user=authenticate(username=form1.cleaned_data['username'],password=form1.cleaned_data['password'])
                if user is not None:
                    login(request,user)
                    return redirect('index')
                else:
                    print(form.errors)
                    messages.warning(request,'enter the valid data')
                    return render(request,'login.html',{'form':form})
            else:
                print(form.errors)
                messages.warning(request,'enter the valid data')
                return render(request,'login.html',{'form':form})                
        return render(request,'login.html',{'form':form})

def user_register(request):
    if request.user.is_authenticated:   
        return redirect('index')
    else:
        form=RegisterForm()
        if request.method == "POST":
            form1=RegisterForm(request.POST)
            if form1.is_valid():
                form1.save()
                messages.success(request,'your account created')
                return redirect('login')
            else:
                messages.warning(request,'Enter the valid data')
                return render(request,'register.html',{'form':form})         
        return render(request,'register.html',{'form':form})

@login_required(login_url='/')
def user_logout(request):
    logout(request)
    return redirect('login')


def forgot_password(request):
    if request.user.is_authenticated:   
        return redirect('index')
    else:
        if request.method =="POST":
            try:
                user=User.objects.get(email=request.POST['email'])
                password="".join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',k=9))
                subject="Rest Password With Email Id"
                message=f""" hello {user.username} your new password is {password}"""
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'],]
                send_mail(subject,message,email_from,recipient_list)
                user.password=make_password(password)
                user.save()
                messages.success(request,'Your New password send in your email')
                return redirect('login')
            except:
                messages.warning(request,'Enter valid email addres')
                return render(request,'forgot-password.html')
                
        return render(request,'forgot-password.html')
#------------------------------------------profile--------------------------------------------
@login_required(login_url='/')
def my_profile(request):
    post=Post.objects.filter(user=request.user)
    return render(request,'my-profile.html',{'post':post})

@login_required(login_url='/')
def edit_profile(request):
    form=EditprofileForm(instance=request.user)
    if request.method =="POST":
        form1=EditprofileForm(request.POST,request.FILES,instance=request.user)
        if form1.is_valid():
            form1.save()
            messages.success(request,'your profile update')
            return redirect('my-profile')
        else:
            messages.warning(request,'Enter the valid data')
            return render(request,'edit-profile.html',{'form':form})
    return render(request,'edit-profile.html',{'form':form})

@login_required(login_url='/')
def delete_profile(request):
    request.user.delete()
    messages.success(request,'Your Account deleted')
    return redirect('register')

@login_required(login_url='/')
def change_password(request):
    form=PasswordForm(user=request.user)
    if request.method =="POST":
        form1=PasswordForm(user=request.user,data=request.POST)
        if form1.is_valid():
            update_session_auth_hash(request,form1.user)
            form1.save()
            messages.success(request,'your password change successfully')
            return redirect('login')
        else:
            messages.warning(request,'enter the correct pasword')
            return render(request,'change-password.html',{'form':form})   
    return render(request,'change-password.html',{'form':form})

@login_required(login_url='/')
def user_profile(request,pk):
    user=User.objects.get(id=pk)
    post=Post.objects.filter(user=user)
    try:
        req=Friendrequest.objects.get(to_user=user)
        return render(request,'user-profile.html',{'user':user,'post':post,'req':req})
    except:
        return render(request,'user-profile.html',{'user':user,'post':post})
        
#------------------------------------------Post--------------------------------------------------
@login_required(login_url='/')
def create_post(request):
    form=CreatepostForm()
    if request.method == "POST":
        form1=CreatepostForm(request.POST,request.FILES)
        if form1.is_valid():
            v=form1.save(commit=False)
            v.user=request.user
            v.save()
            return redirect('my-profile')
        print(form1.errors)
    return render(request,'create-post.html',{'form':form})

@login_required(login_url='/')
def edit_post(request,pk):
    post=Post.objects.get(id=pk)
    com=Comment.objects.filter(post=post)
    form=EditpostForm(instance=post)
    if request.method =="POST":
        form1=EditpostForm(request.POST,instance=post)
        if form1.is_valid():
            form1.save()
            messages.success(request,'Update your post successfully')
            return redirect('edit-post',pk)
        else:
            messages.warning(request,'enter the valid data')
            return render(request,'edit-post.html',{'post':post,'com':com,'form':form})
    return render(request,'edit-post.html',{'post':post,'com':com,'form':form})

@login_required(login_url='/')
def delete_post(request,pk):
    post=Post.objects.get(id=pk)
    post.delete()
    return redirect('my-profile')
#-----------------------------------------comment---------------------------------------------------------
@login_required(login_url='/')
def my_comment(request,pk):
    post=Post.objects.get(id=pk)
    com=Comment.objects.filter(post=post)[::-1]
    com1=Comment.objects.filter(post=post).count()
    return render(request,'comments.html',{'com':com,'post':post,'com1':com1})

@login_required(login_url='/') 
def comment(request,pk):
    if request.method =="POST":
        post=Post.objects.get(id=pk)
        com=Comment.objects.filter(post=post)[::-1]
        form1=CommentForm(request.POST)    
        if form1.is_valid():
            v=form1.save(commit=False)
            v.user=request.user
            v.post=post
            v.save()
            messages.success(request,'Thank you for comment')
            return redirect('my-comment',pk)
        messages.warning(request,'Sorry your comment not uplaod')
        return redirect('my-comment',pk)
 
@login_required(login_url='/')    
def delete_comment(request,pk):
    com=Comment.objects.get(id=pk)
    pk1=com.post_id
    com.delete()
    return redirect('my-comment',pk1)    


#---------------------------------------like----------------------------------------------------
# @login_required(login_url='/')
# def like(request,pk): 
#     post=Post.objects.get(id=pk)
#     post.likes.add(request.user)
#     post.save()
#     if post.user in request.user.friends.all():
#         return redirect('index')
#     else:
#         return redirect('all')

@login_required(login_url='/')
def like(request):
    user=request.user
    if request.method == "POST":
        id=request.POST.get('id')
        val=request.POST.get('str')
        post=Post.objects.get(id=id)
        if val == 'Like':
            post.likes.add(user)
            post.save()
            a=post.total_likes
            return JsonResponse({'status':200,'likes':a})
        else:
            post.likes.remove(user)
            post.save()
            a=post.total_likes
            return JsonResponse({'status':200,'likes':a})
            
      


@login_required(login_url='/')
def unlike(request): 
    user=request.user
    if request.method == "POST":
        id=request.POST.get('id')
        val=request.POST.get('str')
        post=Post.objects.get(id=id)
        if val == 'Like':
            post.likes.add(user)
            post.save()
            a=post.total_likes
            return JsonResponse({'status':200,'likes':a})
        else:
            post.likes.remove(user)
            post.save()
            a=post.total_likes
            return JsonResponse({'status':200,'likes':a})
#-----------------------------------------friend-request---------------------------------------
@login_required(login_url='/')
def sent_request(request,pk):
    user=User.objects.get(id=pk)
    Friendrequest(to_user=user,from_user=request.user).save()
    return redirect('user-profile',pk)

@login_required(login_url='/')
def my_request(request):
    req=Friendrequest.objects.filter(to_user=request.user)[::-1]
    return render(request,'my-request.html',{'req':req})

@login_required(login_url='/') 
def accept_request(request,pk):
    req=Friendrequest.objects.get(id=pk)
    req.status = True
    req.save()
    request.user.friends.add(req.from_user)
    request.user.save()
    req.from_user.friends.add(request.user)
    req.save()
    req.delete()
    return redirect('my-request')

@login_required(login_url='/')
def delete_request(request,pk):
    req=Friendrequest.objects.get(id=pk)
    req.delete()
    return redirect('my-request')

@login_required(login_url='/')
def my_send_request(request):
    req=Friendrequest.objects.filter(from_user=request.user)
    return render(request,'my-send-request.html',{'req':req})

@login_required(login_url='/')
def cancel_request(request,pk):
    req=Friendrequest.objects.get(id=pk)
    req.delete()
    return redirect('my-send-request')
#----------------------------------------------------------friend-list-------------------------------
@login_required(login_url='/')
def friend_list(request):
    return render(request,'friend-list.html')

@login_required(login_url='/')
def delete_friend(request,pk):
    user=User.objects.get(id=pk)
    request.user.friends.remove(user)
    request.user.save()
    user.friends.remove(request.user)
    user.save()
    return redirect('friend-list')

@login_required(login_url='/')
def search(request):
    if request.method =="GET":
        search=request.GET.get('search')
        if search:
            user=User.objects.filter(username__icontains=search)
            return render(request,'search.html',{'user':user})
        else:
            return redirect('index')
   
def all(request):
    post=Post.objects.all()
    return render(request,'all.html',{'post':post})   
