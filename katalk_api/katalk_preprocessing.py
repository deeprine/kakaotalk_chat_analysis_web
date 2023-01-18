from sanic import Sanic
from sanic.response import json
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
from collections import Counter
import os
import time
import json

import re
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from konlpy.tag import Okt

from utils import message_util as msg_util

import requests
import asyncio
import logging.config
import argparse

from datetime import datetime
from time import gmtime, strftime, localtime

logging.config.fileConfig('./configs/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

week_han = {'0' : '월요일',
            '1' : '화요일',
            '2' : '수요일',
            '3' : '목요일',
            '4' : '금요일',
            '5' : '토요일',
            '6' : '일요일'}

def kakaotalk_api(txt_name):
    """
    메인
     
    :return: 분석된 딕셔너리 값을 api로 보낸다
    """
    try:
        try:
            df, title = katalk_msg_parse(txt_name)
        except:
            df, title = katalk_msg_parse_mobile(txt_name)

        user_unique = df['user_name'].unique().tolist()
        print(user_unique)
        ratio_katalk_dict = ratio_katalk(df)
        day_dict = many_katalk(df)
        user_day_dict = user_many_katalk(df)
        continue_dict = get_continue_day_num(df)
        ratio_pic_dict = ratio_pic(df)
        ratio_emo_dict = ratio_emo(df)

        if len(user_unique) <= 2:
            speech_dict = pos_counter(df)
            df['text'] = df['text'].apply(lambda x: hangul_tokenizer(x))
            topic_dict = tfidf_LDA(df)
        else:
            speech_dict = {}
            topic_dict = {}

        output = {'ratio_katalk_dict' : ratio_katalk_dict,
                  'day_dict' : day_dict,
                  'user_day_dict' : user_day_dict,
                  'continue_dict' : continue_dict,
                  'ratio_pic_dict' : ratio_pic_dict,
                  'ratio_emo_dict' : ratio_emo_dict,
                  'topic_dict' : topic_dict,
                  'speech_dict' : speech_dict
                  }

    except Exception as e:
        mtUtils.printError(e, logger)
        print(repr(e))
        print('An error as above occurs when processing the images, please check it')
        result = msg_util.get_error('', e)
        return result
    except KeyboardInterrupt as e:
        mtUtils.printError(e, logger)
        # Thread won't be killed when press Ctrl+C
        result = msg_util.get_error('', "KeyboardInterrupt")
        return result

    return output, title, user_unique

def get_clock(morning_afternoon, clock):
    if morning_afternoon == '오후':
        process_clock = int(clock.split(':')[0]) + 12
        if process_clock == 24:
            process_clock = '00'
        process_clock = str(process_clock) + ":" + str(clock.split(':')[1])
    elif morning_afternoon == '오전':
        if len(clock.split(':')[0]) == 1:
            process_clock = '0' + str(clock.split(':')[0])
        else:
            process_clock = clock
    return process_clock

def katalk_msg_parse_mobile(file_path):
    my_katalk_data = list()
    date_info = "[0-9]{4}년 [0-9]{1,2}월 [0-9]{1,2}일 오\S [0-9]{1,2}:[0-9]{1,2}"

    for idx, line in enumerate(open(file_path, 'r', encoding='UTF8')):
        if idx == 0:
          title = line # 상대방 이름
        if line == '\n':
            continue
        elif re.match(date_info, line):
            try:
                line = line.split(",")
                if len(line) > 1:
                    times = line[0].split(" ")

                    morning_afternoon = times[-2]
                    clock = times[-1]
                    year = times[0]
                    month = '0' + str(times[1]) if len(times[1]) == 2 else times[1]
                    days = '0' + str(times[2]) if len(times[2]) == 2 else times[2]

                    date_time = year + month + days + get_clock(morning_afternoon, clock)
                    date_time = re.sub("[가-힣]", ' ', date_time)

                    user_text = line[1].split(" : ", maxsplit=1)
                    user_name = user_text[0].strip()
                    text = user_text[1].strip()
                    my_katalk_data.append({'date_time': date_time,
                                           'user_name': user_name,
                                           'text': text
                                           })
                else:
                    pass
            except:
                pass

        else:
            if len(my_katalk_data) > 0:
                my_katalk_data[-1]['text'] += "\n" + line.strip()

    my_katalk_df = pd.DataFrame(my_katalk_data)
    my_katalk_df['date_time'] = pd.to_datetime(my_katalk_df['date_time'])
    my_katalk_df['year_month'] = my_katalk_df.date_time.map(lambda x: x.strftime('%Y-%m'))
    my_katalk_df['year_month_day'] = my_katalk_df.date_time.map(lambda x: x.strftime('%Y-%m-%d'))
    my_katalk_df['hour'] = my_katalk_df.date_time.dt.hour
    my_katalk_df['year'] = my_katalk_df.date_time.dt.year
    my_katalk_df['week_day_num'] = my_katalk_df['date_time'].dt.weekday
    my_katalk_df['week_day'] = my_katalk_df['date_time'].dt.weekday.map(lambda x: week_han[str(x)])

    return my_katalk_df, title

def katalk_msg_parse(file_path):
    """
    카톡메세지를 데이터프레임 형태로만든다

    :return: 카톡 데이터프레임
    """
    my_katalk_data = list()
    katalk_msg_pattern = "[가-힣a-zA-Z0-9]* [가-힣]{2} [0-9]* [가-힣a-zA-Z0-9]*"
    date_info = " [0-9]{4}년 [0-9]{1,2}[월] [0-9]{1,2}[일] [가-힣]{3}"
    for idx, line in enumerate(open(file_path, 'r', encoding='UTF8')):
        if idx == 1 or idx == 2:
            continue
        line = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]','', line)
        line_list = line.split()
        if idx == 0:
          title = line # 상대방 이름
          # opponent = line_list[0] # 상대방 이름
          continue

        elif idx == 5:
          continue

        elif re.match(date_info, line):
          weekday = line_list[3]
          date_foward = re.sub("[가-힣]", '', line)
          line_list = date_foward.split()

          if len(line_list[1]) == 1:
            line_list[1] = '0'+line_list[1]
          if len(line_list[2]) == 1:
            line_list[2] = '0'+line_list[2]
          date_foward = line_list[0] + line_list[1] + line_list[2]
          continue

        elif line == '':
            continue

        elif re.match(katalk_msg_pattern, line):
          if line_list[1] == '오후':
            clock = str(int(line_list[2][:-2]) + 12)
            if clock == '24':
              line_list[2] = '00' + line_list[2][-2:]
            else:
              line_list[2] = clock + line_list[2][-2:]

          if line_list[1] == '오전':
            if len(line_list[2]) == 3:
              line_list[2] = '0'+line_list[2]

          date_time = date_foward.strip() + line_list[2].strip()

          user_name = line_list[0]
          if len(line_list) == 4:
            kakao_txt = line_list[3]
          else:
            continue

          my_katalk_data.append({'date_time': date_time,
                                  'week_day' : weekday,
                                  'user_name': user_name,
                                  'text': kakao_txt
                                  })
        else:
            if len(my_katalk_data) > 0:
                my_katalk_data[-1]['text'] += "\n"+line.strip()

    my_katalk_df = pd.DataFrame(my_katalk_data)
    my_katalk_df['date_time'] = pd.to_datetime(my_katalk_df['date_time'])
    my_katalk_df['year_month'] = my_katalk_df.date_time.map(lambda x: x.strftime('%Y-%m'))
    my_katalk_df['year_month_day'] = my_katalk_df.date_time.map(lambda x: x.strftime('%Y-%m-%d'))
    my_katalk_df['year'] = my_katalk_df.date_time.dt.year
    my_katalk_df['week_day_num'] = my_katalk_df['date_time'].dt.weekday
    my_katalk_df['hour'] = my_katalk_df.date_time.dt.hour
    return my_katalk_df, title

