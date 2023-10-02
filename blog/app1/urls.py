from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   
   path('home/',views.home,name='index'),
   path('login/',views.login,name='login'),
   path('signup/',views.signup,name='signup'),
   path('addblog/',views.addblog,name='addblog'),
   path('',views.hometrue,name='hometrue'),
   path('blogdetails/<slug>/',views.blogdetail,name="blogdetails"),
   #path('addcomments',views.commentsection,name="blogdetails")\\
   path('chatbot/',views.chatbot,name="chatbot"),
   path ('newsdetails/',views.news,name ="news"),
   path ('newsdetails1/',views.news1,name ="news1"),
   path ('newsdetails2/',views.news2,name ="news2"),
   path ('profile/',views.profile,name ="profile"),
   path ('editprofile/',views.editprofile,name ="editprofile"),
   path('visual/',views.visual,name = 'visual'),
   path('blog-delete/<id>', views.blog_delete, name="blog_delete"),
   path('blog-update/<slug>/', views.blog_update, name="blog_update")
]
