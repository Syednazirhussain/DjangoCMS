### Singnals
 
 from django.contrib.auth.models import User
 from django.db.models.signals import post_save

post_save.connect(function_name, sender=User)

-----------------------------------------------------
## We also use decorators for this task

from django.dispatch import receiver

@reciever(post_save, sender=User)
def function():
	pass

## Create singnals.py file inside app
app.py

def ready(self):
	import base.singnals

inside installed app array add like this
'base.app.BaseConfig'

## Reset Password work

1. Submit email form  -> PasswordResetView.as_view()
2. Email sent success message -> PasswordResetDoneView.as_view()
3. Link to password email form in email -> PasswordResetConfirmView.as_view()
4. Password successfully changed message -> PasswordResetCompleteView.as_view()