from django.shortcuts import render
import os
from datetime import datetime, time
import jieba
import simplejson as json
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from staff.models import Staff
from medicine.models import Medicine, Cart
from orders.models import Orders, OrderGoods
from store.models import medstore
from store.views import login


# Create your views here.
def finance_medicine_datas(request):
    # 判断是否登录
    context = {
        'page': 'order_list',
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        storeid = request.session.get('storeid')
        context['username'] = username
    else:
        return login(request)

    if request.method == 'GET':
        year = request.GET.get('year')
        month = request.GET.get('month')
        day = request.GET.get('day')
        all = {
            "title": "的销售数据：",
            "allnum": 0,
            "allmoney": 0,
            "all_medname": [],
            "all_medcount": [],
            "all_medallprice": [],
        }
        date_str = ""
        orders = Orders.objects.filter()
        if year != None:
            orders = orders.filter(time__year=year)
            date_str = date_str + str(year) + "年"
        if month != None:
            orders = orders.filter(time__month=month)
            date_str = date_str + str(month) + "月"
        if day != None:
            orders = orders.filter(time__day=day)
            date_str = date_str + str(day) + "日"
        all['title'] = date_str + all['title']
        all_medcount = {}
        all_medprice = {}
        # all["all_med"] = all_medcount
        for order in orders:  # 读取每一笔订单
            all["allmoney"] += order.med_price
            all["allnum"] += order.total_count
            allmed = OrderGoods.objects.filter(order=order)
            for med in allmed:  # 读取每一笔订单中的具体药品
                medname = med.sku.name
                count = med.count
                price = med.price
                all_medprice[medname] = price
                if medname in all_medcount:
                    all_medcount[medname] += count
                else:
                    all_medcount[medname] = count
        all["title"] = all["title"] + " 总销售量：{0}；总销售额：{1}".format(all["allnum"], all["allmoney"])
        for medname in all_medcount.keys():
            all["all_medname"].append(medname)
            all["all_medcount"].append(all_medcount[medname])
            all["all_medallprice"].append(all_medcount[medname] * all_medprice[medname])
    data = json.dumps(all, ensure_ascii=False)
    return HttpResponse(data)
