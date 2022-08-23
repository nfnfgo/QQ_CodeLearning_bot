import asyncio

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event

help_handle = on_command('help')


@help_handle.handle()
async def help(bot: Bot, event: Event):
    await help_handle.finish('''编程姬 Ver 0.0.1

Author:
Oyasuminasai
San_Cai

/cf_list
查看当前CodeForces比赛列表

/cf_u [用户Handle]
查看CF用户信息

/ts
时间戳转换，格式为int时间戳或者d+[日期]，如d20220901120000

您可以发送 /comms 查看完整指令列表''')
