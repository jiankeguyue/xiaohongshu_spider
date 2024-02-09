#! usr/bin/python
# writer: yuej1njia0ke

import random
import pandas as pd
import requests
from time import sleep
import pandas
import config
import json
import colorama
import random
import os
import threading

# 爬取关键词列表
# 网站首页 https://www.xiaohongshu.com/
keywords = ['户外运动产品','户外搭子','户外合作']


def title():
    print("                                        ")
    print("|    | \ _ / | \\ ___ /(/  \\_ __ _| |")
    print("|____|__\_/__|  \\ __/( /__\\ _    | |")
    print("|    |__/ \__|   \\ /(  /  \\      | |   ")
    print("|    | /   \ |    |(___/_ \\  spider_redB00k_|\\_\\")
    print("                                 writer: yuejinjianke")



def get_data(note_id,file_path):

    # 定义cookie
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.0.10191 SLBChan/10',
        'Cookie' : config.cookie
    }

    # 初始化要爬取的内容
    note_id_list = []
    nickname_list = []
    user_id_list = []
    comment_time_list = []
    content_list = []
    content_level_list = []
    like_count_list = []
    page = 1
    comment_num = 0

    # 定义初始note_id，需要自己操作网页获取定义

    print(colorama.Fore.GREEN + "[info] 开始爬取")
    while True:
        if page == 1:
            url = 'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={}&cursor=&top_comment_id=&image_formats=jpg,webp,avif'.format(note_id)
        else:
            print(colorama.Fore.GREEN + "[info] 进入下一轮循环")
            url = 'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={}&cursor={}&top_comment_id=&image_formats=jpg,webp,avif'.format(note_id,next_cursor)
            print(url)
        try:
            json_text = requests.get(url=url,headers=headers).json()
        except Exception as e:
            print(colorama.Fore.RED + '[error] 发生问题：{}'.format(e))

        for comment in json_text['data']['comments']:
            list_append_1(note_id_list, nickname_list, user_id_list, comment_time_list,  content_list,
                        content_level_list,like_count_list, comment)
            comment_num += 1
            # 爬取子评论
            if comment['sub_comment_has_more']:
                for sub_comment in comment['sub_comments']:
                    list_append_2(note_id_list, nickname_list, user_id_list, comment_time_list,  content_list,
                        content_level_list,like_count_list, sub_comment)
                    comment_num += 1
        # if comment_num >= 100:
        #     print(colorama.Fore.RED + '[info] 终止循环。')
        #     break
        if not json_text['data']['has_more']:
            print(colorama.Fore.RED + '[info] 没有多余搜索结果了，终止循环。')
            print(colorama.Fore.RED + '[info] 已结束爬取')
            data_save(note_id_list, nickname_list, user_id_list, comment_time_list, content_list, content_level_list,
                      like_count_list, file_path)
            break

        next_cursor = json_text['data']['cursor']
        page += 1
        print(colorama.Fore.BLUE + '[info] 正在读取下一个页面')
        sleep(3+random.random())
        # if page >= 3:
        #     print(colorama.Fore.RED + '[info] 已结束爬取')
        #     data_save(note_id_list,nickname_list,user_id_list,comment_time_list,content_list,content_level_list,like_count_list,file_path)
        #     break

# 爬取父级评论相关消息
def list_append_1(note_id_list,nickname_list,user_id_list,comment_time_list,content_list,content_level_list,like_count_list,comment):
    note_id_list.append(comment['note_id'])
    nickname_list.append(comment['user_info']['nickname'])
    user_id_list.append(comment['user_info']['user_id'])
    comment_time_list.append(pd.to_datetime(int(comment['create_time']) / 1000, unit='s').strftime("%Y-%m-%d %H:%M:%S"))
    content_list.append(comment['content'])
    content_level_list.append('父评论')
    like_count_list.append(comment['like_count'])

# 爬取子级评论相关消息
def list_append_2(note_id_list,nickname_list,user_id_list,comment_time_list,content_list,content_level_list,like_count_list,comment):
    note_id_list.append(comment['note_id'])
    nickname_list.append(comment['user_info']['nickname'])
    user_id_list.append(comment['user_info']['user_id'])
    comment_time_list.append(pd.to_datetime(int(comment['create_time']) / 1000, unit='s').strftime("%Y-%m-%d %H:%M:%S"))
    content_list.append(comment['content'])
    content_level_list.append('子评论')
    like_count_list.append(comment['like_count'])


def data_save(note_id_list,nickname_list,user_id_list,comment_time_list,content_list,content_level_list,like_count_list,file_path):
    df = pd.DataFrame(
        {
            '笔记链接': note_id_list,
            '评论者昵称': nickname_list,
            '评论者id': user_id_list,
            '评论时间': comment_time_list,
            '评论内容': content_list,
            '评论等级': content_level_list,
            '评论点赞数': like_count_list,
        }
    )
    if os.path.exists(file_path):
        header = False
    else:
        header = True
    df.to_csv(file_path, mode="a+", header=header, index=False, encoding='utf_8_sig')


def multi_thread(note_id):
    threads = []
    for note in note_id:
        threads.append(
            threading.Thread(target=get_data,args=(note,f"{note}.csv"))
        )
    for task in threads:
        task.start()

    for task in threads:
        task.join()

if __name__ == '__main__':
    title()
    # 定义初始note_id，需要自己操作网页获取
    note_id = ['64449a34000000002702a9e8','6502ec4d000000001e00cb08','6555aa90000000000f02b86e']
    multi_thread(note_id)