def ratio_katalk(df):
  """
  나와 상대방의 카톡 메세지 비율을 반환

  :return: 딕셔너리 형태의 카톡메세지 비율
  """
  ratio_dict = dict()
  ratio_username = df['user_name'].value_counts().index.tolist()
  ratio_num = df['user_name'].value_counts().tolist()
  for num, name in zip(ratio_num, ratio_username):
    user_ratio = (num / sum(ratio_num)) * 100
    ratio_dict[name] = user_ratio
  return ratio_dict

# 제일 대화를 많이한 년월, 년월일, 시간대, 요일
def many_katalk(df):
  """
  대화를 많이한 년월, 년월일, 시간대, 요일
  
  :param df: 
  :return: 딕셔너리 형태의 값
  """
  day_dict = dict()
  many_weekday = df['week_day'].value_counts().index
  many_year_month = df['year_month'].value_counts().index[:10]
  many_year_month_day = df['year_month_day'].value_counts().index[:10]
  many_hour = df['hour'].value_counts().index

  day_dict['요일'] = many_weekday.tolist()
  day_dict['년월'] = many_year_month.tolist()
  day_dict['년월일'] = many_year_month_day.tolist()
  day_dict['시간'] = many_hour.tolist()

  day_dict['요일_num'] = df['week_day'].value_counts().tolist()
  day_dict['년월_num'] = df['year_month'].value_counts().tolist()[:10]
  day_dict['년월일_num'] = df['year_month_day'].value_counts().tolist()[:10]
  day_dict['시간_num'] = df['hour'].value_counts().tolist()
  return day_dict


