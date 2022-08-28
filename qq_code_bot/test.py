import asyncio

from aiohttp import ClientSession

# async def main():
#     headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63'}
#     async with ClientSession() as session:
#         async with session.get('https://a-1c37c2-1300876583.ap-shanghai.service.tcloudbase.com/luogu?id=764096') as res:
#             print(await res.json())

async def get_size_read(b):
    b = int(b)
    print(b)
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

async def main():
    print(await get_size_read('340582745'))

if __name__ == '__main__':
    asyncio.run(main())