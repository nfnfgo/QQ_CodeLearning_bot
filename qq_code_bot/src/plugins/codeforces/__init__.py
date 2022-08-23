'''Implement Functions About CodeForce API reading'''

import asyncio
import time
import random

import aiohttp
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event

cf_list_handle = on_command('cf_list')


async def cf_request(method_param: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://codeforces.com/api/{method_param}') as res:
            data_dict = await res.json()
    return data_dict

@cf_list_handle.handle()
async def get_contests(bot: Bot, event: Event):
    data_dict: dict = await cf_request('contest.list?gym=false')
    # If API request Failed
    if data_dict['status'] != 'OK':
        return '数据请求失败'
    else:
        result_list = data_dict['result']
    # Read data
    phase_text_dict = {'BEFORE': '❎未开始', 'FINISHED': '⏹️已结束'}
    # Construct text
    re_text = '赛事列表\n'
    # Iterate Some Contests
    counter = 1
    for contest_dict in result_list:
        if (counter > 10) or (contest_dict['phase'] == 'FINISHED'):
            break
        # phase text
        try:
            phase_text = phase_text_dict[contest_dict['phase']]
        except:
            phase_text = contest_dict['phase']
        # starttime
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(contest_dict['startTimeSeconds'])))
        # duration
        duration = str(int((contest_dict['durationSeconds']/60)//60))+'小时' + str(int((contest_dict['durationSeconds']/60) % 60))+'分'
        # start to construct single text
        single_re_text = ''
        single_re_text += f'''赛事:{contest_dict['name']} ({contest_dict['id']})
赛事状态: {phase_text}
赛事类型: {contest_dict['type']}
开始时间: {start_time} UTC+8
持续时间: {duration}

'''
        re_text += single_re_text
        counter += 1
    await cf_list_handle.finish(re_text)


async def get_user(handle: str, rating_info: bool = True):
    handle = str(handle)
    method_param = f'user.info?handles={handle}'
    # Start to request Info by CF API
    data_dict = await cf_request(method_param=method_param)
    if data_dict['status'] != 'OK':
        return ('error', 'error')
    user_info = data_dict['result'][0]
    # Dump data
    # lastonline
    last_online = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(user_info['lastOnlineTimeSeconds'])))
    # register date
    reg_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(user_info['registrationTimeSeconds'])))
    # rank / phase
    try:
        user_info['rank']
    except:
        user_info['rank'] = '未知'
        user_info['maxRank'] = '未知'
    try:
        user_info['rating']
    except:
        user_info['rating'] = '未知'
        user_info['maxRating'] = '未知'
    # construct Caption
    re_text = ''
    re_text += f'''{user_info['handle']}

注册于: {reg_date}
等级/最高: 
{user_info['rank']}
{user_info['maxRank']}
分数/最高: 
{str(user_info['rating'])}
{str(user_info['maxRating'])}

<a href="https://codeforces.com/profile/{user_info['handle']}">用户档案页面</a>
'''
    return (user_info['titlePhoto'], re_text)
