import asyncio
import time

from nonebot import on_command, on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event

sys_handle = on_keyword(['sys', '搜一搜'], priority=200, block=False)


@sys_handle.handle()
async def shua_ti(bot: Bot, event: Event):
    await sys_handle.finish('''本群已和下列搜索引擎达成单方深度合作

Google
https://google.com

Bing
https://bing.com

Baidu
https://baidu.com

DuckDuckGo
https://duckduckgo.com

————————————————

C/C++: https://docs.microsoft.com/en-us/cpp
Python: https://docs.python.org/zh-cn/3/tutorial/index.html
JavaSE: https://www.oracle.com/cn/java/technologies/java-se-api-doc.html ''')
