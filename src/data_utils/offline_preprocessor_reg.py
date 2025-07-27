# Please specify names of input csv and output csv here - don't include filepath:
input_csv: str = '____________'
output_csv: str = '____________'

import pandas as pd
import numpy as np
import re
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import ast
from rapidfuzz import fuzz, process
from collections import Counter
from sklearn.preprocessing import StandardScaler
import pickle

def strip_non_english(text: str) -> str:
    match = re.search(r'\n(?:Español|Deutsch|Français|Русский|中文|日本語|한국어)\b', text)
    if match:
        return text[:match.start()].strip()
    return text

def remove_non_english_words(text: str) -> str:
    if not isinstance(text, str):
        return ''
    words = text.split()
    english_words = [word for word in words if all(ord(c)<128 for c in word)]
    return ' '.join(english_words)

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def clean_text(text: str) -> str:
    stop_words = set(stopwords.words('english'))
    lemmatiser = WordNetLemmatizer()

    text = strip_non_english(text)
    text = remove_non_english_words(text)
    tokens = word_tokenize(text)
    tags = pos_tag(tokens)

    cleaned = []
    for word, tag in tags:
        if word.lower() in stop_words:
            continue
        if tag in ['NNP', 'NNPS']:
            continue
        if not tag.startswith(('N', 'J')):
            continue
        tag = get_wordnet_pos(tag)
        if tag is None:
            continue
        lemma = lemmatiser.lemmatize(word.lower(), tag)
        cleaned.append(lemma)

    return ' '.join(cleaned)

def clean_tags(tag_series: pd.Series, top_k: int = 100, similarity_cutoff: int = 90, drop_platform_list = None) -> tuple[list, pd.DataFrame]:
    all_tags = [tag.strip().lower() for sublist in tag_series for tag in sublist if isinstance(tag, str)]

    if drop_platform_list:
        all_tags = [tag for tag in all_tags if not any(p in tag for p in drop_platform_list)]
    
    tag_counts = Counter(all_tags)
    unique_tags = list(tag_counts.keys())

    canonical_map = {}
    used = []

    for tag in unique_tags:
        if used:
            match, score, _ = process.extractOne(tag, used, scorer=fuzz.token_sort_ratio)
            if score >= similarity_cutoff:
                canonical_map[tag] = match
        else:
            canonical_map[tag] = tag
        used.append(tag)

    cleaned_series = [[canonical_map.get(tag.strip().lower(), tag.strip().lower())
                       for tag in sublist if isinstance(tag, str)]
                       for sublist in tag_series]
    
    grouped_counts = Counter([tag for tags in cleaned_series for tag in tags])
    top_tags = set([tag for tag, _ in grouped_counts.most_common(top_k)])

    cleaned_topk_lists = [
        [tag for tag in tags if tag in top_tags]
        for tags in cleaned_series
    ]

    tags_encoded = pd.DataFrame([
        {tag: 1 for tag in tags}
        for tags in cleaned_topk_lists
    ]).fillna(0).astype(int)

    return cleaned_topk_lists, tags_encoded

df = pd.read_csv('../../data/'+input_csv)

df['description_clean'] = df['description_raw'].apply(clean_text)

drop_platform_list = ['steam', 'controller', 'remote', 'achievements', 'sdk', 'valve', 'overlay']
df['tags_list'] = df['tags'].apply(ast.literal_eval)
cleaned_tags, tags_encoded = clean_tags(df['tags_list'], top_k=100, drop_platform_list=drop_platform_list)
df['cleaned_tags'] = cleaned_tags
df['tags_string'] = df['cleaned_tags'].apply(lambda tags: ' '.join(tags))

df['combined_text'] = df['description_clean'] + ' ' + df['tags_string']

df.to_csv('../../data/unvectorised_preprocessed_games.csv', index=False)

vectoriser = TfidfVectorizer(
    min_df=2,
    max_df=0.5,
    max_features=300)
tfidf_matrix = vectoriser.fit_transform(df['combined_text'])
tfidf_array = tfidf_matrix.toarray() # type: ignore

with open('vectoriser.pkl', 'wb') as f:
    pickle.dump(vectoriser, f)

df_output = pd.DataFrame(tfidf_array, columns=vectoriser.get_feature_names_out())

scaler = StandardScaler()
success_raw = df['rating'] * np.log1p(df['ratings_count'] + 0.25 * df['added'])
success = scaler.fit_transform(success_raw.to_numpy().reshape(-1,1)).ravel()

df_output['success'] = success

df_output.insert(0, 'id', df['id'].tolist())

df_output.to_csv('../../data/'+output_csv, index=False)