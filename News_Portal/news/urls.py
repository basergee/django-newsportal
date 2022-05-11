from django.urls import path

from .views import NewsList, NewsDetail, NewsSearch, create_post


urlpatterns = [
   path('', NewsList.as_view()),
   path('<int:pk>', NewsDetail.as_view()),
   path('search/', NewsSearch.as_view()),
   path('create/', create_post),
]
