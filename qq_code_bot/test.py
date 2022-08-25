import asyncio

from aiohttp import ClientSession

async def main():
    async with ClientSession() as session:
        async with session.get('https://www.luogu.com.cn/api/problem/list') as res:
            print(await res.json())

if __name__ == '__main__':
    asyncio.run(main())