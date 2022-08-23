import asyncio
import time

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event

ts_handle = on_command('ts')

@ts_handle.handle()
async def home(bot: Bot, event: Event):
    '''Timestamp便民小功能'''
    print('Activated ts module')
    text = event.get_message().extract_plain_text()
    print(text)
    # 删除掉用户信息中的指令部分
    if '/ts' in text:
        text = text.replace('/ts ', '')
    if '/timestamp ' in text:
        text = text.replace('/timestamp ', '')
    # 确认输入的是时间戳还是时间格式
    if text == '/ts':
        await ts_handle.finish(f'当前UNIX时间戳: {str(int(time.time()))}\n\n请输入INT格式的时间戳或者前缀为d的日期时间，如d20220101120000')
    if text.startswith('d'):
        text = text.replace('d','')
        local = time.strptime(text, '%Y%m%d%H%M%S')
        timestamp = time.mktime(local)
        await ts_handle.finish(str(int(timestamp)))
    else:
        timestamp = int(text)
        local = time.localtime(timestamp)
        time_read = time.strftime('%Y-%m-%d %H:%M:%S', local)
        await ts_handle.finish(time_read)