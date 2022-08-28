import asyncio

import aiohttp
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event

lg_user = 'lg_user'
stats_handle = on_command('lg_user')

@stats_handle.handle()
async def lg_user_info(bot:Bot,event:Event):
    text = event.get_plaintext()
    # Delete space
    text = text.replace(' ','')
    if text == '/lg_user':
        await stats_handle.finish('没有检测到用户ID，请在指令后方添加用户id')
    # If has start to request
    text = text.replace('/lg_user','')
    if text.isdigit() == False:
        await stats_handle.finish('输入的用户ID不符合规范，请检查后重新输入')
    # If ALL check passed, start to request
    # Check user Input
    # request info of user by unofi api
    user_id = text
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://a-1c37c2-1300876583.ap-shanghai.service.tcloudbase.com/luogu?id={user_id}') as res:
            if res.status != 200:
                await stats_handle.finish('用户数据请求失败，请稍后再试...')
            data_dict = await res.json()
            print(data_dict)
            await stats_handle.finish(str(data_dict['currentData']['user']))