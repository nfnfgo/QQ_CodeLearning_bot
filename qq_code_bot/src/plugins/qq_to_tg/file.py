import asyncio
import time
import os

from nonebot import on_command, on_keyword, on_notice
from nonebot.adapters.onebot.v11 import Bot, Event, Message

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery, InputFile

import aiohttp


async def offline_file(bot: Bot, event: Event) -> bool:
    if event.notice_type == 'offline_file':
        return True
    else:
        return False

file_handle = on_notice(offline_file)


# Handle private file and download it
@file_handle.handle()
async def file_to_tg(bot: Bot, event: Event):
    # https://docs.go-cqhttp.org/event/#%E6%8E%A5%E6%94%B6%E5%88%B0%E7%A6%BB%E7%BA%BF%E6%96%87%E4%BB%B6
    # Set Allow List
    allow_qq_id = [1756185288, 1]
    tg_user_name = 975140440
    if (event.user_id in allow_qq_id) == False:
        return
    file_info = event.file
    f_name = file_info['name']
    f_size = await get_size_read(file_info['size'])
    f_url = file_info['url']
    re_text = f'''文件信息

文件名: {f_name}
文件大小: {f_size}
下载链接: {f_url}'''
    await bot.send(event, re_text)
    # Download part
    # Get user id
    if event.user_id in allow_qq_id:
        tg_bot = AsyncTeleBot('5050467713:AAFQultsmN1YdFnp9MVZiBakXSEXVr1ED6M', parse_mode='HTML')
        if file_info['size'] < 1024*1024*50:
            # Auto download if file size little than 200MB
            try:
                # If file already exists, Delete it
                if os.path.exists(f'./downloads/{f_name}'):
                    os.remove(f'./downloads/{f_name}')
                # Start Downloading
                b_now = 0
                b_total = int(file_info['size'])
                b_times = 0
                await tg_bot.send_message(tg_user_name, re_text)
                dl_proc_msg = await tg_bot.send_message(tg_user_name, str(round(b_now*100/b_total, 2)))
                async with aiohttp.ClientSession() as session:
                    async with session.get(f_url) as res:
                        with open(f'./downloads/{f_name}', 'wb') as f:
                            async for chunk in res.content.iter_chunked(1024):
                                f.write(chunk)
                                b_now += 1024
                                b_times += 1
                                if (b_times > b_total/1024/10):
                                    b_times = 0
                                    try:
                                        await tg_bot.edit_message_text(f'Uploading: {str(round(b_now*100/b_total, 2))}%', tg_user_name, dl_proc_msg.id)
                                    except:
                                        print('passed update proc')
                                        pass
                # Start Sending
                await tg_bot.send_document(tg_user_name, InputFile(f'./downloads/{f_name}'))
                await bot.send(event, f'{f_name} 已经被成功上传到远程服务！')
            except Exception as e:
                await bot.send(event, '远程端上传失败，请稍后重试')
                await tg_bot.send_message(tg_user_name, 'Upload Failed: '+f_url+'\n\n'+str(e))
            try:
                os.remove(f'./downloads/{f_name}')
            except:
                await bot.send(event,'残余文件清理失败，您可能需要手动清理文件')
        else:
            await bot.send(event, '文件超过200MB，如果需要上传到远程端，请复制以下指令发送')
            await bot.send(event, f'/to_tg {f_url}')


async def get_size_read(b):
    b = int(b)
    if b > 1024*1024*1024:
        re_text = f'{str(round((b/(1024*1024*1024)),2))}GB'
        return re_text
    elif b > 1024*1024:
        re_text = f'{str(round((b/(1024*1024)),2))}MB'
        return re_text
    elif b > 1024:
        re_text = f'{str(round((b/(1024)),2))}KB'
        return re_text
    else:
        return f'{b}B'
