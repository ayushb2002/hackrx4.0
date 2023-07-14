
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json

driver = webdriver.Edge()
wait = WebDriverWait(driver, 10)

MONTH_DICT = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

YEAR_DICT = {
    '2023': 1,
    '2022': 2,
    '2021': 3,
    '2020': 4,
    '2019': 5,
    '2018': 6
}

driver.get("https://twitter.com/login")
driver.maximize_window()
time.sleep(5)

def web_scrape_from_twitter(driver, num_tweets):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    tweet_cursor = soup.find_all('div', class_='css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu', limit=num_tweets)
    store = {}
    i = 0
    for divisions in tweet_cursor:
        tweet_spans = divisions.find_all('span', class_='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0') 
        tweet_data = []
        for spans in tweet_spans:
            tweet_data.append(spans.text)
        data = {
            'name': tweet_data[0],
            'username': tweet_data[1],
            'tweet': ' '.join(tweet_data[2:]) 
        }
        
        store[i] = data
        i += 1
        
    return store

def store_json(data):
    try:
        with open('result.json', 'w') as f:
            json.dump(data, f)
    except:
        return False
        
    return True

def fetch_from_twitter(driver=None, username=None, password=None, must_keywords=None, advanced_search_flag=False, optional_keywords=None, hashtags=None, from_month=None, to_month=None, from_year=None, to_year=None, account=None, num_tweets=10):
    
    if not driver or not username or not password or not must_keywords:
        return {}
    
    #username
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'))).send_keys(username)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]'))).click()
    time.sleep(3)

    # password
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'))).send_keys(password)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div'))).click()
    time.sleep(3)

    # keyword search
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input'))).send_keys(must_keywords)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input'))).send_keys(Keys.RETURN)
    time.sleep(3)

    if advanced_search_flag:
        # advanced search starts here
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/a'))).click()
        
        # must keywords
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div/label/div/div[2]/div/input'))).send_keys(must_keywords)
        
        # optional keywords
        if optional_keywords:
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div/label/div/div[2]/div/input'))).send_keys(optional_keywords)
        
        # hashtags
        if hashtags:
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[5]/div/label/div/div[2]/div/input'))).send_keys(hashtags)
        
        # account
        if account:
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/label/div/div[2]/div/input'))).send_keys(account)
        
        # from_month
        if from_month:
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[16]/div/div[2]/div/div[1]/select'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[16]/div/div[2]/div/div[1]/select/option[{MONTH_DICT.get(from_month)+1}]'))).click()
            
        # from_year
        if from_year:
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[16]/div/div[2]/div/div[3]/select'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[16]/div/div[2]/div/div[3]/select/option[{YEAR_DICT.get(from_year)+1}]'))).click()
            
        # to_month
        if to_month:
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[16]/div/div[4]/div/div[1]/select'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[16]/div/div[4]/div/div[1]/select/option[{MONTH_DICT.get(to_month)+1}]'))).click()
            
        # to_year
        if to_year:
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[16]/div/div[4]/div/div[3]/select'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[16]/div/div[4]/div/div[3]/select/option[{YEAR_DICT.get(to_year)+1}]'))).click()
        
        # search button for advanced search
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[3]/div'))).click()
        time.sleep(3)
        # advanced search ends here
    
    # shift from top to latest
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a'))).click()
    time.sleep(3)

    for _ in range(num_tweets//5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # use beautiful soup to retrieve data 
    data = web_scrape_from_twitter(driver=driver, num_tweets=num_tweets)

    time.sleep(3)
    driver.quit()
    
    success = store_json(data)
    return success

twitter_username = 'GithubArchs'
twitter_password = 'githubArchitectsForLife'
must_keywords = 'cards bajaj finserv'
optional_keywords = ''
from_year = '2021'
to_year = '2022'
from_month = ''
to_month = ''
account = ''
hashtags = ''
adv_flag = True

print(fetch_from_twitter(driver=driver, username=twitter_username, password=twitter_password, must_keywords=must_keywords, optional_keywords=optional_keywords, from_year=from_year, to_year=to_year, account=account, from_month=from_month, to_month=to_month, hashtags=hashtags, num_tweets=30, advanced_search_flag=adv_flag))