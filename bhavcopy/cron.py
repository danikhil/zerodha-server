from typing import List
import requests
import logging
import uuid
import zipfile
import os, shutil
import aioredis, asyncio
import csv
from itertools import chain
from datetime import datetime, timedelta

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
redis_host = str(os.getenv("REDIS_HOST"))
redis_username = os.getenv("REDIS_USERNAME")
redis_password = os.getenv("REDIS_PASSWORD")
redis_port = os.getenv("REDIS_PORT")

#key is name in record and value is index
async def store_in_db0(key, value, redis):
   await redis.lpush(key.strip(), value.strip())

#key is sc_code
async def store_in_db1(key, columns, record, redis):
   pairs = list(chain.from_iterable([columns[i].strip(), record[i].strip()] for i in range(len(record))))
   await redis.hmset(key.strip(), *pairs)

async def read_files_and_store(directory: str):
   files = os.listdir(directory)
   redis = await aioredis.create_redis(address=redis_host, password=redis_password, db=0)
   for file in files:
      with open(os.path.join(directory, file), newline='\n') as csvfile:
         reader = csv.reader(csvfile)
         columns = next(reader)
         if(columns == None):
            continue
         for row in reader:
            await store_in_db0(row[1], row[0], redis)
            await store_in_db1(row[0], columns, row, redis)
   redis.close()
   await redis.wait_closed()


def fetch_equity():
   date = datetime.today() - timedelta(days=1)
   url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ'+ date.strftime("%d%m%y") +'_CSV.ZIP'
   try:
      response = requests.get(url=url, headers=headers)
      response.raise_for_status()
      file_name = "equity_" + str(uuid.uuid4())
      zip_path = '/tmp/' + file_name + ".zip"
      file_directory = '/tmp/' + file_name
      with open(zip_path, 'wb') as f:
         f.write(response.content)
      with zipfile.ZipFile(zip_path, 'r') as zip_ref:
         zip_ref.extractall(file_directory)
      os.remove(zip_path)
      asyncio.run(read_files_and_store(file_directory))
      shutil.rmtree(file_directory)
   except requests.exceptions.RequestException as e:
      logging.error(e)

def fetch_bhavcopy():
   fetch_equity()

if __name__ == "__main__":
   fetch_bhavcopy() 