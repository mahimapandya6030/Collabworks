from django.urls import path
from .views import login_view, signup, profile_view, edit_profile, add_skill, logout_view, user_profile_view

app_name = 'accounts'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/<str:username>/', user_profile_view, name='user_profile'),
    path('edit/', edit_profile, name='edit_profile'),
    path('new_skills/', add_skill, name='add_skills'),
]
