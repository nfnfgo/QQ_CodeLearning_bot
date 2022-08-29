import asyncio
import json

from bilibili_api import video


async def main():
    # 实例化 Video 类
    v = video.Video(bvid="BV1uv411q7Mv")
    # 获取信息
    info = await v.get_info()
    # 打印信息
    print(info)
    test = json.dumps(info)
    # print(test)
    with open('bilibili_api_info.json', 'w') as f:
        f.write(test)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
