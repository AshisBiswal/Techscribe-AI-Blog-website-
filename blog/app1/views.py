from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import BlogModel,Bloggers,Addcomment,Profile,Chat
from django.http import JsonResponse
import openai
import requests
from django.utils import timezone
from .form import *
from .apikey import API_KEY,API_Secret,API_Key
from django.core.cache import cache  
import json



openai.api_key = API_KEY
def ask_openai(message):
    url = "https://chatgpt-api8.p.rapidapi.com/"

    payload = [
        {
            "content": message,
            "role": "user"
        }
    ]
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "339208829emshf69cf262725a427p1a5366jsn62834fb2b081",
        "X-RapidAPI-Host": "chatgpt-api8.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    #print(response.json())
    return response.json()

  
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')

    
        cache_key = f'chatbot_response:{message}'

        
        response_text = cache.get(cache_key)

        if response_text is None:
           
            response_data = ask_openai(message)
            response_text = response_data.get('text', 'No response')

            
            cache.set(cache_key, response_text, timeout=3600)  # Cache for 1 hour

        chat = Chat(user=request.user, message=message, response=response_text, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response_text})

    return render(request, 'chatbot.html', {'chats': chats})







    

def getvisual(url):
    api_key = API_Key
    api_secret = API_Secret
    image_url = url

    response = requests.get(
    'https://api.imagga.com/v2/tags?image_url=%s' % image_url,
    auth=(api_key, api_secret))

    #print(response.json())
    return response.json()

def visual(request):
    if request.method == 'POST':
        url = request.POST.get('imageurl')
        answer = getvisual(url)
        print(answer)
        return render(request, 'visual.html', {'answer': answer})

    # If the request method is not POST or if it's the initial GET request
    return render(request, 'visual.html', {'answer': None})


def analyze_image(image,category):
    api_key = API_Key
    api_secret = API_Secret

    # Construct the URL for image analysis using the Imagga API
    url = 'https://api.imagga.com/v2/tags?image_url=%s' % image.url  # Assuming image is a Django ImageField

    response = requests.get(url, auth=(api_key, api_secret))

    if response.status_code == 200:
        result = response.json()
        tags = result.get('result', {}).get('tags', [])
        print(tags)
        # Check if any of the detected tags indicate explicit content
        unwanted_tags = ['explicit', 'nudity', 'violence',category]  # Define the unwanted tags
        for tag in tags:
            if tag['tag'] in unwanted_tags:
                return True  # Image is explicit

    # If no explicit tags were found or there was an error, assume the image is not explicit
    return False


def home(request):
    context = {"blogs":BlogModel.objects.all()}
    if(request.method == 'POST'):
        categories = request.POST.getlist('filter')
        blogs = BlogModel.objects.all()
        filtered_blogs = []
        for blog in blogs:
            img = blog.image
            is_explicit = analyze_image(img,categories)

        
            if not is_explicit:
                filtered_blogs.append(blog)
        print(filtered_blogs)

        return render(request, 'index.html', {'blogs': filtered_blogs})
    else:
        
        return render(request,'index.html',context)
    #return render(request,'index.html',context)

def addblog(request):
    context = {'form': BlogForm()}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            title = request.POST.get('title')
            image = request.FILES.get('image', '')
            cate = request.POST.get('category')
            user = request.user

            if form.is_valid():
                print('Valid')
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user=user, title=title,
                content=content, image=image
            )
            blogger_obj = Bloggers.objects.create(
                name=user,
                category=cate,
                blogs=title  # Store the title of the blog
            )
            #print(blog_obj)
            #print(blog_obj2)
            return redirect('/addblog/')
    except Exception as e:
        print(e)
    return render(request,'addblog.html',context)

#def addcomment(request):



def hometrue(request):
   
    return render(request,'home.html')
def login(request):
    if(request.method == 'POST'):
        uname = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user=authenticate(request,username=uname,password=pass1)
        if user is not None:
            #login(request,user)
            return redirect('index')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")
    return render(request,'login.html')

def signup(request):
    if(request.method == 'POST'):
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if(pass1!=pass2):
            return HttpResponse("your confirm password is incorrect")
        else:
            my_user = User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')

    return render(request,'signup.html')
def blogdetail(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug=slug).first()
        if request.method == 'POST':
            comment_text = request.POST.get('comment1')
            if comment_text:
                user = request.user
                comment = Addcomment.objects.create(name=user, comment=comment_text, blog=blog_obj)
                comment.save()
                blog_obj.increment_view_count2()

        comments = Addcomment.objects.filter(blog=blog_obj)
        context['blog_obj'] = blog_obj
        context['comments'] = comments
        blog_obj.increment_view_count()
        return render(request, 'blogdetails.html', context)
    except Exception as e:
        print(e)
    #print(comments)
    return render(request, 'blogdetails.html', context)


def LogoutPage(request):
    logout(request)
    return redirect('login')

def news(request):
    return render(request,'newsdetails.html')

def news1(request):
    return render(request,'newsdetails1.html')

def news2(request):
    return render(request,'newsdetails2.html')

def profile(request):
    context = {}
    user = request.user
    if(user == None):
        context['profile'] = None
        context['blog_objs'] = "NO BLOGS OF USER FOUND"
        return render(request, 'profile.html',context)
        

    p = Profile.objects.get(Name = user)
    user_blogs = BlogModel.objects.filter(user=user)
    if(p is not None):
        
        context['profile'] = p
        context['blog_objs'] = user_blogs
    else:
        context['profile'] = None
        context['blog_objs'] = "NO BLOGS OF USER FOUND"
        
    

    

    return render(request, 'profile.html',context)
    
def editprofile(request):
    context = {}
    user = request.user

    if request.method == 'POST':
        name = request.POST.get('name')
        photo1 = request.FILES.get('photo')
        facebook = request.POST.get('Facebook')
        instagram = request.POST.get('Instagram')
        about = request.POST.get('about')

        user_obj = User.objects.get(username=user)
        user_obj.username = name
        user_obj.save()

        try:
            profile = Profile.objects.get(Name=user)
            profile.img = photo1
            profile.facebook = facebook
            profile.instagram = instagram
            profile.about = about
            profile.save()
        except Profile.DoesNotExist:
            # Create a new profile if it doesn't exist
            profile = Profile.objects.create(
                Name=user_obj,
                img=photo1,
                facebook=facebook,
                instagram=instagram,
                about=about
            )

    return render(request, "editprofile.html")

def blog_update(request, slug):
    context = {}
    try:

        blog_obj = BlogModel.objects.get(slug=slug)

        if blog_obj.user != request.user:
            return redirect('/')

        initial_dict = {'content': blog_obj.content}
        form = BlogForm(initial=initial_dict)
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(form)
            print(request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user=user, title=title,
                content=content, image=image
            )

        context['blog_obj'] = blog_obj
        context['form'] = form
    except Exception as e:
        print(e)

    return render(request, 'update_blog.html', context)


def blog_delete(request, id):
    try:
        blog_obj = BlogModel.objects.get(id=id)

        if blog_obj.user == request.user:
            blog_obj.delete()

    except Exception as e:
        print(e)

    return redirect('/see-blog/')


      
        
   
