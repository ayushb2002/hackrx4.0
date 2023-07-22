from django.urls import path,include
from .views import get_instagram_profile,get_instagram_stats,get_instagram_posts,get_subreddit_data,test,get_tweets,scrape_facebook_page,save_posts,dashboard, generateDataForTwitter, generateDataForInsta, generateLeads, dataVisualization,sales_analytics,approve_employee_view,todo,settings,change_password_view,analysis, competitorAnalysis, dataFilter
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.contrib import admin

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
    # path('login/', login, name='login'),
    # signup page
    path("", include("accounts.urls")),
    # dashboard page
    path('login/dashboard/', dashboard, name='dashboard'),
    # generate data Twitter
    path('generateDataFromTwitter/', generateDataForTwitter, name='generateDataFromTwitter'),
    # generate data Instagram
    path('generateDataFromInsta/', generateDataForInsta, name='generateDataFromInsta'),
    # generate leads
    path('generateLeads/', generateLeads, name='generateLeads'),
    # data visualization
    path('dataVisualization/', dataVisualization, name='dataVisualization'),
    # sales analytics
    path('sales-analysis',sales_analytics,name='sales-analytics'),
    # admin approve employee account
    path('approve_employee/', approve_employee_view, name='approve_employee'),
    path('todo/', todo, name='todo'),
    # path('del/<str:item_id>', views.remove, name="del"),
    path('settings/', settings, name='settings'),
    path('change_password/', change_password_view, name='change_password'),
    path('analysis/',analysis,name='analysis'),
    path('competitors/', competitorAnalysis, name="competitors"),

    path('dataFilter/', dataFilter, name='dataFilter'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),

]
