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

@csrf_exempt
@require_POST
def get_tweets(request):
    data = json.loads(request.body.decode('utf-8'))
    keyword = data.get('keyword', '')
    count = data.get('count', '100')  # Default count is set to 20 if not provided
    until = data.get('until')  # Optional parameter 'until' for the date filter

    url = "https://twitter135.p.rapidapi.com/v1.1/SearchTweets/"
    querystring = {"q": keyword, "count": count}

    if until:
        querystring['until'] = until

    headers = {
        'X-RapidAPI-Key': 'cc8d44e175mshcaabe692fb45fc0p104c66jsn0762ffe8c38b',
        'X-RapidAPI-Host': 'twitter135.p.rapidapi.com'
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

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

    return JsonResponse({'tweets': tweets, 'stored_tweets': list(stored_tweets)})


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



def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def generateLeads(request):
    return render(request, 'generateLeads.html')

def generateData(request):
    return render(request, "generateData.html")

def dataVisualization(request):
    return render(request, "dataVisualization.html")

def crmConnect(request):
    return render(request, "connect.html")

def crmMessage(request):
    return render(request, "message.html")
