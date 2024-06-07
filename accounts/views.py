from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse
from django.urls import reverse

from boards.forms import CreateBoardForm
from .forms import UserRegistrationForm, UserLoginForm, EditProfileForm
from .models import User, Follow

from django.contrib import messages
# from .models import  Message, Chat
from .forms import  MessageForm


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            check_user = User.objects.filter(
                Q(username=data['username']) | Q(email=data['email'])
            )
            if not check_user:
                user = User.objects.create_user(
                    data['email'], data['username'], data['password']
                )
                return redirect('accounts:user_login')
    else:
        form = UserRegistrationForm()
    context = {'title':'Signup', 'form':form}
    return render(request, 'register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password']
            )
            print(user)
            if user is not None:
                login(request, user)
                return redirect('pinterest:home')
            else:
                return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = UserLoginForm()
    context = {'title':'Login', 'form': form}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')


@login_required
def follow(request, username):
    user = get_object_or_404(User, username=username)
    check_user = Follow.objects.filter(follower=request.user, following=user)
    if user == request.user:
        raise Http404
    elif check_user.exists():
        raise Http404
    else:
        follow = Follow.objects.create(follower=request.user, following=user)
        follow.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unfollow(request, username):
    user = get_object_or_404(User, username=username)
    following = Follow.objects.filter(following=user).delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    print(user)
    print(user)
    boards = user.board_user.all()
    is_following = request.user.followers.filter(following=user).first()
    create_board_form = CreateBoardForm()
    context = {
        'user': user,
        'boards':boards,
        'is_following': is_following,
        'create_board_form':create_board_form
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user.username)
    else:
        form = EditProfileForm(instance=request.user.profile)
    context = {'title': 'Edit Profile', 'form': form}
    return render(request, 'edit_profile.html', context)


# @login_required(login_url='login')
# class DialogsView(View):
#     def get(self, request):
#         chats = Chat.objects.filter(members__in=[request.user.id])
#         return render(request, 'dialogs.html', {'user_profile': request.user, 'chats': chats})
# @register.simple_tag
# def get_companion(user, chat):
#     for u in chat.members.all():
#         if u != user:
#             return u
#     return None 
# @login_required
# class MessagesView(View):
#     def get(self, request, chat_id):
#         try:
#             chat = Chat.objects.get(id=chat_id)
#             if request.user in chat.members.all():
#                 chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
#             else:
#                 chat = None
#         except Chat.DoesNotExist:
#             chat = None
 
#         return render(
#             request,
#             'users/messages.html',
#             {
#                 'user_profile': request.user,
#                 'chat': chat,
#                 'form': MessageForm()
#             }
#         )
 
#     def post(self, request, chat_id):
#         form = MessageForm(data=request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.chat_id = chat_id
#             message.author = request.user
#             message.save()
#         return redirect(reverse('users:messages', kwargs={'chat_id': chat_id}))


@login_required(login_url='login') 
def inbox(request): 
    profile = request.user.profile 
    messageRequests = profile.messages.all() 
    unreadCount = messageRequests.filter(is_read=False).count() 
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount} 
    return render(request, 'inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'message.html', context)


def createMessage(request, username):
    form = MessageForm()
    recipient = User.objects.get(username=username).profile
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        print(form.is_valid())
        print(form.is_valid())
        if form.is_valid():


            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.user.username
                message.email = sender.user.email
            message.save()
            messages.success(request, 'Your message was successfully sent!')
            return redirect('accounts:profile', username=recipient.user.username)
    context = {'recipient': recipient, 'form': form}
    return render(request, 'message_form.html', context)   