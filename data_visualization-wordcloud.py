from wordcloud import WordCloud
import pandas as pd

def generate_wordcloud(dataframe, output_filename):
    """
    DataFrame을 입력받아 WordCloud를 생성하고 이미지 파일로 저장하는 함수.

    :param dataframe: WordCloud를 생성할 DataFrame
    :param output_filename: WordCloud 이미지를 저장할 파일명
    """
    # word의 개수 합산하여 집계
    word_counts = dataframe.groupby('Word')['count'].sum().reset_index()

    # WordCloud 생성
    img_wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(zip(word_counts['Word'], word_counts['count'])))

    # 이미지 파일로 저장
    img_wordcloud.to_file(output_filename)
    print(f"WordCloud 이미지가 '{output_filename}' 파일로 저장되었습니다.")

# 예시로 사용할 DataFrame 생성
column_name = ['onion', 'Word', 'count', 'DateTime']
df = pd.read_csv("output.csv")
data = df.values.tolist()
new_df = pd.DataFrame(data, columns=column_name)
new_df['Date'] = pd.to_datetime(new_df['DateTime']).dt.strftime('%Y-%m-%d')

# 함수 호출
generate_wordcloud(new_df, "output.jpg")



def generate_wordcloud_by_date(dataframe, target_date, output_filename):
    """
    날짜를 기준으로 DataFrame을 필터링하여 WordCloud를 생하고 이미지 파일로 저장하는 함수.

    :param dataframe: WordCloud를 생성할 DataFrame
    :param target_date: WordCloud를 생성할 날짜 (YYYY-MM-DD 형식의 문자열)
    :param output_filename: WordCloud 이미지를 저장할 파일명
    """
    try:
        # 입력받은 날짜를 datetime 형식으로 변환
        target_date = pd.to_datetime(target_date).date()

        # 입력받은 날짜에 해당하는 데이터만 필터링
        filtered_data = dataframe[pd.to_datetime(dataframe['DateTime']).dt.date == target_date]

        if not filtered_data.empty:
            # 날짜별로 단어 수를 합산하여 집계
            word_counts = filtered_data.groupby('Word')['count'].sum().reset_index()

            # WordCloud 생성
            img_wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(zip(word_counts['Word'], word_counts['count'])))

            # 이미지 파일로 저장
            img_wordcloud.to_file(output_filename)
            print(f"{target_date} 날짜의 WordCloud 이미지가 '{output_filename}' 파일로 저장되었습니다.")
        else:
            print("선택한 날짜에 해당하는 데이터가 없습니다.")
    except ValueError:
        print("올바른 날짜 형식을 입력하세요.")

# 예시로 사용할 DataFrame 생성
column_name = ['onion', 'Word', 'count', 'DateTime']
df = pd.read_csv("output.csv")
data = df.values.tolist()
new_df = pd.DataFrame(data, columns=column_name)
new_df['Date'] = pd.to_datetime(new_df['DateTime']).dt.strftime('%Y-%m-%d')

# 함수 호출 (예시: "2024-05-01" 날짜에 대한 WordCloud 생성)
input_date = '2024-02-05'
generate_wordcloud_by_date(new_df, input_date, f"output_{input_date}.jpg")