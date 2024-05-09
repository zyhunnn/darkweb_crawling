# 필요한 라이브러리 import
import requests
import pandas as pd
import matplotlib.pyplot as plt
import json

# 데이터 분석
class data_analyzer():
    def __init__(self):

        # 리눅스에서 작업할 경우 9050으로 변경해야 함
        self.proxies = {
                "http" : "socks5h://127.0.0.1:9150",
                "https" : "socks5h://127.0.0.1:9150"
        }
    
    # /api/word/ 접근하여 dataframe 생성
    def get_word_counts(self, url):
        response = requests.get(url + "api/word/", proxies=self.proxies)

        print("/api/word : " + str(response.status_code))
        word_df = pd.DataFrame(json.loads(response.content.decode("utf-8")))

        #print(word_df.head())
        # csv 파일로 dataframe 백업
        word_df.to_csv('word_df.csv', index=False)

        return word_df
    
    
    # /api/url/ 접근하여 dataframe 생성
    def get_urls(self, url):
        response = requests.get(url + "api/url/", proxies=self.proxies)

        print("/api/url : " + str(response.status_code))
        url_df = pd.DataFrame(json.loads(response.content.decode("utf-8")))

        # dataframe 5행 출력
        #print(url_df.head())
        # csv 파일로 dataframe 백업
        url_df.to_csv('url_df.csv', index=False)

        return url_df
    
    # csv 파일 읽기(데이터프레임 반환)
    def read_csv_file(self, file):
        df = pd.read_csv(str(file))
        return df
    

    ##### 전처리 ####
    ## date 컬럼 생성(CreatedAt에서 날짜만 추출하여 date라는 새로운 컬럼 만듦)
    def add_column(self, df):
        # createdAt열에서 날짜만 추출
        df['Date'] = pd.to_datetime(df['createdAt']).dt.strftime('%Y-%m-%d-%H')
        return df

    ## 각 사이트 별 상위 5개 단어 추출
    def find_top_5(self, word_df, url_df):
            for url_id in word_df['url'].unique():

                url = self.find_url(url_df, url_id)
                # url_id에 해당하는 url 찾을 수 없으면 건너뛰기
                if url == None:
                    continue

                top_words_df = pd.DataFrame(columns=['url', 'url_id', 'word', 'freq', 'max_count', 'sum_count', 'avg_count'])


                # 특정 사이트 선택
                site_data = word_df[word_df['url'] == url_id]
                
                # 날짜 오름차순 정렬(최근 다섯 개의 날짜만 분석)
                dates = pd.DataFrame(site_data['Date'], columns=['Date'])
                dates = dates.sort_values(by='Date')
                dates = dates['Date'].unique()
                date_list = dates[:] # 날짜 개수 수정

                # 지속적으로 크롤링된 단어들(word count 존재 여부 기준 5회)
                words = site_data['word'].unique()
                for word in words :
                    freq = 0
                    max_count = []

                    try : # 날짜 5개용으로 만들어서 5일이 아니면 오류남
                        d0_w = site_data.loc[(site_data['Date'] == date_list[0]) & (site_data['word'] == word), 'count'].values
                        if len(d0_w) != 0:
                            freq += 1
                            max_count.append(max(d0_w))

                        d1_w = site_data.loc[(site_data['Date'] == date_list[1]) & (site_data['word'] == word), 'count'].values
                        if len(d1_w) != 0:
                            freq += 1
                            max_count.append(max(d1_w))

                        d2_w = site_data.loc[(site_data['Date'] == date_list[2]) & (site_data['word'] == word), 'count'].values
                        if len(d2_w) != 0:
                            freq += 1
                            max_count.append(max(d2_w))

                        d3_w = site_data.loc[(site_data['Date'] == date_list[3]) & (site_data['word'] == word), 'count'].values
                        if len(d3_w) != 0:
                            freq += 1
                            max_count.append(max(d3_w))

                        d4_w = site_data.loc[(site_data['Date'] == date_list[4]) & (site_data['word'] == word), 'count'].values
                        if len(d4_w) != 0:
                            freq += 1
                            max_count.append(max(d4_w))

                    except:
                        pass

                        if freq != 0:
                            record = {'url' : url, 'url_id' : url_id, 'word' : word,
                                            'freq' : freq, 'max_count' : max(max_count), 
                                            'sum_count' : sum(max_count), 'avg_count' : int((sum(max_count)/freq))}
                            top_words_df = top_words_df._append(record, ignore_index=True)
                        else :
                            continue

                # 상위 빈도 5개 단어
                sorted_df = top_words_df.sort_values(by=['freq', 'max_count'], ascending=False)
                word_list = sorted_df['word'][:5].tolist()


                self.print_keyword_graph_per_site(words=word_list, url_id = url_id, url=str(url), date_list=date_list, site_data=site_data)


    ## url id 찾기
    def find_url(self, url_df, url_id):
        url = url_df.loc[url_df['id'] == url_id, 'url'].values
        if len(url) != 0 : 
            return url
        else:
            return None
        
    
    ## 그래프 ##
    # 날짜별 keyword count 수 총계(사이트 구분 안 함)
    def print_total_count(self, word_df):
        # 색상 목록
        colors = plt.cm.tab20.colors

        ## 날짜별 word count
        drop_df = word_df.drop(columns=['url'])
        gr_df = drop_df.groupby(['Date', 'word']).sum().reset_index()
        st_df = gr_df.sort_values(by='count', ascending=False)

        for dt in st_df['Date'].unique():
            # 특정 날짜의 데이터만 선택
            dt_data = st_df[st_df['Date'] == dt]
            
            # 그래프 제목 설정
            plt.figure(figsize=(13, 6))
            plt.title(dt)
            
            # x축에는 단어, y축에는 단어 카운트 값을 설정하여 그래프 생성
            try:
                x_word = dt_data['word'][:15]
                y_count = dt_data['count'][:15]
            except: # 날짜 당 20개 이하의 단어가 크롤링 됨
                x_word = dt_data['word'][:]
                y_count = dt_data['count'][:]                
            plt.bar(x_word, y_count, color=colors[:len(x_word)])
            plt.xlabel('word')
            plt.ylabel('count')
            plt.xticks(rotation=45)  # x축 레이블 회전
            plt.tight_layout()  # 레이아웃 조정
            #plt.show()
            plt.savefig(str(dt) + '_date_count.png')
            #break ## 모든 날짜로 반복하려면 제거하면 됨

    # 한 사이트 당 keyword 날짜 기반 추이 그래프(이건 쓸 수 없는 상태)
    def print_keyword_graph_per_site(self, words, url, date_list, site_data, url_id) :
        line_list = ['solid', 'dashed', 'dotted', 'dashdot', 'solid']

        plt.figure(figsize=(13, 6))
        plt.title(url)
        for i in range(len(words)):
            y_list = []
            for j in range(len(date_list)):
                c_values = site_data.loc[(site_data['Date'] == date_list[j]) & (site_data['word'] == words[i]), 'count'].values
                if len(c_values) != 0:
                    y_list.append(c_values[-1])
                else:
                    y_list.append(0)

            plt.plot(date_list, y_list, label = words[i], linestyle = line_list[i])
        
        plt.legend(loc='upper right')
        
        # x축에는 단어, y축에는 단어 카운트 값을 설정
        plt.xlabel('date')
        plt.ylabel('count')
        plt.xticks(rotation=45)  # x축 레이블 회전
        plt.tight_layout()  # 레이아웃 조정
        plt.savefig(str(url_id) + '_site_count_word.png')


## Main 함수 ##
if __name__ == "__main__":

    file_list = ["word_df.csv", "url.csv"]

    # backend server url 지정
    backend_url = "http://dufjhr6iwoenkalljyy4calxpqcxxe3trs7jymvmyk5dgjobtojbbvqd.onion:8000/"

    da = data_analyzer()
    #word_df = da.get_word_counts(backend_url)
    #url_df = da.get_urls(backend_url)

    word_df = da.read_csv_file("word_df.csv")
    url_df = da.read_csv_file("url_df.csv")

    word_df = da.add_column(word_df)
    url_df = da.add_column(url_df)

    da.find_top_5(word_df=word_df, url_df=url_df)
    da.print_total_count(word_df=word_df)
