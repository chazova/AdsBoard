from django.core.mail import EmailMultiAlternatives  # импортируем класс для создания объекта письма с html
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from ads.models import Ad
from django.contrib.auth.models import User
from datetime import date, timedelta


def get_users_emails():
    users_emails = []
    for user in User.objects.all():
        users_emails.append(user.email)
    return users_emails


def notify_users_weekly():
    current_date = date.today()
    one_week_ago_date = current_date - timedelta(days=7)
    ads_for_week = Ad.objects.filter(create_time__range=[one_week_ago_date, current_date])
    users_emails = get_users_emails()

    html_content = render_to_string(
        'ads_for_week.html',
        {
            'ads': ads_for_week,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Новые объявления за прошедшую неделю',
        body='',  # это то же, что и message
        from_email='test-mail-dj@yandex.ru',
        to=users_emails,  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()
