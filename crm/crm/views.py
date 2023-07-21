import http.client
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.views.decorators.http import require_GET
import csv
import json
import os
import pickle
from django.http import JsonResponse
import requests
import json
from time import sleep
from accounts.models import InstagramProfile,InstagramStats,InstagramPost,SubredditData
from .serializers import InstagramProfileSerializer
from leads.models import Post
from django.shortcuts import render
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
import warnings
from leads.models import Lead
from accounts.models import Employee
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db.models import Count, Q
from django.conf import settings
import os


warnings.filterwarnings("ignore", category=DeprecationWarning)

@api_view(['POST'])
def test(request):
    username = 'BG10OclMcu'
    apiKey = 'TMT7FgHx6kXaQc7Vd0jtDJw85'
    scraper = 'facebookPost'
    url = 'https://www.facebook.com/bajajallianzlifeinsuranceltd/posts/pfbid038M6xPY9vMokyWctUHdcobY7dVYr35wQrAiVngThpCFKNRiHcLUP4FTjqjUf6xWxzl'

    apiEndPoint = "http://api.scraping-bot.io/scrape/data-scraper"
    apiEndPointResponse = "http://api.scraping-bot.io/scrape/data-scraper-response?"

    payload = {
        "url": url,
        "scraper": scraper
    }
    headers = {
        'Content-Type': "application/json"
    }

    response = requests.post(apiEndPoint, json=payload, auth=(username, apiKey), headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
        print(response_json["responseId"])
        responseId = response_json["responseId"]

        pending = True
        while pending:
            # Sleep 5 seconds between each loop to allow time for social media scraping
            sleep(5)
            finalResponse = requests.get(apiEndPointResponse + "scraper=" + scraper + "&responseId=" + responseId,
                                         auth=(username, apiKey))
            result = finalResponse.json()
            if isinstance(result, list):
                pending = False
                print(finalResponse.text)
            elif isinstance(result, dict):
                if "status" in result and result["status"] == "pending":
                    print(result["message"])
                    continue
                elif result["error"] is not None:
                    pending = False
                    print(json.dumps(result, indent=4))

        return JsonResponse(result, safe=False)

    else:
        return JsonResponse({'error': response.text}, status=500)


# @api_view(['POST'])
# def get_instagram_profile(request):
#     username = request.data.get('username', '')
#     if not username:
#         return JsonResponse({'error': 'Username parameter is missing.'}, status=400)
#     conn = http.client.HTTPSConnection("scraper-api.smartproxy.com")
#     payload = {
#         "target": "instagram_graphql_profile",
#         "url": f"https://www.instagram.com/{username}/",
#         "locale": "en",
#         "geo": "India"
#     }
#     headers = {
#         'Accept': 'application/json',
#         'Authorization': 'Basic UzAwMDAxMTExMjE6UCRXMTM5YThjMmQwNTM2NTg2MmI5ZTk0Y2IzZjM3NzAzMzJj',
#         'Content-Type': 'application/json'
#     }
#     payload_str = json.dumps(payload)
#     conn.request("POST", "/v1/scrape", payload_str, headers)
#     res = conn.getresponse()
#     data = res.read()
#     response = json.loads(data.decode("utf-8"))
#     # print(response)
    
#     content = response.get('data', {}).get('content', {})
#     user = content.get('user', {})
    
#     # Extracting the required information
#     username = user.get('username')
#     is_verified = user.get('is_verified')
#     followers_count = user.get('edge_followed_by', {}).get('count')
#     following_count = user.get('edge_follow', {}).get('count')
#     biography = user.get('biography')
    
#     posts = []
#     edges = user.get('edge_felix_video_timeline', {}).get('edges', [])
#     for edge in edges:
#         node = edge.get('node', {})
#         shortcode = node.get('shortcode')
#         post_url = f'https://www.instagram.com/p/{shortcode}/'
#         posts.append(post_url)
    
#     result = {
#         'username': username,
#         'verified': is_verified,
#         'followers': followers_count,
#         'following': following_count,
#         'biography': biography,
#         'post_urls': posts
#     }

#     return Response(result)
@api_view(['POST'])
def get_instagram_profile(request):
    username = request.data.get('username', '')
    if not username:
        return JsonResponse({'error': 'Username parameter is missing.'}, status=400)


    try:
        profile = InstagramProfile.objects.get(username=username)
        serialized_data = InstagramProfileSerializer(profile).data
        return Response(serialized_data)
    except InstagramProfile.DoesNotExist:
        # Call the API to get the profile data
        conn = http.client.HTTPSConnection("scraper-api.smartproxy.com")
        payload = {
            "target": "instagram_graphql_profile",
            "url": f"https://www.instagram.com/{username}/",
            "locale": "en",
            "geo": "India"
        }
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Basic UzAwMDAxMTExMjE6UCRXMTM5YThjMmQwNTM2NTg2MmI5ZTk0Y2IzZjM3NzAzMzJj',
            'Content-Type': 'application/json'
        }
        payload_str = json.dumps(payload)
        conn.request("POST", "/v1/scrape", payload_str, headers)
        res = conn.getresponse()
        data = res.read()
        response = json.loads(data.decode("utf-8"))

        content = response.get('data', {}).get('content', {})
        user = content.get('user', {})

        # Extracting the required information
        username = user.get('username')
        is_verified = user.get('is_verified')
        followers_count = user.get('edge_followed_by', {}).get('count')
        following_count = user.get('edge_follow', {}).get('count')
        biography = user.get('biography')

        posts = []
        edges = user.get('edge_felix_video_timeline', {}).get('edges', [])
        for edge in edges:
            node = edge.get('node', {})
            shortcode = node.get('shortcode')
            post_url = f'https://www.instagram.com/p/{shortcode}/'
            posts.append(post_url)

        # Save the data in the model
        profile = InstagramProfile.objects.create(
            username=username,
            verified=is_verified,
            followers=followers_count,
            following=following_count,
            biography=biography,
            post_urls=posts
        )

        # Serialize the saved data
        serialized_data = InstagramProfileSerializer(profile).data
        return Response(serialized_data)


