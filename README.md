# 다크웹 크롤링 시각화

## 설치
```
$ git clone https://github.com/zyhunnn/darkweb_crawling

$ cd darkweb_crawling

$ pip install -r requirements.txt

$ python manage.py makemigrations

$ python manage.py migrate

$ python manage.py runserver
```

## API DOCUMENT

|REST 명령어|주소|설명|필요입력값|
|----------|---|---|------------|
|GET|api/url/|URL DB 출력|없음|
|GET|api/word/|word DB 출력|없음|
|GET|api/word/<int:url_id>/|특정 url의 word DB 출력|없음|
|POST|api/url/|URL 저장|url: 주소, title: 타이틀|
|POST|api/word/|word 저장|url: url id 값, word: 단어, count: 단어 개수|