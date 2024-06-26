from .models import *
from rest_framework import generics
from rest_framework.response import Response
from .serializers import URLSerializer, wordSerializer
from rest_framework.permissions import AllowAny
from urllib.parse import urlparse
from django_cron import CronJobBase, Schedule
import traceback
from bs4 import BeautifulSoup
import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter


class preprocess_data:
    def __init__(self, data):
        self.data = data
        self.match_datatype()

    def match_datatype(self):
        if type(self.data) != 'str':
            self.data = self.data.text
    
    def normalize_data(self, vocab_size):
        words = []

        # tokenizing and cleaning
        word_tokens = word_tokenize(self.data)
        stop_words = set(stopwords.words('english'))
        
        for word in word_tokens:
            word = word.lower()
            if (word not in stop_words) and (len(word) > 2):
                words.append(word)
        
        # left lemma
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word in words]
        
        # left nouns
        word_tag_pairs = nltk.pos_tag(words, tagset='universal')
        words = [word for (word, tag) in word_tag_pairs if tag == 'NOUN']
        
        # count words
        vocab = Counter(words)

        # create a word list with word counts
        words_to_db = vocab.most_common(vocab_size)
        words_to_db = dict(words_to_db)
        
        return words_to_db


      

        
# # 하루에 한 번 크롤링 함수 실행
# class DailyTask(CronJobBase):
#     # 24시간
#     # RUN_EVERY_MINS = 1440

#     # schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'api.daily_task'

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')

            
def schedule_job() :
    def crawling(url, start_url, depth, target_depth, visited, keyword, prev_url):

        print(f"{url}_crawl")

        if url in visited:
            return
        
        visited.append(url)
        
        proxies = {
                    "http" : "socks5h://127.0.0.1:9050",
                    "https" : "socks5h://127.0.0.1:9050"
                }
        
        if depth == target_depth:
            try:
                response = requests.get(url, proxies=proxies, allow_redirects=True)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, "html.parser")
                
                existing_url = URL.objects.filter(url=url).first()

                if existing_url:
                    existing_url.save()
                else:
                    title = str(soup.title)
                    title = title.replace("<title>","").replace("</title>", "").strip()
                    
                    parsed_url = urlparse(url)
                    domain = parsed_url.netloc
                    parameters = parsed_url.query
                    URL.objects.create(keyword=keyword, url=url, domain=domain, parameters=parameters, title=title, prev_url=prev_url)
                

                html_data = preprocess_data(soup)
                word_count_pair = html_data.normalize_data(30)

                url_id = URL.objects.filter(url=url).first()

                for word,count in word_count_pair.items():
                    # url_id = URL.objects.filter(url=url).first()
                    # existing_word = word_count.objects.filter(url=url_id, word=word).first()

                    # if existing_word:
                    #     existing_word.count = count
                    #     existing_word.save()
                    #     continue
                    word_count.objects.create(keyword=keyword, url=url_id, word=word, count=count)
                    
                    
                
            except Exception as e:
                print(traceback.format_exc())
            return
        
        try:
            response = requests.get(url, proxies=proxies, allow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link['href']
                
                if not href.startswith('http'):
                    if href.startswith('/'):
                        href = url + href
                    else:
                        href = url + "/" + href
                        
                elif not href.startswith(start_url):
                    continue

                prev_url = url
                
                crawling(href, start_url, depth + 1, target_depth, visited, keyword, prev_url)
                
        
        except Exception as e:
            print(traceback.format_exc())
        
    print("before_crawl")

    base_url = "https://ahmia.fi/search/?q="
    keywords = ['drug', 'exploits', 'weapon', 'bangers', 'scam', 'fakes', 'carding', 'counterfeit', 'gambling']
    prev_url = 'https://ahmia.fi/'

    for keyword in keywords:
        url = base_url + keyword
        crawling(url, url, 0, 1, [], keyword, prev_url)

# url api
class url_List(generics.ListCreateAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset=URL.objects.all()
        return queryset
    
    def create(self, request, *args, **kwargs):

        keyword = request.data.get('keyword')
        url = request.data.get('url')
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        parameters = parsed_url.query
        title = request.data.get('title')
        prev_url = request.data.get('prev_url')

        existing_url = URL.objects.filter(url=url).first()

        if existing_url:
            existing_url.save()
            serializer = self.get_serializer(existing_url)
            return Response(serializer.data)

        new_url = URL.objects.create(keyword=keyword, url=url, domain=domain, parameters=parameters, title=title, prev_url=prev_url)
        serializer = self.get_serializer(new_url)
        return Response(serializer.data)


# word api
class Word_List(generics.ListCreateAPIView):
    queryset = word_count.objects.all()
    serializer_class = wordSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.kwargs.get('url_id'):
            return word_count.objects.filter(url=self.kwargs.get('url_id'))
        return word_count.objects.all()
    
    def create(self, request, *args, **kwargs):
        keyword = request.data.get('keyword')
        url = request.data.get('url')
        word = request.data.get('word')
        count = request.data.get('count')

        existing_word = word_count.objects.filter(url=url, word=word).first()
        url_id = URL.objects.filter(url=url)
        word_count.objects.create(keyword=keyword, url=url_id, word=word, count=count)
        # if existing_word:
            # existing_word.count = count
            # existing_word.save()
            # serializer = self.get_serializer(existing_word)
            # return Response(serializer.data)

        # return super().create(request, *args, **kwargs)
        new_word_count = word_count.objects.create(keyword=keyword, url=url_id, word=word, count=count)
        serializer = self.get_serializer(new_word_count)
        return Response(serializer.data)