# @csrf_exempt
# @require_POST
# def get_instagram_stats(request):
#     payload = json.loads(request.body)
#     post_links = payload.get('post_links', [])

#     result = []
#     for link in post_links:
#         conn = http.client.HTTPSConnection("scraper-api.smartproxy.com")
#         payload = json.dumps({
#             "target": "instagram_post",
#             "url": link,
#             "locale": "en",
#             "geo": "India"
#         })
#         headers = {
#             'Accept': 'application/json',
#             'Authorization': 'Basic UzAwMDAxMTExMjE6UCRXMTM5YThjMmQwNTM2NTg2MmI5ZTk0Y2IzZjM3NzAzMzJj',
#             'Content-Type': 'application/json'
#         }
#         conn.request("POST", "/v1/scrape", payload, headers)
#         res = conn.getresponse()
#         data = res.read().decode("utf-8")
#         response = json.loads(data)
        
#         # Extract the required information from the response
#         comments = response['data']['content']['comments']
#         extracted_info = [{'username': comment['username'], 'likes': comment['likes'], 'replies': comment['replies'], 'comment': comment['comment']} for comment in comments]
        
#         result.append({'post_link': link, 'comments': extracted_info})
    
#     return JsonResponse(result, safe=False)

@api_view(['POST'])
def get_instagram_stats(request):
    payload = json.loads(request.body)
    post_links = payload.get('post_links', [])
    print(post_links)
    result = []
    for link in post_links:
        # Check if the data already exists in the model
        try:
            stats = InstagramStats.objects.get(post_link=link)
            result.append({'post_link': link, 'comments': stats.comments})
        except InstagramStats.DoesNotExist:
            conn = http.client.HTTPSConnection("scraper-api.smartproxy.com")
            payload = json.dumps({
                "target": "instagram_post",
                "url": link,
                "locale": "en",
                "geo": "India"
            })
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Basic UzAwMDAxMTExMjE6UCRXMTM5YThjMmQwNTM2NTg2MmI5ZTk0Y2IzZjM3NzAzMzJj',
                'Content-Type': 'application/json'
            }
            conn.request("POST", "/v1/scrape", payload, headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            response = json.loads(data)

            # Extract the required information from the response
            comments = response['data']['content']['comments']
            extracted_info = [{'username': comment['username'], 'likes': comment['likes'], 'replies': comment['replies'], 'comment': comment['comment']} for comment in comments]

            # Save the data in the model
            stats = InstagramStats.objects.create(post_link=link, comments=extracted_info)
            result.append({'post_link': link, 'comments': extracted_info})

    return JsonResponse(result, safe=False)

@api_view(['POST'])
def get_instagram_posts(request):
    hashtag = request.data.get('hashtag', '')
    # Retrieve existing results from the database
    existing_results = InstagramPost.objects.filter(hashtag=hashtag)

    
    
    hashtag = request.data.get('hashtag', '')
    
    conn = http.client.HTTPSConnection("scraper-api.smartproxy.com")
    payload = json.dumps({
        "target": "instagram_graphql_hashtag",
        "url": f"https://www.instagram.com/explore/tags/{hashtag}/",
        "locale": "en",
        "geo": "India"
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic UzAwMDAxMTExMjE6UCRXMTM5YThjMmQwNTM2NTg2MmI5ZTk0Y2IzZjM3NzAzMzJj',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/scrape", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    result = []

    if 'data' in data:
        data = data['data']
        if 'content' in data:
            content = data['content']
            if content is not None and 'hashtag' in content:
                hashtag_data = content['hashtag']
                if 'edge_hashtag_to_media' in hashtag_data:
                    edges = hashtag_data['edge_hashtag_to_media'].get('edges', [])
                    post_links = [f"https://www.instagram.com/p/{edge['node']['shortcode']}/" for edge in edges]

                    # Retrieve existing results
                    for post in existing_results:
                        result.append({'post_link': post.post_link})

                    # Save new results obtained from the API
                    for link in post_links:
                        # Check if the data already exists in the model
                        try:
                            existing_post = InstagramPost.objects.get(post_link=link)
                            result.append({'post_link': existing_post.post_link})
                        except InstagramPost.DoesNotExist:
                            # Save the new post in the database
                            new_post = InstagramPost.objects.create(hashtag=hashtag, post_link=link)
                            result.append({'post_link': new_post.post_link})

    return Response({'post_links': result})


@api_view(['POST'])
def get_subreddit_data(request):
    subreddit_name = request.data.get('subreddit_name', '')

    # Retrieve existing results from the database
    existing_results = SubredditData.objects.filter(subreddit_name=subreddit_name)

    conn = http.client.HTTPSConnection("scraper-api.smartproxy.com")
    payload = json.dumps({
        "target": "reddit_subreddit",
        "url": f"https://www.reddit.com/r/{subreddit_name}/",
        "locale": "en",
        "geo": "India"
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic UzAwMDAxMTExMjE6UCRXMTM5YThjMmQwNTM2NTg2MmI5ZTk0Y2IzZjM3NzAzMzJj',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/scrape", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    children_data = data.get('data', {}).get('content', {}).get('data', {}).get('children', [])
    response_data = []

    # Retrieve existing results
    for result in existing_results:
        response_data.append({
            'selftext': result.selftext,
            'author_fullname': result.author_fullname,
            'title': result.title,
            'name': result.name,
            'upvote_ratio': result.upvote_ratio,
            'score': result.score,
            'author': result.author,
            'subreddit_subscribers': result.subreddit_subscribers
        })

    # Save new results obtained from the API
    for child in children_data:
        child_data = child.get('data', {})
        subreddit_data = {
            'subreddit_name': subreddit_name,
            'selftext': child_data.get('selftext', ''),
            'author_fullname': child_data.get('author_fullname', ''),
            'title': child_data.get('title', ''),
            'name': child_data.get('name', ''),
            'upvote_ratio': child_data.get('upvote_ratio', 0.0),
            'score': child_data.get('score', 0),
            'author': child_data.get('author', ''),
            'subreddit_subscribers': child_data.get('subreddit_subscribers', 0)
        }

        # Check if the data already exists in the model
        try:
            existing_result = SubredditData.objects.get(subreddit_name=subreddit_name, name=subreddit_data['name'])
            response_data.append({
                'selftext': existing_result.selftext,
                'author_fullname': existing_result.author_fullname,
                'title': existing_result.title,
                'name': existing_result.name,
                'upvote_ratio': existing_result.upvote_ratio,
                'score': existing_result.score,
                'author': existing_result.author,
                'subreddit_subscribers': existing_result.subreddit_subscribers
            })
        except SubredditData.DoesNotExist:
            # Save the new subreddit data in the database
            new_subreddit_data = SubredditData.objects.create(**subreddit_data)
            response_data.append({
                'selftext': new_subreddit_data.selftext,
                'author_fullname': new_subreddit_data.author_fullname,
                'title': new_subreddit_data.title,
                'name': new_subreddit_data.name,
                'upvote_ratio': new_subreddit_data.upvote_ratio,
                'score': new_subreddit_data.score,
                'author': new_subreddit_data.author,
                'subreddit_subscribers': new_subreddit_data.subreddit_subscribers
            })

    return Response(response_data)
from leads.models import Tweet
# @csrf_exempt
# def delete_duplicates(request):
#     if request.method=='GET':
#         stored_tweets = Tweet.objects.all().values()
#         df = pd.DataFrame.from_records(stored_tweets)
#         intent=pkl.load(open("model/intent_classification.pkl","rb"))
#         intent_tfidf=pkl.load(open("model/intent_classification_tfidf.pkl","rb"))
#         def predict_intent(s):
#             s=[s]
#             d=intent.predict(intent_tfidf.transform(s))
#             if d[0][0] == 1:
#                 return "enquiry"
#             elif d[0][1] == 1:
#                 return "general talk"
#             else:
#                 return "complaint"
#         df["intent"] = df["full_text"].apply(predict_intent)
#         value_counts = df["intent"].value_counts()
#         leads = []
#         for index, row in df.iterrows():
#             print(row['intent'])
#             if row['intent'] == 'enquiry':
#                 leads.append((row['screen_name'], row['location']))
#         for lead in leads:
#             username = lead[0]
#             location = lead[1]
#             handled_by = None  # Replace 'Your Employee Name' with the appropriate employee name or query
#             if not Lead.objects.filter(username=username).exists():
#                 lead_obj = Lead.objects.create(username=username, location=location, status='new', handled_by=handled_by)
#                 lead_obj.save()
#         return JsonResponse("Data saved succesfully", safe=False)

@csrf_exempt
def get_tweets(request):
    if request.method=="POST":
        data = json.loads(request.body.decode('utf-8'))
        keyword = data.get('keyword', '')
        count = data.get('count', '100')  # Default count is set to 20 if not provided
        until = data.get('until')  # Optional parameter 'until' for the date filter

        url = "https://twitter135.p.rapidapi.com/v1.1/SearchTweets/"
        querystring = {"q": keyword, "count": count}

        if until:
            querystring['until'] = until

        headers = {
            # 'X-RapidAPI-Key': 'cc8d44e175mshcaabe692fb45fc0p104c66jsn0762ffe8c38b',
            # 'X-RapidAPI-Host': 'twitter135.p.rapidapi.com'
            'X-RapidAPI-Key': '7e7d825c09mshdf576f7bb75175ep1418b5jsnb9d3d7ad6763',
            'X-RapidAPI-Host': 'twitter135.p.rapidapi.com'
        }

        response = requests.get(url, headers=headers, params=querystring)
        print(response)
        data = response.json()
        print(data)

        tweets = []
        for status in data.get('statuses', []):
            tweet = {
                'created_at': status.get('created_at', ''),
                'full_text': status.get('full_text', ''),
                'user': {
                    'name': status['user'].get('name', ''),
                    'screen_name': status['user'].get('screen_name', ''),
                    'location': status['user'].get('location', ''),
                    'followers_count': status['user'].get('followers_count', 0),
                    'friends_count': status['user'].get('friends_count', 0),
                },
                'lang': status.get('lang', ''),
            }
            tweets.append(tweet)

            # Store the tweet data in the database
            Tweet.objects.create(
                keyword=keyword,
                created_at=status.get('created_at', ''),
                full_text=status.get('full_text', ''),
                user_name=status['user'].get('name', ''),
                screen_name=status['user'].get('screen_name', ''),
                location=status['user'].get('location', ''),
                followers_count=status['user'].get('followers_count', 0),
                friends_count=status['user'].get('friends_count', 0),
                lang=status.get('lang', ''),
            )
            

        # Retrieve all stored tweets from the database
        stored_tweets = Tweet.objects.all().values()
        
        
        df = pd.DataFrame(data['statuses'])
        print(df.head())
        
        #intent anaylsis
        intent=pkl.load(open("/anush/Projects/hackrx4.0/Service Classification/model/intent_classification.pkl","rb"))
        intent_tfidf=pkl.load(open("/anush/Projects/hackrx4.0/Service Classification/model/intent_classification_tfidf.pkl","rb"))
        def predict_intent(s):
            s=[s]
            d=intent.predict(intent_tfidf.transform(s))
            if d[0][0] == 1:
                return "enquiry"
            elif d[0][1] == 1:
                return "general talk"
            else:
                return "complaint"
        df["intent"] = df["full_text"].apply(predict_intent)
        value_counts = df["intent"].value_counts()
        leads = []
        for index, row in df.iterrows():
            print(row['intent'])
            if row['intent'] == 'enquiry':
                leads.append((row['user']['screen_name'], row['user']['location']))
        
        #sentiment       
        sentiment=pkl.load(open("/anush/Projects/hackrx4.0/Service Classification/model/sentiment_clf.pkl","rb"))
        sentiment_tfidf=pkl.load(open("/anush/Projects/hackrx4.0/Service Classification/model/sentiment_tfidf.pkl","rb"))
        def predict_sentiment(s):
            s=[s]
            d=sentiment.predict(sentiment_tfidf.transform(s))
            if d[0]==1:
                return "positive"
            else:
                return "negative"
        df["sentiment"]=df["full_text"].apply(lambda x:predict_sentiment(x))
        for index, row in df.iterrows():
            print(row['sentiment'])
            if row['sentiment'] == 'positive':
                leads.append((row['user']['screen_name'], row['user']['location']))
        
        
        for lead in leads:
            username = lead[0]
            location = lead[1]
            handled_by = None  # Replace 'Your Employee Name' with the appropriate employee name or query
            if not Lead.objects.filter(username=username).exists():
                lead_obj = Lead.objects.create(username=username, location=location, status='new', handled_by=handled_by)
                lead_obj.save()
        
        
        
        return JsonResponse({'tweets': tweets, 'stored_tweets': list(stored_tweets)})
    if request.method=="GET":
        stored_tweets = Tweet.objects.all().values()
        return JsonResponse({'stored_tweets': list(stored_tweets)})

def convert_dict_to_csv(data_dict):
    # Get the keys from the dictionary
    keys = list(data_dict.keys())

    # Specify the temporary file path to save the CSV file
    temp_file_path = "/path/to/temporary/file.csv"

    # Convert the dictionary to a list of rows
    rows = [keys]
    for values in zip(*[map(str, value) for value in data_dict.values()]):
        rows.append(values)

    # Save the rows to the temporary CSV file
    with open(temp_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

    # Return the temporary file path
    return temp_file_path


import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from leads.models import FacebookPost
from facebook_scraper import get_posts

@csrf_exempt
def scrape_facebook_page(request):
    if request.method == 'POST':
        data = request.POST
        page_url = data.get('page_url', '')

        # Scrape Facebook page data
        posts = []
        print(get_posts(page_url, pages=5, lang='en', extra_info=True))
        for post in get_posts(page_url, pages=5, lang='en', extra_info=True):  # Specify the number of pages to scrape
            post_data = {
                'account_name': post['username'],
                'post_content': post['text'],
                'likes': post['likes'],
                'comments': post['comments'],
                'shares': post['shares'],
            }
            posts.append(post_data)
            print(post_data)

            # Store the post data in the database
            FacebookPost.objects.create(**post_data)

        # Retrieve all stored Facebook posts from the database
        stored_posts = list(FacebookPost.objects.all().values())

        return JsonResponse({'new_posts': posts, 'stored_posts': stored_posts})

    return JsonResponse({'message': 'Invalid request method'})


@csrf_exempt
def save_posts(request):
    if request.method == 'POST':
        # data = json.loads(request.body.decode('utf-8'))
        combined_json = [
  {
    "account_name": "Bajaj Allianz life insurance",
    "post_content": "Public · 817 members · 5 posts a week\n\n*BAJAJ ALLIANZ LIFE INSURANCE INVESTMENT PLANS AND BENEFITS* • tax benefits & Saving • Family Protection • child Education/ Marriage plan • Retirement plan • returns getting is guaranted *My solution is guaranteed for life* - Guaranted returns - safety of money - liquidity options - Pension for lifetime - joint life with cash back - high returns U can Attach *MWPA ( MARRIED WOMEN PROPERTY ACT)* > ADVANTAGES:- • Wife & childrens • Money get secured againts banks, courts and creditors attachment *It is covered under section 80C and 10 (10D)* For More Details Contact 📲 *Mr. Sanket Kadam :- 9892639513* 🏠 *𝐒𝐓𝐀𝐘 𝐇𝐎𝐌𝐄 𝐒𝐓𝐀𝐘 𝐒𝐀𝐅𝐄* 🏠",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Bajaj Allianz life Insurance co.Ltd",
    "post_content": "Public · 136 members · 5 posts a week\n\nUrgently Required For The Post of Insurance Consultant for Bajaj Allianz Pvt Ltd. For more details Comments Me.",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Bajaj Allianz life insurance",
    "post_content": "Public · 74 members · 7 posts a month\n\nBajaj Allianz life insurance Hum apke sath h Humare sath jud kar kaam karene ke liye contact jariye ...... Ek better plan kariye apne aour apni family � ke sath sath.... Ek Good Earing �",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Kalyan Dombivali Thane Job Opportunity",
    "post_content": "DP Singh\n3 days ago\n\nBajaj Group Company\nUrgent Recruitment\n25 Male And Female Candidates… See more",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Arun Saxena",
    "post_content": "23 June at 10:00\n\nBuy today Bajaj Allianz life insurance company Plans for enquiry call me at 98106 87681",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Vrushi property's is in India.",
    "post_content": "23 June at 15:59\n\nBAJAJ ALLIANZ LIFE INSURANCE\nINTERESTED CALL ME 082915 41823 📞\nBEST INVESTMENT FOR LIFE\nVrushi property's\nProperty company",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Banuka Gopi",
    "post_content": "2 days ago\n\n# In London (UK) lo Naku \"Bajaj Allianz Life Insurance co Ltd\" Naku vachina Award",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Future life Advisor Group",
    "post_content": "3 July at 13:19\n\nWE ARE HIRING: FINANCIAL ADVISORS / INSURANCE AGENTS For Bajaj Allianz Life insurance company.\n(Part-time/Full-time)\nWHO CAN APPLY … See more",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Bajaj Allianz Association of india",
    "post_content": "Bajaj Allianz Association of india\nCHAT.WHATSAPP.COM\nBajaj Allianz Association of india\nWhatsApp Group Invite",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Er Mohan Sharma",
    "post_content": "3 July at 23:21\n\nGeneral Insurance festival of India(GIFI) conducted by Bajaj Allianz GIC Ltd Pune. Become a member of this grand fest. Thanks everyone for your support..",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Monika Nigam Chauhan",
    "post_content": "a day ago\n\nContact no.-9999437603\nCompany name-:bajaj Allianz Life insurance company\nPost-: retail partner\nSalary 19000+ incentive\nJob details *BAJAJ ALLIANZ LIFE INSURANCE COMPANY* ( *BALIC* ) … See more",
    "keyword": "bajajallianzlifeinsurance"
  }
]

        combined_json=json.dumps(combined_json)
        # Parse the JSON object
        posts_data = json.loads(combined_json)

        # Iterate over the posts and save them
        for post_data in posts_data:
            post = Post(
                account_name=post_data['account_name'],
                post_content=post_data['post_content'],
                keyword=post_data['keyword']
            )
            post.save()

        return JsonResponse({'message': 'Posts saved successfully.'})

    return JsonResponse({'error': 'Invalid request method.'})

def approve_employee_view(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        try:
            employee = Employee.objects.get(id=employee_id)
            employee.is_approved = True
            employee.save()
            return redirect('dashboard')
        except Employee.DoesNotExist:
            return HttpResponse('Employee not found')
    else:
        return HttpResponse('Invalid request method')
from django.conf import settings
import os
from pathlib import Path
@csrf_exempt
def dashboard(request):
    if request.method=="POST":
            form_id = request.POST.get('form_id')
            print(form_id)
            model_folder = settings.BASE_DIR / 'model'
            if form_id == 'emp_req':
                employee_id = request.POST.get('employee_id')
                print(employee_id)
                employee = Employee.objects.get(id=employee_id)
                employee.is_approved = True
                employee.save()
                return JsonResponse("employee approved",safe=False)
            
            else:
                account_name = request.POST.get('account_name')
                form_id = request.POST.get('form_id')
                selected_option = request.POST.get('status')
                print(account_name,form_id,selected_option)
                
                
                Lead.objects.filter(username=account_name).update(status=selected_option)
                lead = Lead.objects.get(username=account_name)
                lead.handled_by.add(form_id)
                print("status changed")
                Employeeob = Employee.objects.get(id=form_id)
            
                leads = Lead.objects.all()
                count_leads = Lead.objects.count()

                
                context= {
                    'username': Employeeob.email,
                    'user_type': "sales",
                    'leads': leads,
                    'id':form_id,
                    'message': "Status Updated",
                    'leads_generated': count_leads
                    }
                return render(request, 'dashboard.html',context=context)
    if request.method=="GET":
            username=request.user
            current_user = request.user
            employee = Employee.objects.get(email=current_user)
            user_type=employee.position
           
            if(user_type=="manager"):
            
                api_url = 'http://127.0.0.1:8000/tweets/'
                response = requests.get(api_url)
                json_data = response.json()
                df = pd.json_normalize(json_data['stored_tweets'])
                print(df.head)
            
                #intent anaylsi
                # base_dir_path = Path(settings.BASE_DIR)
                # model_folder = base_dir_path / 'model'
                intent=pkl.load(open("/Users/harshdhariwal/Desktop/crm_main/hackrx4.0/Service Classification/model/intent_classification.pkl","rb"))
                intent_tfidf=pkl.load(open("/Users/harshdhariwal/Desktop/crm_main/hackrx4.0/Service Classification/model/intent_classification_tfidf.pkl","rb"))
                def predict_intent(s):
                    s=[s]
                    d=intent.predict(intent_tfidf.transform(s))
                    if d[0][0] == 1:
                        return "enquiry"
                    elif d[0][1] == 1:
                        return "general talk"
                    else:
                        return "complaint"
                df["intent"] = df["full_text"].apply(predict_intent)
                value_counts = df["intent"].value_counts()
                # print(df["intent"])
                general=value_counts['general talk']
                complaint=value_counts['complaint']
                enquiry=value_counts['enquiry']
                print("general",general,"complaint",complaint,"enquiry",enquiry)
                link="https://quickchart.io/chart?c={type:'doughnut',data:{labels:['General talk','Complaint','Enquiry'],datasets:[{data:["+str(general)+","+str(complaint)+","+str(enquiry)+"]}]},options:{plugins:{doughnutlabel:{labels:[{text:'550',font:{size:20}},{text:'total'}]}}}}"
                print(link)
                
                
                #sentiment analysis
                sentiment=pkl.load(open("/Users/harshdhariwal/Desktop/crm_main/hackrx4.0/Service Classification/model/sentiment_clf.pkl","rb"))
                sentiment_tfidf=pkl.load(open("/Users/harshdhariwal/Desktop/crm_main/hackrx4.0/Service Classification/model/sentiment_tfidf.pkl","rb"))
                def predict_sentiment(s):
                    s=[s]
                    d=sentiment.predict(sentiment_tfidf.transform(s))
                    if d[0]==1:
                        return "positive"
                    else:
                        return "negative"
                df["sentiment"]=df["full_text"].apply(lambda x:predict_sentiment(x))
                response = df["sentiment"].value_counts()
                positive=response['positive']
                negative=response['negative']
                response_link="https://quickchart.io/chart?c={type:'doughnut',data:{labels:['Positive','Negative'],datasets:[{data:["+str(positive)+","+str(negative)+"]}]},options:{plugins:{doughnutlabel:{labels:[{text:'550',font:{size:20}},{text:'total'}]}}}}"
                print(response_link)

                #service anaylsis
                service=pkl.load(open("/Users/harshdhariwal/Desktop/crm_main/hackrx4.0/Service Classification/model/service_model.pkl","rb"))
                service_tfidf=pkl.load(open("/Users/harshdhariwal/Desktop/crm_main/hackrx4.0/Service Classification/model/service_model_tfidf.pkl","rb"))
                def predict_service(s):
                    s=[s]
                    d=service.predict(service_tfidf.transform(s))
                    if d[0][0]==1:
                        return "EMI"
                    elif d[0][1]==1:
                        return "insurance"
                    elif d[0][2]==1:
                        return "investment"
                    elif d[0][3]==1:
                        return "loan"
                    elif d[0][4]==1:
                        return "savings"
                    else:
                        return "card"
                df["service"]=df["full_text"].apply(lambda x:predict_service(x))
                service=df["service"].value_counts()
                card=service['card']
                emi=service['EMI']
                loan=service['loan']
                investment = service['investment']
                service_link="https://quickchart.io/chart?c={type:'bar',data:{labels:['Cards','EMI','loan','Investment'],datasets:[{label:'This month',data:["+str(card)+","+str(emi)+","+str(loan)+","+str(investment)+"],fill:false,borderColor:'blue'}]}}"
                
                leads = Lead.objects.all()
                count_leads = Lead.objects.count()
                
                #employee joining requests
                req=Employee.objects.filter(is_approved=False)
                

                employee_lead_counts = Employee.objects.annotate(
                    converted_lead_count=Count('lead', filter=Q(lead__status='converted'))
                ).values('name', 'converted_lead_count')
                
                print(employee_lead_counts)

                context= {
                'username': username,
                'user_type': user_type,
                "intent":link,
                "response":response_link,
                "service":service_link,
                "leads": leads,
                "leads_generated": count_leads,
                "employee_req":req,
                "top_performers": employee_lead_counts
                }
            else:
                count_leads = Lead.objects.count()
                leads = Lead.objects.all()
                context= {
                'username': username,
                'user_type': user_type,
                'leads': leads,
                'id': employee.id,
                "leads_generated": count_leads
                }
            return render(request, 'dashboard.html',context=context)

def generateLeads(request):
    current_user = request.user
    employee = Employee.objects.get(email=current_user)
    context={
        "username":current_user,
        "user_type":employee.position}
    
    return render(request, 'generateLeads.html',context=context)

def generateDataForTwitter(request):
    if request.method == "POST":
        keyword = request.POST.get('keywords')
        print("keyword recieved -------",keyword)
        count = 100  # Default count is set to 20 if not provided
        # until = request.POST.get('until') 
        

        url = "https://twitter135.p.rapidapi.com/v1.1/SearchTweets/"
        querystring = {"q": keyword, "count": count}

        # if until:
        #     querystring['until'] = until

        headers = {
            # 'X-RapidAPI-Key': 'cc8d44e175mshcaabe692fb45fc0p104c66jsn0762ffe8c38b',
            # 'X-RapidAPI-Host': 'twitter135.p.rapidapi.com'
            'X-RapidAPI-Key': '7e7d825c09mshdf576f7bb75175ep1418b5jsnb9d3d7ad6763',
            'X-RapidAPI-Host': 'twitter135.p.rapidapi.com'
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        print(data)

        tweets = []
        for status in data.get('statuses', []):
            tweet = {
                'created_at': status.get('created_at', ''),
                'full_text': status.get('full_text', ''),
                'user': {
                    'name': status['user'].get('name', ''),
                    'screen_name': status['user'].get('screen_name', ''),
                    'location': status['user'].get('location', ''),
                    'followers_count': status['user'].get('followers_count', 0),
                    'friends_count': status['user'].get('friends_count', 0),
                },
                'lang': status.get('lang', ''),
            }
            print(tweet)
            tweets.append(tweet)

            # Store the tweet data in the database
            Tweet.objects.create(
                keyword=keyword,
                created_at=status.get('created_at', ''),
                full_text=status.get('full_text', ''),
                user_name=status['user'].get('name', ''),
                screen_name=status['user'].get('screen_name', ''),
                location=status['user'].get('location', ''),
                followers_count=status['user'].get('followers_count', 0),
                friends_count=status['user'].get('friends_count', 0),
                lang=status.get('lang', ''),
            )
            

        # Retrieve all stored tweets from the database
        # stored_tweets = Tweet.objects.all().values()
        
        
        df = pd.DataFrame(data['statuses'])
        print(df.columns)
        if 'statuses' in data and data['statuses']:
        # If the 'statuses' field is not empty, proceed with creating the DataFrame
            df = pd.DataFrame(data['statuses'])
            print(df.columns)
        else:
        # If the 'statuses' field is empty or doesn't exist, handle the error here
           message="No tweets found"
           context={
               'message':message
    
           }
           return redirect('generateDataFromTwitter')
           
        model_folder = settings.BASE_DIR / 'model'
        #intent anaylsis
        intent=pkl.load(open(os.path.join(model_folder, os.path.basename("intent_classification.pkl")),"rb"))
        intent_tfidf=pkl.load(open(os.path.join(model_folder, os.path.basename("intent_classification_tfidf.pkl")),"rb"))
        def predict_intent(s):
            s=[s]
            d=intent.predict(intent_tfidf.transform(s))
            if d[0][0] == 1:
                return "enquiry"
            elif d[0][1] == 1:
                return "general talk"
            else:
                return "complaint"
        df["intent"] = df["full_text"].apply(predict_intent)
        value_counts = df["intent"].value_counts()
        leads = []
        for index, row in df.iterrows():
            print(row['intent'])
            if row['intent'] == 'enquiry':
                leads.append((row['user']['screen_name'], row['user']['location']))
        
        #sentiment       
        service=pkl.load(open(os.path.join(model_folder, os.path.basename("service_model.pkl")),"rb"))
        service_tfidf=pkl.load(open(os.path.join(model_folder, os.path.basename('service_model_tfidf.pkl')),"rb"))
        def predict_service(s):
                    s=[s]
                    d=service.predict(service_tfidf.transform(s))
                    if d[0][0]==1:
                        return "EMI"
                    elif d[0][1]==1:
                        return "insurance"
                    elif d[0][2]==1:
                        return "investment"
                    elif d[0][3]==1:
                        return "loan"
                    elif d[0][4]==1:
                        return "savings"
                    else:
                        return "card"
        df["sentiment"]=df["full_text"].apply(lambda x:predict_service(x))
        for index, row in df.iterrows():
            print(row['sentiment'])
            if row['sentiment'] == 'positive':
                leads.append((row['user']['screen_name'], row['user']['location']))
        
        
        for lead in leads:
            username = lead[0]
            location = lead[1]
            handled_by = None  # Replace 'Your Employee Name' with the appropriate employee name or query
            if not Lead.objects.filter(username=username).exists():
                lead_obj = Lead.objects.create(username=username, location=location, status='new')
                lead_obj.save()
        
        
        
        return redirect('generateDataFromTwitter')
        
    current_user = request.user
    employee = Employee.objects.get(email=current_user)
    context={
        "username":current_user,
        "user_type":employee.position}
    return render(request, "generateDataForTwitter.html",context=context)

def generateDataForInsta(request):
    if request.method=="POST":
                hashtag = request.POST.get('hashtag', '')
                print(hashtag)
                # Retrieve existing results from the database
                existing_results = InstagramPost.objects.filter(hashtag=hashtag)            
                conn = http.client.HTTPSConnection("scraper-api.smartproxy.com")
                payload = json.dumps({
                    "target": "instagram_graphql_hashtag",
                    "url": f"https://www.instagram.com/explore/tags/{hashtag}/",
                    "locale": "en",
                    "geo": "India"
                })
                headers = {
                    'Accept': 'application/json',
                    'Authorization': 'Basic UzAwMDAxMTExMjE6UCRXMTM5YThjMmQwNTM2NTg2MmI5ZTk0Y2IzZjM3NzAzMzJj',
                    'Content-Type': 'application/json'
                }
                conn.request("POST", "/v1/scrape", payload, headers)
                res = conn.getresponse()
                data = json.loads(res.read().decode("utf-8"))
                result = []
                print(res)

                if 'data' in data:
                    data = data['data']
                    if 'content' in data:
                        content = data['content']
                        if content is not None and 'hashtag' in content:
                            hashtag_data = content['hashtag']
                            if 'edge_hashtag_to_media' in hashtag_data:
                                edges = hashtag_data['edge_hashtag_to_media'].get('edges', [])
                                post_links = [f"https://www.instagram.com/p/{edge['node']['shortcode']}/" for edge in edges]

                                # Retrieve existing results
                                for post in existing_results:
                                    result.append({'post_link': post.post_link})

                                # Save new results obtained from the API
                                for link in post_links:
                                    # Check if the data already exists in the model
                                    try:
                                        existing_post = InstagramPost.objects.get(post_link=link)
                                        result.append({'post_link': existing_post.post_link})
                                    except InstagramPost.DoesNotExist:
                                        # Save the new post in the database
                                        new_post = InstagramPost.objects.create(hashtag=hashtag, post_link=link)
                                        result.append({'post_link': new_post.post_link})
                                print(result)

                return redirect('generateDataFromInsta')
        
    current_user = request.user
    employee = Employee.objects.get(email=current_user)
    context={
        "username":current_user,
        "user_type":employee.position}
    return render(request, "generateDataForInsta.html",context=context)
from leads.models import Lead
def dataVisualization(request):
    if request.method=="POST":
        service=request.POST.get('service')
        social_media=request.POST.get('social_media')
        chart=request.POST.get('chart')
        current_user = request.user
        employee = Employee.objects.get(email=current_user)
        leads = Lead.objects.all()
        

        
        context={
            "username":current_user,
            "user_type":employee.position,
            "lead":leads,
            }
        return render(request, "dataVisualization.html",context=context)
        
        
    current_user = request.user
    employee = Employee.objects.get(email=current_user)
    context={
        "username":current_user,
        "user_type":employee.position
        }
    return render(request, "dataVisualization.html",context=context)

def crmConnect(request):
    current_user = request.user
    employee = Employee.objects.get(email=current_user)
    context={
        "username":current_user,
        "user_type":employee.position}
    return render(request, "connect.html",context=context)

def crmMessage(request):
    current_user = request.user
    employee = Employee.objects.get(email=current_user)
    context={
        "username":current_user,
        "user_type":employee.position}
    return render(request, "message.html",context=context)

def sales_analytics(request):
    current_user = request.user
    employee = Employee.objects.get(email=current_user)

    #anaylsis
    new=Lead.objects.filter(status="new").count()
    engaged=Lead.objects.filter(status="engaged",handled_by=employee.id).count()
    qualified=Lead.objects.filter(status="qualified",handled_by=employee.id).count()
    converted=Lead.objects.filter(status="converted",handled_by=employee.id).count()
    lost=Lead.objects.filter(status="lost",handled_by=employee.id).count()
    status_chart="https://quickchart.io/chart?c={type:'bar',data:{labels:['new','engaged','qualified','converted','lost'],datasets:[{label:'This month',data:["+str(new)+","+str(engaged)+","+str(qualified)+","+str(converted)+","+str(lost)+"],fill:false,borderColor:'blue'}]}}"
    
    context={
        "username":current_user,
        "user_type":employee.position,
        "stats":status_chart
    }
    return render(request, "sales_anaylsis.html",context=context)


def todo(request):
    return render(request, "todo.html")

def settings(request):
    current_user = request.user
    employee = Employee.objects.get(email=current_user)
    context={
        "username":current_user,
        "user_type":employee.position
        }

    return render(request, "settings.html",context=context)
from django.contrib.auth.decorators import login_required

@login_required
def change_password_view(request):
    if request.method == 'POST':

        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')


        if not request.user.check_password(current_password):
            return render(request, 'change_password.html', {'error': 'Current password is incorrect.'})

        if new_password != confirm_new_password:
            return render(request, 'change_password.html', {'error': 'New password and confirm new password do not match.'})

        request.user.set_password(new_password)
        request.user.save()


        return redirect('settings')

    return render(request, 'settings.html')