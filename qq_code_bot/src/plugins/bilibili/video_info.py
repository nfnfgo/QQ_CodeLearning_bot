'''Functions about showing video info while bilibili relevant link detected in a group chat or a private chat'''

import asyncio
import time
import json
import re

from nonebot import on_command, on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
from bilibili_api import video, get_real_url


# Some Module Config
# Default description length
desc_len = 50

# Create bilibili.com and b23.tv checker
bili_link_handle = on_keyword(['b23.tv', 'bilibili.com'])


@bili_link_handle.handle()
async def show_video_info_handler(bot: Bot, event: Event):
    '''Call get_video_read to get the info and parsing it to a OneBot Message type object'''

    # Request Read Function to get info
    re_info = await get_video_info_read(event.get_plaintext())
    if re_info is not None:
        text = re_info[0]
        url = re_info[1]
        # Construct return Message Object
        re_msg = Message([MessageSegment(type='image', data={'file': url}),
                          MessageSegment(type='text', data={'text': text})])
        await bili_link_handle.finish(re_msg)
    else:
        await bili_link_handle.finish('未能成功解析视频')


async def get_video_info_read(video_info: str | int) -> list | None:
    '''
    (Coroutine) Use to get a readable information about a bilibili video

    Params:
    video_info: May be the BV Number or a link of a bilibili video. the link could 
    be the bilibili.com/xxx or the short url b23.tv/xxx

    Return: None if the video info is invailid, else return a List which contains a 
    info text and a cover picture.

    Notice: the list type object will have such structure [text:str, url:str]'''
    # Try to find a link in the text
    try:
        video_info = re.search('(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]',video_info).group()
    except:
        pass
    # Try to deal with info, if is short url, find the original url, and exstract BV or AV num
    try:
        video_info = await get_real_url(video_info)
    except:
        pass
    print('video_info:', video_info)

    # use regex to find av or bv
    if 'BV' in video_info:
        video_info = re.search('BV[A-Za-z0-9]+', video_info).group()
    elif 'av' in video_info:
        video_info = re.search('av[0-9]+', video_info).group()
    else:
        pass
    print('video_info_AFTER:', video_info)

    # create video instance for later use
    try:
        v = video.Video(video_info)
        v_info = await v.get_info()
    except Exception as e:
        print(e)
        return None
    # construct re_text info
    title = v_info['title']
    cover_url = v_info['pic']
    desc = v_info['desc']
    up_name = v_info['owner']['name']
    try:
        desc = desc[:desc_len]+'...'
    except Exception as e:
        print(e)
        pass
    date = v_info['pubdate']
    date = time.localtime(int(date))
    date = time.strftime('%Y-%m-%d %H:%M:%S', date)
    re_text = ''
    # Title and BV info
    re_text += f'''{title}
————————————————
发布于 {date}
UP主: {up_name}
————————————————
简介:
{desc}
————————————————
{v_info['bvid']} (av{v_info['aid']})
'''
    return (re_text, cover_url)

# Test
# if __name__ == '__main__':
#     asyncio.run(show_video_info_handler())
