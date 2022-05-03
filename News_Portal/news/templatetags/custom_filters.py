from django import template

register = template.Library()


@register.filter()
def censor(text_to_filter):
    # В тексте text_to_filter заменим все буквы слов из списка bad_words на
    # символы '*'. Слово из списка bad_words может являться частью другого
    # слова. В данный момент мы все равно произведем замену.
    # Пока, чтобы проверить работу, будем заменять часто встречающиеся предлоги
    # и приставки

    bad_words = [
        'на',
        'не',
        'ли',
        'это',
    ]

    filtered_text = text_to_filter
    for bw in bad_words:
        filtered_text = filtered_text.replace(bw, '*' * len(bw))
    return filtered_text
