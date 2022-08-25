import asyncio
import time

import aiohttp
import wikipedia
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message

wikipedia_handle = on_command('wiki')

@wikipedia_handle.handle()
async def wiki(bot:Bot,event:Event):
    await bot.send(event,'编程姬努力翻书ing，请稍等...')
    # initialize the param
    text = event.get_plaintext()
    if text == '/wiki':
        await wikipedia_handle.finish('没有检测到搜索内容，请在命令后方加入想要搜索的内容\n\n可选参数: lang-')
    else:
        text = text.replace('/wiki ','')
    lang = 'zh'
    info = text.split(' ')
    text = info[0]
    # 读取传入字符串中的参数
    for i in info:
        # print(i)
        if 'lang-' in i:
            lang = i.replace('lang-', '')
    # 部署参数
    wikipedia.set_lang(lang)
    # 去歧义化输入的查询字符，但同时提供多个相近结果，引导用户选择正确的字符进行查询
    search = wikipedia.search(text)
    try:
        text = search[0]
    except:
        await wikipedia_handle.finish('啊呀，没有找到结果呢')
    print('text', text)
    search_text = ''
    # 生成一个包含各个建议项的文字列表，同时排除已经被采用的首个建议项
    for i in search:
        if i == text:
            continue
        search_text = search_text+'\n'+i
    # print(search)
    # 尝试抓取内容
    try:
        sum = wikipedia.summary(text)
        page = wikipedia.page(text)
        link = page.url
    # 一般抓取失败的原因是关键词歧义严重，无法通过选择首选建议项的方式解决（即关键词的首选建议项仍然存在歧义，此时放弃抓取，要求用户重新输入关键词）
    except:
        sum = '关键词歧义过大，请更换更精确的关键词再试吧～'
        link = ''
        # 对选择的关键词重新建立候选项
    search = wikipedia.search(text)
    search_text = ''
    for i in search:
        search_text = search_text+'\n'+i
    # re_info = (text, link, sum, search_text)
    # print(re_info)
    await wikipedia_handle.finish(sum+'\n\n'+link+'\n\n'+search_text)
