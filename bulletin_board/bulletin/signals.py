from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from .models import Reply, Post


@receiver(post_save, sender=Reply)
def notify_post_author_about_reply(sender, signal, instance, **kwargs):
    domain = Site.objects.get_current().domain

    reply = instance
    post = instance.post

    # !!!
    url_to_post_detail = f'http://{domain}:8000{post.get_absolute_url()}'
    # !!!

    html_content = render_to_string(
        template_name='email_reply_notify.html',
        context={
            'reply': reply,
            'post': post,
            'url_to_post_detail': url_to_post_detail,
            'url_to_reply': None, # !!!!!
        }
    )
    msg = EmailMultiAlternatives(
        subject='На ваше объявление откликнулись!',
        body=reply.text,
        to=[post.author.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


