from django.urls import path

from .views import NewsList, NewsDetail, NewsSearch, PostCreate


urlpatterns = [
   path('', NewsList.as_view()),
   path('<int:pk>', NewsDetail.as_view(), name='news_details'),
   path('search/', NewsSearch.as_view()),
   path('create/', PostCreate.as_view()),
]