def user_many_katalk(df):
    user_list = df['user_name'].unique().tolist()
    user_day_dict = dict()

    user_day_dict['total_요일'] = list(map(lambda x : week_han[str(x)], sorted(df['week_day_num'].unique().tolist())))
    user_day_dict['total_년월'] = df['year_month'].value_counts().sort_index().index.tolist()
    user_day_dict['total_년'] = df['year'].value_counts().sort_index().index.tolist()
    user_day_dict['total_시간'] = df['hour'].value_counts().sort_index().index.tolist()

    for user in user_list:
        user_df = df[df['user_name'] == user]
        many_weekday = user_df['week_day_num'].value_counts().sort_index().index.map(lambda x: week_han[str(x)]).tolist()
        many_year_month = user_df['year_month'].value_counts().sort_index().index.tolist()
        many_year = user_df['year'].value_counts().sort_index().index.tolist()
        many_hour = user_df['hour'].value_counts().sort_index().index.tolist()

        user_day_dict[user + '_요일'] = many_weekday
        user_day_dict[user + '_년월'] = many_year_month
        user_day_dict[user + '_년'] = many_year
        user_day_dict[user + '_시간'] = many_hour

        user_day_dict[user + '_요일_num'] = user_df['week_day_num'].value_counts().sort_index().tolist()
        user_day_dict[user + '_년월_num'] = user_df['year_month'].value_counts().sort_index().tolist()
        user_day_dict[user + '_년_num'] = user_df['year'].value_counts().sort_index().tolist()
        user_day_dict[user + '_시간_num'] = user_df['hour'].value_counts().sort_index().tolist()

    return user_day_dict


# 대화가 최대로 끊어진 날, 이어진 날
def get_continue_day_num(df):
    """
    대화가 최대로 끊어진 날, 이어진 날
    :param df: 
    :return: 딕셔너리 형태의 값, 날짜와 날짜 그리고 일수 반환
    """
    max_day = 0
    continue_day = 0

    unique_year_month_day = df['year_month_day'].unique()
    unique_year_month_day_df = pd.DataFrame(unique_year_month_day, columns=['day'])
    unique_year_month_day_df['day'] = pd.to_datetime(unique_year_month_day_df['day'])

    continue_day_list = list()
    continue_select_list = list()

    max_continue_day = list()
    get_continue_day_dict = dict()

    try:
        for day_num in range(len(unique_year_month_day_df) - 1):
            gap = unique_year_month_day_df['day'][day_num] - unique_year_month_day_df['day'][day_num + 1]
            gap = abs(gap.days)
            if max_day < gap:
                max_day = gap
                max_before_day = unique_year_month_day_df['day'][day_num]
                max_after_day = unique_year_month_day_df['day'][day_num + 1]
            if gap == 1:
                continue_day += 1
                continue_day_list.append(unique_year_month_day_df['day'][day_num])
            if gap > 1:
                max_continue_day.append(continue_day)
                continue_select_list.append(continue_day_list)
                continue_day_list = []
                continue_day = 0

        max_continue_num = max(max_continue_day)
        max_continue_idx = max_continue_day.index(max_continue_num)
        continue_min = continue_select_list[max_continue_idx][0]
        continue_max = continue_select_list[max_continue_idx][-1]
    except:
        continue_min = unique_year_month_day[0]
        continue_max = unique_year_month_day[0]
        max_before_day = unique_year_month_day[0]
        max_after_day = unique_year_month_day[0]
        max_continue_num = 1
        max_day = 1

    get_continue_day_dict['continue'] = [str(continue_min), str(continue_max), max_continue_num]
    get_continue_day_dict['max_continue'] = [str(max_before_day), str(max_after_day), max_day]
    return get_continue_day_dict

