from django.urls import path
from .views import get_instagram_profile,get_instagram_stats,get_instagram_posts,get_subreddit_data,test,get_tweets,scrape_facebook_page,save_posts,login, signup, dashboard, generateData, generateLeads, dataVisualization, crmConnect, crmMessage
from django.shortcuts import redirect

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
    # path('fb/', scrape_facebook_page, name='scrape_facebook_page'),
     path('', lambda request: redirect('login/', permanent=False)),
    # login page
    path('login/', login, name='login'),
    # signup page
    path('signup/', signup, name='signup'),
    # dashboard page
    path('dashboard/', dashboard, name='dashboard'),
    # generate data
    path('generateData/', generateData, name='generateData'),
    # generate leads
    path('generateLeads/', generateLeads, name='generateLeads'),
    # data visualization
    path('dataVisualization/', dataVisualization, name='dataVisualization'),
    # crm connect
    path('crmConnect', crmConnect, name="crmConnect"),
    # crm message
    path('crmMessage', crmMessage, name="crmMessage")
]
