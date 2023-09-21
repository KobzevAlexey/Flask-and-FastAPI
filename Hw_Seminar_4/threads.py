import requests
import threading
import time
import sys
from random import sample
import os

if not os.path.exists('threads_images'):
    os.makedirs('threads_images')

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
    filename = f'threads_images/{image_name}'
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Downloaded {url} in {time.time() - start_time:.2f}seconds")


threads = []

with open(LINK, 'r', encoding='utf-8') as file:
    links = [i.rstrip() for i in file.readlines()]

start_time = time.time()

for link in sample(links, min(IMG_COUNT, len(links))):
    thread = threading.Thread(target=download, args=[link])
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()

print(f"total = {time.time() - start_time}")
