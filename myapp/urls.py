from django.urls import path
from .import views

urlpatterns = [
    #----------------------------home/login/logout/register/forgot-password---------------------------
   
    path('',views.user_login,name='login'),
    path('index/',views.index,name='index'),
    path('logout/',views.user_logout,name='logout'),
    path('register/',views.user_register,name='register'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('all',views.all,name='all'),
  
    #--------------------------------Profile----------------------------------------------------------  
   
    path('my-profile/',views.my_profile,name='my-profile'),
    path('edit-profile/',views.edit_profile,name='edit-profile'),
    path('change-password/',views.change_password,name='change-password'),
    path('delete-profile/',views.delete_profile,name='delete-profile'),
    path('user-profile/<int:pk>',views.user_profile,name='user-profile'),
   
    #------------------------------Post---------------------------------------------------------------
    
    path('create-post/',views.create_post,name='create-post'),
    path('edit-post/<int:pk>',views.edit_post,name='edit-post'),
    path('delete-post/<int:pk>',views.delete_post,name='delete-post'),
   
    #-----------------------------comment----------------------------------------------------------
   
    path('my-comment/<int:pk>',views.my_comment,name='my-comment'),
    path('comment/<int:pk>',views.comment,name='comment'),
    path('delete-comment/<int:pk>',views.delete_comment,name='delete-comment'),
    
    #------------------------------------Like---------------------------------------------------------
    
    path('like/',views.like,name='like'),
    path('unlike/',views.unlike,name='unlike'),
    
    #-------------------------------------request--------------------------------------------------
    
    path('sent-request/<int:pk>',views.sent_request,name='sent-request'),
    path('my-request/',views.my_request,name='my-request'),
    path('accept-request/<int:pk>',views.accept_request,name='accept-request'),
    path('delete-request/<int:pk>',views.delete_request,name='delete-request'),
    path('my-send-request/',views.my_send_request,name='my-send-request'),
    path('cancel-request/<int:pk>',views.cancel_request,name='cancel-request'),
    
    #--------------------------------Friend-list----------------------------------------------------
   
    path('friend-list/',views.friend_list,name='friend-list'),
    path('delete-friend/<int:pk>',views.delete_friend,name='delete-friend'),
    
    path('search/',views.search,name='search')   
]