def ratio_pic(df):
    """
    사진 나와 상대방의 비율
    :param df: 
    :return: 각각의 이름으로 딕셔너리 형태 반환
    """
    pic_dict = dict()
    user_unique = df['user_name'].unique()

    pic_num = df[df.text == '사진']['user_name'].value_counts().tolist()
    pic_user = df[df.text == '사진']['user_name'].value_counts().index.tolist()

    if not pic_num == 0:
        pic_num = df[df.text == '<사진 읽지 않음>']['user_name'].value_counts().tolist()
        pic_user = df[df.text == '<사진 읽지 않음>']['user_name'].value_counts().index.tolist()

    none_user = list(set(user_unique) - set(pic_user))
    pic_user = pic_user + none_user
    for idx, user in enumerate(user_unique):
        if pic_user[idx] in none_user:
            pic_dict[pic_user[idx] + "_사진"] = 0
            continue
        pic_ratio = (pic_num[idx] / sum(pic_num)) * 100
        pic_dict[pic_user[idx] + "_사진"] = pic_ratio

    return pic_dict

def ratio_emo(df):
    """
    이모티콘 나와 상대방의 비율
    :param df:
    :return: 각각의 이름으로 딕셔너리 형태 반환
    """
    emo_dict = dict()
    user_unique = df['user_name'].unique()
    emo_num = df[df.text == '이모티콘']['user_name'].value_counts().tolist()
    emo_user = df[df.text == '이모티콘']['user_name'].value_counts().index.tolist()
    none_user = list(set(user_unique) - set(emo_user))
    emo_user = emo_user + none_user
    for idx, user in enumerate(user_unique):
        if emo_user[idx] in none_user:
            emo_dict[emo_user[idx]+"_이모티콘"] = 0
            continue
        emo_ratio = (emo_num[idx] / sum(emo_num)) * 100
        emo_dict[emo_user[idx]+"_이모티콘"] = emo_ratio

    return emo_dict

# 토픽모델링 (주제찾기)
def hangul_tokenizer(text):
  """
  문장 명사처리, 한글자는 제거
  
  :param text: 
  :return: 명사 리스트 반환
  """
  okt = Okt()
  drop_str = []
  text = okt.normalize(text)
  tokens_ko = okt.nouns(text)
  for idx, ko in enumerate(tokens_ko):
      if len(ko) == 1:
          drop_str.append(ko)
  for dr in drop_str:
      tokens_ko.remove(dr)

  tokens_ko = ' '.join(tokens_ko)
  return tokens_ko

def get_topics(components, feature_names, n=5):
    """
    모델에서 가장 확률이 높은 값을 뽑아냄 5개
    
    :param components: 
    :param feature_names: 
    :param n: 
    :return: 주제 리스트 반환
    """
    topic_list = list()

    for idx, topic in enumerate(components):
        topic_list.extend(feature_names[i] for i in topic.argsort()[:-n -1:-1])
    return list(set(topic_list))

