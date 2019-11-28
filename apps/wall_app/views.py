from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from apps.wall_app.models import *
import bcrypt
from datetime import date, datetime



def index(request):
    return render(request, "wall_app/index.html")

def login(request):
    valid_user = User.objects.filter(email=request.POST['email'])
    if valid_user:
        current_user = valid_user[0]

        pw_match = bcrypt.checkpw(request.POST['password'].encode(), current_user.password.encode())

        if pw_match:
            request.session['user_id'] = current_user.id
        else:
            messages.error(request, "Invalid credentials")
            return redirect("/")
    else:
        messages.error(request, "Invalid credentials")
        messages.error(request, "Please try again")
        return redirect("/")
    return redirect ("/home")


def home(request):
    user_id = request.session.get('user_id')
    # comment_id = request.session.get('comment_id')

    if not user_id:
        return redirect("/")

  
    user = User.objects.get(id=user_id)
    all_messages = Message.objects.all()
    all_comments = Comment.objects.all()
   
   

    context = {"user": user, "messages" : all_messages, "comments" : all_comments}
    return render(request, "wall_app/welcome.html", context)


def wall(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("/")

  
    user = User.objects.get(id=user_id)
    all_messages = Message.objects.all()
    all_comments = Comment.objects.all()

    context = {"user": user, "messages" : all_messages, "comments" : all_comments}
    return render(request, "wall_app/wall.html", context)

def register(request):
    taken_user = User.objects.filter(email=request.POST['email'])
    if taken_user:
        messages.error(request, "Invalid credentials")
        return redirect("/")

    if not User.objects.is_reg_valid(request):
        return redirect("/")

    hashed = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())

    new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed, birthday=request.POST['birthday'])
    request.session['user_id'] = new_user.id
    print(new_user.id)
    return redirect("/home")

def add_message_home(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    new_message = Message.objects.create(user = user, message = request.POST['message'])
    request.session['message_id'] = new_message.id
    return redirect("/home")

def add_message_wall(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    new_message = Message.objects.create(user = user, message = request.POST['message'])
    request.session['message_id'] = new_message.id
    return redirect("/wall")

def delete_home(request, message_id):
   message = Message.objects.get(id=message_id)
   message.delete()
   return redirect('/home')

def delete_wall(request, message_id):
   message = Message.objects.get(id=message_id)
   message.delete()
   return redirect('/wall')


def add_comment(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    
    message_id = request.POST['comment_id']
    message = Message.objects.get(id=message_id)
   
    new_comment = Comment.objects.create(user = user, message = message, comment = request.POST['comment'])
    return redirect("/wall")


def logout(request):
    request.session.clear()
    return redirect('/')
