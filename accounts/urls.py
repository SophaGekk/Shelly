from django.urls import path
from . import views

# urlpatterns = [
#     path('dialogs/',views.DialogsView.as_view(), name='dialogs'),
#     path('dialogs/create/<int:user_id>/',views.CreateDialogView.as_view(), name='create_dialog'),
#     path('dialogs/<int:chat_id>/', views.MessagesView.as_view(), name='messages'),
# ]

app_name = 'accounts'
urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('unfollow/<str:username>', views.unfollow, name='unfollow'),
    path('<str:username>/_saved/', views.profile, name='profile'),
    path('settings/edit-profile/', views.edit_profile, name='edit_profile'),
    path('message/<str:pk>/', views.viewMessage, name="message"),
    path('create-message/<str:username>/', views.createMessage, name="create-message"),
    path('<str:username>/_saved/create-message/', views.createMessage, name="create-message"),
    path('inbox/', views.inbox, name="inbox"),
]