def get_recommend_topic(topic_list):
    """
    모델에서 뽑아낸 주제를 통하여 추천 주제를 얻는다
    2개 이상일시 해당 주제라고 판단
    :param topic_list: 
    :return: 추천주제 리스트 반환
    """
    recommend_topic = []
    topic_txt = load_topic()
    for topic, value in topic_txt.items():
        diff_topic = list(set(topic_list) & set(value))
        if len(diff_topic) >= 2:
            recommend_topic.append(topic)

    if len(recommend_topic) == 0:
        recommend_topic.append(['일상생활','맛집','영화'])

    return recommend_topic

def tfidf_LDA(df_text):
  """
  LDA 학습 및 유저, 나, 상대방을 각각 학습하여 주제, 추천주제를 추출
  
  :param df_text: 
  :return: 전체, 나, 상대방 딕셔너리 비율을 반환
  """
  katalk_stopword = load_stopword()
  name_unique = df_text['user_name'].unique().tolist()
  user_dict = {}

  vectorizer = TfidfVectorizer(max_features=1000, stop_words=katalk_stopword)
  # total_topic = vectorizer.fit_transform(df_text['text'])

  lda_model = LatentDirichletAllocation(n_components=5, learning_method='online', random_state=777, max_iter=1)
  # lda_model.fit_transform(total_topic)

  for name in name_unique:
    user_text = df_text[df_text.user_name == name]['text']
    user_topic = vectorizer.fit_transform(user_text)
    lda_model.fit_transform(user_topic)
    user_terms = vectorizer.get_feature_names()
    user_dict[name + "_주제"] = get_topics(lda_model.components_, user_terms)

  terms = vectorizer.get_feature_names()
  total_topic_list = get_topics(lda_model.components_, terms)
  user_dict['주제추천'] = get_recommend_topic(total_topic_list)

  return user_dict

def load_stopword():
  """
  불용어를 제거하기 위해 불용어 사전을 읽어온다
  
  :return: 불용어 리스트
  """
  korean_stopword_path = 'katalk_stopwords.txt'
  with open(korean_stopword_path, encoding='cp949') as f:
    stopwords_list = [x.strip() for x in f]
    f.close()
  return stopwords_list

def load_topic():
    """
    추천 주제를 위해 주제별 text문서를 가져온다
    
    :return: 주제별 딕셔너리 값 반환
    """
    topic_txt_dict = {}
    topic_txt_list = ['운동','스포츠','인문학','책','글','사교','인맥','게임',
              '오락','아웃도어','여행','업종','직무','외국','언어',
              '문화','공연','축제','음악','악기','공예','만들기','댄스',
              '무용','봉사활동','자동차','오토바이','사진','영상',
              '요리','제조','애완동물','가족','연애']

    for topic in topic_txt_list:
        with open(f"topic/{topic}.txt", encoding='UTF-8') as f:
            topic_word_list = [x.strip() for x in f]
        topic_txt_dict[topic] = topic_word_list
        f.close()
    return topic_txt_dict

def pos_counter(df):
  """
  문장에서 명사를 제거한후 형태소를 찾아내어 말투를 얻음 
  나, 상대방의 각각 top 20의 말투
  
  :param df: 
  :return: 나와 상대방의 딕셔너리 반환
  """
  okt = Okt()
  morphs = ['Josa', 'Adjective', 'Adverb','Verb',' KoreanParticle']
  user_name = df['user_name'].unique().tolist()
  user_dict = dict()
  for name in user_name:
    pos_list = list()
    user_df = df[df.user_name == name]['text'].tolist()
    pos_text = "".join(user_df)
    pos = okt.pos(pos_text, stem=False)
    pos = [p[0] for p in pos if p[1] in morphs]
    pos = [p for p in pos if len(p) > 1]
    pos_counter = Counter(pos).most_common(n=100)
    for text, num in pos_counter:
      pos_list.append([text,num])
    user_dict[name + "_말투"] = pos_list
  return user_dict


# if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('port', type=int, default=4000, help='port number')
    # args = parser.parse_args()

    # app.run(debug=False, host='0.0.0.0', port=4000, ssl_context=None)
    # app.run(debug=False, host='0.0.0.0', port=80)
    # args.port
