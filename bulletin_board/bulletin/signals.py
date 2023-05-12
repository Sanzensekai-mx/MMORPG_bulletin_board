from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import Signal

from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from .models import Reply, Post

update_reply_signal = Signal()


@receiver(update_reply_signal, sender=Reply)
def notify_reply_status(sender, signal, instance, **kwargs):
    domain = Site.objects.get_current().domain

    # print(kwargs)

    reply = instance
    post = instance.post

    # !!!
    url_to_post_detail = f'http://{domain}:8000{post.get_absolute_url()}'
    # !!!

    is_accept = kwargs.get('is_accept', False)
    answer_choices = ['принят', 'отконен']
    answer_choice = answer_choices[0] if is_accept else answer_choices[1]

    html_content = render_to_string(
        template_name='email_reply_accept_reject.html',
        context={
            'reply': reply,
            'post': post,
            'url_to_post_detail': url_to_post_detail,
            'is_accept': is_accept,
            'answer_choice': answer_choice
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Ваш отклик на объявление {answer_choice}',
        body=reply.text,
        to=[reply.user.email]
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=Reply)
def notify_post_author_about_reply(sender, signal, instance, **kwargs):
    domain = Site.objects.get_current().domain

    reply = instance
    post = instance.post

    # !!!
    url_to_post_detail = f'http://{domain}:8000{post.get_absolute_url()}'
    # !!!
    if kwargs['created']:
        html_content = render_to_string(
            template_name='email_reply_notify.html',
            context={
                'reply': reply,
                'post': post,
                'url_to_post_detail': url_to_post_detail,
                'url_to_reply': None,  # !!!!!
            }
        )
        msg = EmailMultiAlternatives(
            subject='На ваше объявление откликнулись!',
            body=reply.text,
            to=[post.author.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
