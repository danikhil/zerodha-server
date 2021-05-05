from django.http import HttpResponse, response
from django.views.decorators.http import require_http_methods
from asgiref.sync import async_to_sync

import aioredis
import json
import os

redis_host = os.getenv("REDIS_HOST")
redis_username = os.getenv("REDIS_USERNAME")
redis_password = os.getenv("REDIS_PASSWORD")

# Create your views here.
@require_http_methods(["GET"])
def index(request):
   return HttpResponse("Hello world")

@require_http_methods(["GET"])
@async_to_sync
async def search_name(request):
   redis = await aioredis.create_redis(redis_host, 16872, password=redis_password)
   query = request.GET['query']
   results = await redis.scan(0, match= '*' + query + '*', count=1000)
   _, results = results
   results = results[:10]
   results = [x.decode('utf-8') for x in results]
   return HttpResponse(json.dumps(results))

@require_http_methods(["GET"])
@async_to_sync
async def search(request):
   redis = await aioredis.create_redis(redis_host, 16872, password=redis_password)
   name = request.GET['query']
   length = await redis.llen(name)
   indices = await redis.lrange(name, 0, length)
   response = []
   for index in indices:
      columns = ['SC_CODE', 'SC_NAME', 'OPEN', 'CLOSE', 'LOW', 'HIGH']
      result = await redis.hmget(index, *columns)
      result = [x.decode('utf-8') for x in result]
      record = {columns[i].replace("SC_", "").lower(): result[i] for i in range(len(result))}
      response.append(record)
   return HttpResponse(json.dumps(response))
