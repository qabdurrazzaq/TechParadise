from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from .models import ConfirmEmail
import random
import hashlib

def user_created(sender,instance,created,*args,**kwargs):
    user = instance
    if created:
        email_confirmed, email_is_created = ConfirmEmail.objects.get_or_create(user=user)
        if email_is_created:
            short_hash = hashlib.sha1(str(random.random()).encode()).hexdigest()[:5]
            base, domain = str(user.email).split("@")
            email_activation_key = hashlib.sha1((str(random.random())+short_hash+base).encode()).hexdigest()
            email_confirmed.email_activation_key = email_activation_key
            email_confirmed.save()
            email_confirmed.activate_user_email()

post_save.connect(user_created, sender = settings.AUTH_USER_MODEL)