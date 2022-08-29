import asyncio
import time

from nonebot import on_command,on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event

shuati_handle = on_keyword(['/刷题','/刷点题','/做题'],priority=200)

last_check_time = {0:0}

@shuati_handle.handle()
async def shua_ti(bot:Bot,event:Event):
    await shuati_handle.finish('''刷题网站汇总:

牛客
https://www.nowcoder.com/

杭电
http://acm.hdu.edu.cn/

洛谷
https://www.luogu.com.cn/

C语言网
https://www.dot.cpp.com/

LibreOJ
https://loj.ac/

AcWing
https://www.acwing.com/

Leetcode
https://leetcode.cn/

CodeForces
https://codeforces.com/''')