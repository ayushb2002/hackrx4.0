from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    manager = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='managed_team')
    # Add other fields for team as needed

    def __str__(self):
        return self.name


class Manager(models.Model):
    name = models.CharField(max_length=100)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True, related_name='manager')
    # Add other fields for manager as needed

    def __str__(self):
        return self.name


class Request(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Request by {self.employee.name}"



class InstagramProfile(models.Model):
    username = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    biography = models.TextField(blank=True, null=True)
    post_urls = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.username
    


class InstagramStats(models.Model):
    post_link = models.URLField()
    comments = models.JSONField()

    def __str__(self):
        return self.post_link
    


class InstagramPost(models.Model):
    hashtag = models.CharField(max_length=100)
    post_link = models.URLField()
    def __str__(self):
        return self.post_link
    
class SubredditData(models.Model):
    subreddit_name = models.CharField(max_length=100)
    selftext = models.TextField()
    author_fullname = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    upvote_ratio = models.FloatField()
    score = models.IntegerField()
    author = models.CharField(max_length=100)
    subreddit_subscribers = models.IntegerField()

    def __str__(self):
        return self.title


# class Tweet(models.Model):
#     id = models.AutoField(primary_key=True)
#     keyword = models.CharField(max_length=100, default='keyword')
#     created_at = models.CharField(max_length=100)
#     full_text = models.TextField()
#     user_name = models.CharField(max_length=100)
#     screen_name = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)
#     followers_count = models.IntegerField()
#     friends_count = models.IntegerField()
#     lang = models.CharField(max_length=10)

#     def __str__(self):
#         return self.id



    