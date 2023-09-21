import asyncio
import aiohttp
import aiofiles
from random import sample
from aiohttp import ClientSession
import aiofiles
from uuid import uuid4
import time
import sys
import os

if not os.path.exists('async_images'):
    os.makedirs('async_images')

IMG_COUNT = 10

LINK = sys.argv
if len(LINK) > 1:
    LINK = LINK[1]
else:
    LINK = None
print(f"{LINK=}")


async def get_image(session, url):
    try:
        resp = await session.request(method="GET", url=url)
        return resp
    except Exception as ex:
        print(ex)


async def save_image(url):
    start_time = time.time()
    async with ClientSession() as session:
        resp = await get_image(session, url)
        if resp and resp.status == 200:
            image_name = url.split('/')[-1]
            path = f'async_images/{image_name}'

            async with aiofiles.open(path, 'wb') as f:
                await f.write(await resp.read())
        else:
            print("NOT OK")
    print(f"saving {url[-10:]} ended for {time.time() - start_time}")


async def save_multiple_images(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        data = [i.rstrip() for i in file.readlines()]
    async with ClientSession() as session:
        tasks = []

        for link in sample(data, min(IMG_COUNT, len(data))):
            tasks.append(
                save_image(link)
            )
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_time = time.time()
    if LINK:
        asyncio.run(save_multiple_images(filename=LINK))
    else:
        asyncio.run(save_multiple_images(filename='links.txt'))
    print(f"total = {time.time() - start_time}")
