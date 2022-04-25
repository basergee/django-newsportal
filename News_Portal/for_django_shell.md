Что вы должны сделать в консоли Django?

1. Создать двух пользователей (с помощью метода User.objects.create_user('username')).

```python
from django.contrib.auth.models import User

User.objects.create_user('demo_user_1')
User.objects.create_user('demo_user_2')
```

2. Создать два объекта модели Author, связанные с пользователями.

```python
from news.models import Author

Author.objects.create(user=User.objects.get(username='demo_user_1'))
Author.objects.create(user=User.objects.get(username='demo_user_2'))
```


3. Добавить 4 категории в модель Category.

```python
from news.models import Category
Category.objects.create(name='наука')
Category.objects.create(name='спорт')
Category.objects.create(name='политика')
Category.objects.create(name='образование')
```


4. Добавить 2 статьи и 1 новость.

```python
from news.models import Post

# Добавляем первую статью
p1 = Post.objects.create(
	author = Author.objects.get(pk=1),
	post_type = Post.article,
	
    title = '2 + 2 теперь равно 5!',
    content = 'Вчера анонимный британский ученый установил невероятный факт: 2 + 2 = 5. Сделать такое шокирующее открытие ему помогли витаминки, которые он купил на Бэйкер-стрит в одном широко известном в узких кругах доме.'
)

# Добавляем новость

p2 = Post.objects.create(
	author = Author.objects.get(pk=2),
	post_type = Post.news,
    title = 'В РФ не выявлено случаев заболевания гепатитом неизвестного происхождения',
    content = 'Москва. 24 апреля. INTERFAX.RU - Случаев заболевания гепатитом неизвестного происхождения, выявленным в нескольких странах Европы и Америке, в России не зафиксировано, сообщили в воскресенье в Роспотребнадзоре.'
)

# Добавляем вторую статью

p3 = Post.objects.create(
	author = Author.objects.get(pk=2),
	post_type = Post.article,
    title = 'Существует ли информационный парадокс черных дыр?',
    content = 'В середине 1970-х годов Стивен Хокинг показал, что черные дыры не только поглощают вещество из окружающего пространства, но и излучают. Природа этого излучения такова, что оно в принципе не может нести никакой информации. Но в квантовой механике информация не может пропасть бесследно — получается противоречие, которое называют информационным парадоксом черных дыр. Попытки разрешить этот парадокс предпринимаются до сих пор — например, в марте была опубликована очередная статья на эту тему. При этом не все физики-теоретики согласны с тем, что парадокс вообще существует. Обо всем этом мы поговорили с директором мюнхенского Института физики Макса Планка Георгием Двали.'
)
```

5. Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
```python
p1.categories.add(Category.objects.get(name='наука'))
p1.categories.add(Category.objects.get(name='образование'))

p2.categories.add(Category.objects.create(name='здравоохранение'))
p2.categories.add(Category.objects.get(name='наука'))

p3.categories.add(Category.objects.get(name='наука'))
```

6. Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).

```python
import random

from news.models import Comment

comment_texts = [
    "Отлично",
    "Хорошо",
    "Абсолютная ерунда",
    "Автора сдать в дурдом",
]

# Распределим комментарии случайным образом по статьям и пользователям
posts = Post.objects.all()
commentators = User.objects.all()
for _ in range(10):
    Comment.objects.create(
        post=posts[random.randint(0, len(posts) - 1)],
        user=commentators[random.randint(0, len(commentators) - 1)],
        content = comment_texts[random.randint(0, len(comment_texts) - 1)]
    )

```

7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
```python
import random

from news.models import Post
from news.models import Comment

posts = Post.objects.all()
comments = Comment.objects.all()

# распределим лайки и дизлайки случайным образом
for _ in range(100):
    p = posts[random.randint(0, len(posts) - 1)]
    c = comments[random.randint(0, len(comments) - 1)]
    if random.randint(0, 10) > 3:
        p.like()
        c.like()
    else:
        p.dislike()
        c.dislike()

```

8. Обновить рейтинги пользователей.
```python
from django.contrib.auth.models import User
from news.models import Author, Post, Comment

# Перебираем всех пользователй в таблице User
for user in User.objects.all():
    # Найдем каждую статью, где он автор
    user_posts = Post.objects.filter(author__user=user)
    user_rating = 0
    for p in user_posts:
        user_rating += p.rank * 3
        # Найдем все комментарии к этой статье автора и добавим их рейтинг
        # к общему рейтингу
        comments = Comment.objects.filter(post=p)
        for c in comments:
            user_rating += c.rank
    # Найдем все комментарии самого автора и добавим их рейтинг к общему
    user_comments = Comment.objects.filter(user=user)
    for c in user_comments:
        user_rating += c.rank
    # Обновляем рейтинг пользователя
    Author.objects.get(user=user).update_rating(user_rating)
```

9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
```python
from news.models import Author

# Сортируем в порядке убывания рейтинга
Author.objects.all().order_by('-rank').values('user__username', 'rank')[0]
```

10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.


11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.

