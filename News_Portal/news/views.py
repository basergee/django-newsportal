from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post
from .filters import NewsFilter
from .forms import PostForm, UserEditForm, BaseRegisterForm


# Create your views here.
class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-creation_time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'default.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news_list'
    # Ограничиваем количество новостей на странице
    paginate_by = 10


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publication_date'] = self.object.creation_time.strftime('%d.%m.%Y')
        return context


class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news_search_results'
    # Ограничиваем количество новостей на странице
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Не знаю, как добавить преобразование в класс фильтра, поэтому пока
        # сделаю так.
        #
        # Сперва применим фильтр NewsFilter. Он вернет отфильтрованные
        # значения. Затем мы отфильтруем эти значения следующим образом.
        #
        # Из строки GET-запроса выделим дату публикации.
        # Затем преобразуем ее в тип datetime, потому что можно применить
        # фильтр 'date__gt' к полю 'creation_time'. Таким образом останутся
        # только записи позже указанной даты. Их и вернем.
        #
        # Также возможны два случая, по которым мы можем определить, что
        # пользователь не ввел дату или ввел ее неправильно:
        # 1 - в GET-запросе нет параметра creation_date;
        # 2 - параметра creation_date пустой или неправильный.
        # В обоих случаях считаем, что по дате фильтровать не надо.

        self.filterset = NewsFilter(self.request.GET, queryset)

        try:
            dt = datetime.strptime(self.request.GET['creation_date'], '%Y-%m-%d')
        except MultiValueDictKeyError:
            return self.filterset.qs
        except ValueError:
            return self.filterset.qs

        return self.filterset.qs.filter(creation_time__date__gt=dt)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.filterset
        return context


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    def form_valid(self, form):
        # Узнаем, с какой страницы пришел запрос
        # В данный момент запрос может придти с двух страниц:
        # 1. /articles/create/
        # 2. /news/create/
        # В зависимости от адреса устанавливаем тип посту перед сохранением
        post = form.save(commit=False)
        if self.request.path == '/articles/create/':
            # Мы создаем статью
            post.post_type = 'AR'
        elif self.request.path == '/news/create/':
            # Мы создаем новость
            post.post_type = 'NE'

        return super().form_valid(form)


class PostEdit(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class UserEdit(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('news_list')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = reverse_lazy('news_list')
