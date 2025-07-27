import pandas as pd
import re

def find_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

def find_japanese(text):
    # Regex pattern for Hiragana, Katakana, and Kanji (CJK Ideographs)
    japanese_pattern = re.compile(r'[\u3040-\u30FF\u4E00-\u9FFF]')
    return japanese_pattern.findall(text)

def find_chinese(text):
    # Regex pattern for Chinese characters (CJK Unified Ideographs)
    chinese_pattern = re.compile(r'[\u4E00-\u9FFF]')
    return chinese_pattern.findall(text)

df_grand = pd.read_csv('all_games_raw.csv')

df_grand_1 = df_grand.dropna(subset=['description_raw']).reset_index(drop=True)

language_list = []
for i in range(len(df_grand_1)):
    if find_chinese(df_grand_1.iloc[i,9]) or find_japanese(df_grand_1.iloc[i,9]) or find_cyrillic(df_grand_1.iloc[i,9]):
        language_list.append(i)

df_grand_2 = df_grand_1.drop(language_list).reset_index(drop=True)

count = 0
count_no_ratings = 0
no_ratings = []
for i in range(len(df_grand_2)):
    if df_grand_2.iloc[i,3] == 0:
        count += 1
        if df_grand_2.iloc[i,5] == 0:
            count_no_ratings += 1
            no_ratings.append(i)

df_grand_3 = df_grand_2.drop(no_ratings).reset_index(drop=True)

zero_ratings = []
for i in range(len(df_grand_3)):
    if df_grand_3.iloc[i,3] == 0:
        zero_ratings.append(i)

df_grand_4 = df_grand_3.drop(zero_ratings).reset_index(drop=True)

df_grand_3.to_csv('all_games_with_rating.csv', index=False)
df_grand_4.to_csv('all_games_pos_rating.csv', index=False)

