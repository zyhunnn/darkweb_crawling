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
