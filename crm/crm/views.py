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


@api_view(['POST'])
def get_instagram_profile(request):
    username = request.data.get('username', '')
    if not username:
        return JsonResponse({'error': 'Username parameter is missing.'}, status=400)

    conn = http.client.HTTPSConnection("scraper-api.smartproxy.com")
    payload = json.dumps({
        "target": "instagram_profile",
        "url": f"https://www.instagram.com/{username}/",
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

    json_data = json.loads(data)
    response_data = {}

    if "data" in json_data:
        profile_data = json_data["data"]["content"]["account"]

        response_data["username"] = profile_data["username"]
        response_data["verified"] = profile_data["verified"]

        stats_data = json_data["data"]["content"]["stats"]
        response_data["posts"] = stats_data["posts"]
        response_data["followers"] = stats_data["followers"]
        response_data["following"] = stats_data["following"]

        biography_data = json_data["data"]["content"]["biography"]
        response_data["name"] = biography_data["name"]
        response_data["occupation"] = biography_data["occupation"]
        response_data["url"] = biography_data["url"]

        posts_data = json_data["data"]["content"]["posts"]
        response_data["posts"] = [post["href"] for post in posts_data]

        related_accounts_data = json_data["data"]["content"]["relatedAccounts"]
        response_data["related_accounts"] = [account["username"] for account in related_accounts_data]
    else:
        response_data["error"] = "Posts data not found for the account."

    return JsonResponse(response_data)

@csrf_exempt
@require_POST
def get_instagram_stats(request):
    payload = json.loads(request.body)
    post_links = payload.get('post_links', [])

    result = []
    for link in post_links:
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
        
        result.append({'post_link': link, 'comments': extracted_info})
    
    return JsonResponse(result, safe=False)

@api_view(['POST'])
def get_instagram_posts(request):
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

    edges = data['data']['content']['hashtag']['edge_hashtag_to_media']['edges']
    post_links = [f"https://www.instagram.com/p/{edge['node']['shortcode']}/" for edge in edges]
    
    return Response({'post_links': post_links})


@api_view(['POST'])
def get_subreddit_data(request):
    subreddit_name = request.data.get('subreddit_name', '')

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

    children_data = data['data']['content']['data']['children']
    response_data = []

    for child in children_data:
        child_data = child['data']
        response_data.append({
            'selftext': child_data['selftext'],
            'author_fullname': child_data['author_fullname'],
            'title': child_data['title'],
            'name': child_data['name'],
            'upvote_ratio': child_data['upvote_ratio'],
            'score': child_data['score'],
            'author': child_data['author'],
            'subreddit_subscribers': child_data['subreddit_subscribers']
        })

    return Response(response_data)



@csrf_exempt
@require_POST
def get_tweets(request):
    data = json.loads(request.body.decode('utf-8'))
    keyword = data.get('keyword', '')
    count = data.get('count', '20')  # Default count is set to 20 if not provided
    print(keyword, count)
    url = "https://twitter135.p.rapidapi.com/v1.1/SearchTweets/"

    querystring = {"q": keyword, "count": count}

    headers = {
        "X-RapidAPI-Key": "54caaa891bmsh28b30d3e6519382p1e54dejsnb01e24eac7f5",
        "X-RapidAPI-Host": "twitter135.p.rapidapi.com"
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

    return JsonResponse({'tweets': tweets})