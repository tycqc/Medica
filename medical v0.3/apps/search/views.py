from django.shortcuts import render
from django.http import JsonResponse
from elasticsearch import Elasticsearch
from django.core.cache import cache
from xpinyin import Pinyin
import redis
import time
# 将关键词转化为pinyin
p = Pinyin()
redis_client = redis.StrictRedis(host='127.0.0.1')
client = Elasticsearch(hosts=["elastic:123456@81.70.202.37:9200"])

# 三位以逗号的科学计数法
def sci_format(number):
    res = ''
    count = 0
    for i in range(len(number)-1, -1, -1):
        count += 1
        if count == 4:
            res = ',' + res
            count = 1
        res = number[i] + res
    return res


def index(request):
    context = {}
    # context['movie_count'] = sci_format(redis_client.get('movie_count').decode('utf-8'))
    return render(request,'search/index.html', context)

# 搜索建议
def suggest(request):
    search_word = request.GET.get('search_word')
    response = client.search(
        index='medica',
        body={
             "suggest": {
                "blog-suggest": {
                  "text": search_word,
                  "completion": {
                    "field": "title.suggest"
                  }
                }
              }
        }
        )
    title_list = []
    for response in response['suggest']['blog-suggest'][0]['options']:
        title_list.append(response['text'])
    return JsonResponse({'suggest':title_list})

def search(request): 
    NUMS_PER_PAGE = 10
    try:
        page_num = request.GET.get('page', 1)
        page_num = int(page_num)
        search_word = request.GET.get('search_word').strip()
        if len(search_word)<1:
            raise Exception('请输入关键词')
        if len(search_word)>30:
            raise Exception('关键词过长')
        # # 热搜统计,使用cookies判断是否为同一客户端，避免同一关键词重复计数
        # if not request.COOKIES.get(p.get_pinyin(search_word, '')):
        #     redis_client.zincrby('search_word', search_word)
        # 查询时间
        start_time = time.time()
        # 设置使用缓存
        if not cache.get(search_word+'_'+'medica'+'_'+str(page_num)):
            response = client.search(
                index="medica",
                body={
                    "query": {
                        "match": {
                          "name": search_word
                        }
                      },
                    "from": (page_num - 1) * NUMS_PER_PAGE,
                    "size": NUMS_PER_PAGE,
                    "highlight": {  # 查询关键词高亮处理
                        "pre_tags": ['<span class="search-word">'],  # 高亮开始标签
                        "post_tags": ['</span>'],  # 高亮结束标签
                        "fields": {  # 高亮设置
                            "name": {}# 高亮字段
                        }
                    }
                }
            )
            result_list = []
            res = response['hits']['hits']
            for result in res:
                result_list.append({
                    'name': result['highlight']['name'][0] if 'title' in result['highlight'] else result['_source']['name'],
                    'type': result['_source']['type'],
                    'company': result['_source']['company'],
                    'effect': result['_source']['effect'],
                    'side_effect': result['_source']['side_effect'],
                    'method': result['_source']['method'],
                    'code' :result['_source']['code'],
                    'price': result['_source']['price'],
                    'standards': result['_source']['standards'],
                    'project_id': result['_id']

                })
            cache.set(search_word+'_'+'medica'+'_'+str(page_num), result_list , 60)

            if not cache.get(str(search_word)+'_'+'medica'+'_count'):
                cache.set(str(search_word)+'_'+'medica'+'_count', response["hits"]["total"]["value"], 3600)
        end_time = time.time()
        result_list = cache.get(search_word+'_'+'medica'+'_'+str(page_num))
        search_count = cache.get(str(search_word)+'_'+'medica'+'_count')

        # 总页数
        if search_count == 0:
            MAX_PAGE = 1
        else:
            MAX_PAGE = int(search_count/NUMS_PER_PAGE)+1 if search_count/NUMS_PER_PAGE !=0 else int(search_count/NUMS_PER_PAGE)

        if page_num>MAX_PAGE or page_num<0:
            raise Exception('页码不符合规范')

        # 分页逻辑
        page = list(range(max(1,page_num-2), page_num)) +list(range(page_num, min(page_num+2, MAX_PAGE)+1))
        if page_num <= 2:
            page = list(range(1, min(MAX_PAGE, 5)+1))
        if page_num >= MAX_PAGE-1:
            page = list(range(max(1, MAX_PAGE-4), MAX_PAGE+1))
        if page[0]-1 >= 2:
            page.insert(0, '...')
            page.insert(0, 1)
        if MAX_PAGE - page[-1] >= 2:
            page.append('...')
            page.append(MAX_PAGE)

    except Exception as e:
        return render(request, 'search/message.html', { 'message':str(e) })
    # 热搜词
    # hot_search_word = redis_client.zrevrangebyscore('search_word', '+inf', '-inf', start=0, num=8)
    context = {}
    context['MAX_PAGE'] = MAX_PAGE
    context['search_time'] = str(end_time - start_time)[:5]
    context['search_word'] = search_word
    context['previous'] = True if page_num-1>0 else False
    context['next'] = True if page_num+1<=MAX_PAGE else False
    context['page_num'] = page_num
    context['page'] = page
    context['result_list'] = result_list
    context['search_count'] = search_count
    # context['hot_search_word'] = [search_word.decode('utf-8')[:6] for search_word in hot_search_word]
    response = render(request, 'search/result.html', context)
    # 设置cookies
    search_word=search_word.replace('；','')
    response.set_cookie(p.get_pinyin(search_word, ''), 'true')
    return response
