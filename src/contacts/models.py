# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# from managers import FriendshipManager
from django.db.models.signals import post_save
    

class MyUser(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100, default = 'Me')
    description = models.TextField(default = "None")
    like_number = models.IntegerField(default = 0)
    def __unicode__(self):
        return self.name  
    def save(self, *args, **kwargs):
        try:
            existing = MyUser.objects.get(user=self.user)
            self.id = existing.id #force update instead of insert
        except MyUser.DoesNotExist:
            pass 
        models.Model.save(self, *args, **kwargs)
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        MyUser.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)  

class Message(models.Model):
    sender = models.ForeignKey(MyUser, related_name = 'profile')
    receiver = models.ForeignKey(User)
    message = models.TextField()
    subject = models.CharField(max_length=50, default = 'No Subject')
    
class Like(models.Model):
    user = models.ForeignKey(User)
    profile = models.ForeignKey(MyUser)