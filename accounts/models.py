from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid
from .managers import UserManager
# from django.contrib import messages
# from django.http import HttpResponseRedirect

# def my_view(request):
#     messages.success(request, "Сообщение успешно отправлено!")
#     return HttpResponseRedirect('/')


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=150, unique=True)    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='profiles/default.png', upload_to='profiles')
    about = models.TextField()
    fname = models.CharField(max_length=300)
    lname = models.CharField(max_length=300)
    pronouns = models.CharField(max_length=100)
    website = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username} Profile'


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f'{self.follower} is following {self.following}'

class Message(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                        primary_key=True, editable=False)
 
    def __str__(self):
        return self.subject
 
    class Meta:
        ordering = ['is_read', '-created']