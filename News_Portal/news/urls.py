from django.urls import path

from .views import NewsList, NewsDetail, NewsSearch, PostCreate, PostEdit


urlpatterns = [
   path('', NewsList.as_view()),
   path('<int:pk>', NewsDetail.as_view(), name='news_details'),
   path('search/', NewsSearch.as_view()),
   path('create/', PostCreate.as_view()),
   path('<int:pk>/edit/', PostEdit.as_view()),
]
