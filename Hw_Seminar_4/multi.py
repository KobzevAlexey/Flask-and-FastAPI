import requests
from multiprocessing import Process, Pool
import time
import sys
from random import sample
import os

if not os.path.exists('multi_images'):
    os.makedirs('multi_images')

IMG_COUNT = 10

LINK = sys.argv
if len(LINK) > 1:
    LINK = LINK[1]
else:
    LINK = 'links.txt'


def download(url):
    start_time = time.time()
    response = requests.get(url)
    image_name = url.split('/')[-1]
    filename = f'multi_images/{image_name}'
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


processes = []

with open(LINK, 'r', encoding='utf-8') as file:
    links = [i.rstrip() for i in file.readlines()]

if __name__ == '__main__':
    start_time = time.time()
    for url in sample(links, min(IMG_COUNT, len(links))):
        process = Process(target=download, args=(url,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    print(f"Total {time.time() - start_time}")
