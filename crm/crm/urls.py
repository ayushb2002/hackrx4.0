from django.urls import path
from .views import get_instagram_profile,get_instagram_stats,get_instagram_posts,get_subreddit_data,get_tweets

urlpatterns = [
    # username
    path('instagram/profile/', get_instagram_profile, name='instagram-profile'),
    # array of instagram post links => post_links=[...]
    path('instagram/stats/', get_instagram_stats, name='instagram-stats'),
    # hashtag from instagram 
    path('instagram-posts/', get_instagram_posts, name='get_instagram_posts'),
    # subreddit_name
    path('subreddit-data/', get_subreddit_data, name='get_subreddit_data'),
    # keyword, count
    path('tweets/', get_tweets, name='get_tweets'),
]
