from django.urls import path
from django.contrib.auth.views import LoginView

from .views import (NewsList, NewsDetail, NewsSearch,
                    PostCreate, PostEdit, PostDelete,
                    UserEdit, BaseRegisterView)


urlpatterns = [
   path('', NewsList.as_view(), name='news_list'),
   path('<int:pk>', NewsDetail.as_view(), name='news_details'),
   path('search/', NewsSearch.as_view()),
   path('create/', PostCreate.as_view()),
   path('<int:pk>/edit/', PostEdit.as_view()),
   path('<int:pk>/delete/', PostDelete.as_view()),
   path('edit_user/<int:pk>/', UserEdit.as_view()),

    path('login/',
        LoginView.as_view(template_name='../templates/login.html'),
        name='login'),
    path('signup/',
        BaseRegisterView.as_view(template_name='../templates/signup.html'),
        name='signup'),
]
