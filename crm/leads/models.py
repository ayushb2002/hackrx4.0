from django.db import models

class Lead(models.Model):
    STATUS_CHOICES = (
        ('new', 'New Lead'),
        ('engaged', 'Engaged Lead'),
        ('qualified', 'Qualified Lead'),
        ('converted', 'Converted Lead'),
        ('lost', 'Lost Lead'),
    )

    username=models.CharField(max_length=100,default=None)
    location=models.CharField(max_length=100,default=None)
    status=models.CharField(choices=STATUS_CHOICES,max_length=100,default='new')
    handled_by=models.ManyToManyField("accounts.employee", default=None,null=True)

    # Add other fields as needed for lead information
    def __str__(self):
        return self.username
    
    
class Tweet(models.Model):
    keyword = models.CharField(max_length=255)
    created_at = models.CharField(max_length=255)
    full_text = models.TextField()
    user_name = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    followers_count = models.IntegerField()
    friends_count = models.IntegerField()
    lang = models.CharField(max_length=10)
    
class FacebookPost(models.Model):
    account_name = models.CharField(max_length=255)
    post_content = models.TextField()
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    
class Post(models.Model):
    account_name = models.CharField(max_length=255)
    post_content = models.TextField()
    keyword = models.CharField(max_length=50)

    def __str__(self):
        return self.account_name