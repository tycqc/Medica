from django.shortcuts import render
import os
import datetime
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
import calendar

'''
res = calendar.monthrange(2020,5)
print(res)
[out]:
(4,31)第一个数表示5月份第一天是星期五（周一到周天：0-6），第二个数字表示天数
'''


# Create your views here.
# 某个时间段每种药品的销售数据
def finance_medicine(request):
    # 判断是否登录
    context = {
        'page': 'finance_medicine',
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        storeid = request.session.get('storeid')
        store = medstore.objects.get(pk=storeid)
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
        orders = Orders.objects.filter(drugstore=store)
        if not orders.exists():
            context['errmsg'] = "您还没有数据"
        if year != None and year != "":
            orders = orders.filter(time__year=year)
            date_str = date_str + str(year) + "年"
        if month != None and month != "":
            orders = orders.filter(time__month=month)
            date_str = date_str + str(month) + "月"
        if day != None and day != "":
            orders = orders.filter(time__day=day)
            date_str = date_str + str(day) + "日"
        if not orders.exists():
            context['errmsg'] = "该时间没有销售数据"
        if date_str == '':
            date_str = "所有"
        all['title'] = date_str + all['title']
        context['year'] = year
        context['month'] = month
        context['day'] = day
        if context['year'] == None:
            context.pop('year')
        if context['month'] == None:
            context.pop('month')
        if context['day'] == None:
            context.pop('day')
        thisyear = int(datetime.datetime.now().strftime('%Y'))
        context['years'] = [i for i in range(thisyear, 1999, -1)]
        context['months'] = [i for i in range(1, 13)]
        context['days'] = [i for i in range(1, 32)]
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
        all["all_medname"] = json.dumps(all["all_medname"], ensure_ascii=False)
        all["all_medcount"] = json.dumps(all["all_medcount"], ensure_ascii=False)
        all["all_medallprice"] = json.dumps(all["all_medallprice"], ensure_ascii=False)
    context['all'] = all
    return render(request, "salesDATA/finance_medicine.html", context=context)


# 某个时间段每个员工的销售数据
def finance_staff(request):
    # 判断是否登录
    context = {
        'page': 'finance_staff',
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        storeid = request.session.get('storeid')
        store = medstore.objects.get(pk=storeid)
        context['username'] = username
    else:
        return login(request)

    if request.method == 'GET':
        startdate = request.GET.get('startdate')
        enddate = request.GET.get('enddate')
        if str(startdate) > str(enddate):
            startdate, enddate = enddate, startdate
        orders = Orders.objects.filter(drugstore=store)
        if not orders.exists():
            context['errmsg'] = "您还没有数据"
        order1 = orders[0]
        if startdate == None:
            startdate = order1.time.strftime('%Y-%m-%d')
        if enddate == None:
            enddate = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        all = {
            "title": "从{}到{}的各员工销售数据：".format(startdate, enddate),
            "allnum": 0,
            "allmoney": 0,
            "all_staffname": [],
            "all_staffcount": [],
            "all_staffallprice": [],
        }
        context['startdate'] = startdate
        context['enddate'] = enddate
        orders = orders.filter(time__range=(startdate, enddate))
        print(orders)
        if not orders.exists():
            context['errmsg'] = "没有销售数据"
        all_staffcount = {}
        all_staffprice = {}
        all_staff = Staff.objects.filter(store=store)
        for staff in all_staff:
            staffname = staff.name
            all_staffcount[staffname] = 0
            all_staffprice[staffname] = 0

        # all["all_med"] = all_medcount
        for order in orders:  # 读取每一笔订单
            med_price = order.med_price
            all["allmoney"] += med_price
            total_count = order.total_count
            all["allnum"] += total_count
            staffname = order.staff.name
            if staffname in all_staffcount:
                all_staffcount[staffname] += total_count
                all_staffprice[staffname] += med_price
            else:
                all_staffcount[staffname] = total_count
                all_staffprice[staffname] = med_price
        for staffname in all_staffcount.keys():
            all["all_staffname"].append(str(staffname))
            all["all_staffcount"].append(all_staffcount[staffname])
            all["all_staffallprice"].append(all_staffprice[staffname])
        all["all_staffname"] = json.dumps(all["all_staffname"], ensure_ascii=False)
        all["all_staffcount"] = json.dumps(all["all_staffcount"], ensure_ascii=False)
        all["all_staffallprice"] = json.dumps(all["all_staffallprice"], ensure_ascii=False)
    context['all'] = all
    return render(request, "salesDATA/finance_staff.html", context=context)


# 按天对展示某月的销售数据
def finance_month(request):
    # 判断是否登录
    context = {
        'page': 'finance_month',
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        storeid = request.session.get('storeid')
        store = medstore.objects.get(pk=storeid)
        context['username'] = username
    else:
        return login(request)

    if request.method == 'GET':
        year = request.GET.get('year')
        month = request.GET.get('month')
        # if startdate > enddate:
        #     startdate, enddate = enddate, startdate
        orders = Orders.objects.filter(drugstore=store)
        if not orders.exists():
            context['errmsg'] = "您还没有数据"
        if year == None and month == None:
            year = datetime.datetime.now().strftime('%Y')
            month = datetime.datetime.now().strftime('%m')
        all = {
            "title": "{}年{}月的每日销售数据：".format(year, month),
            "allnum": 0,
            "allmoney": 0,
            "all_i": [],
            "all_daycount": [],
            "all_dayallprice": [],
        }
        allorders = orders.filter(time__year=year, time__month=month)
        if not orders.exists():
            context['errmsg'] = "您还没有数据"
        all_daycount = {}
        all_dayprice = {}
        context['year'] = year
        context['month'] = month
        if context['year'] == None:
            context.pop('year')
        if context['month'] == None:
            context.pop('month')
        thisyear = int(datetime.datetime.now().strftime('%Y'))
        context['years'] = [i for i in range(thisyear, 1999, -1)]
        context['months'] = [i for i in range(1, 13)]
        days = int(calendar.monthrange(int(year), int(month))[1])
        for i in range(1, days + 1):
            orders = allorders.filter(time__day=i)
            all_daycount[i] = 0
            all_dayprice[i] = 0
            if orders == None:
                continue
            else:
                for order in orders:
                    med_price = order.med_price
                    all["allmoney"] += med_price
                    total_count = order.total_count
                    all["allnum"] += total_count
                    all_daycount[i] += total_count
                    all_dayprice[i] += med_price

        for dayname in all_daycount.keys():
            all["all_i"].append(str(month) + "-" + str(dayname))
            all["all_daycount"].append(all_daycount[dayname])
            all["all_dayallprice"].append(all_dayprice[dayname])
        all["all_i"] = json.dumps(all["all_i"], ensure_ascii=False)
        all["all_daycount"] = json.dumps(all["all_daycount"], ensure_ascii=False)
        all["all_dayallprice"] = json.dumps(all["all_dayallprice"], ensure_ascii=False)
    context['all'] = all
    return render(request, "salesDATA/finance_month.html", context=context)


# 按月对展示某年的销售数据
def finance_year(request):
    # 判断是否登录
    context = {
        'page': 'finance_year',
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        storeid = request.session.get('storeid')
        store = medstore.objects.get(pk=storeid)
        context['username'] = username
    else:
        return login(request)

    if request.method == 'GET':
        year = request.GET.get('year')
        orders = Orders.objects.filter(drugstore=store)
        if not orders.exists():
            context['errmsg'] = "您还没有数据"
        if year == None:
            year = datetime.datetime.now().strftime('%Y')
        all = {
            "title": "{}年的每月销售数据：".format(year),
            "allnum": 0,
            "allmoney": 0,
            "all_i": [],
            "all_daycount": [],
            "all_dayallprice": [],
        }
        allorders = orders.filter(time__year=year)
        if not orders.exists():
            context['errmsg'] = "您还没有数据"
        all_daycount = {}
        all_dayprice = {}
        context['year'] = year
        if context['year'] == None:
            context.pop('year')
        thisyear = int(datetime.datetime.now().strftime('%Y'))
        context['years'] = [i for i in range(thisyear, 1999, -1)]
        for i in range(1, 13):
            orders = allorders.filter(time__month=i)
            all_daycount[i] = 0
            all_dayprice[i] = 0
            if orders == None:
                continue
            else:
                for order in orders:
                    med_price = order.med_price
                    all["allmoney"] += med_price
                    total_count = order.total_count
                    all["allnum"] += total_count
                    all_daycount[i] += total_count
                    all_dayprice[i] += med_price

        for dayname in all_daycount.keys():
            all["all_i"].append(str(dayname) + "月")
            all["all_daycount"].append(all_daycount[dayname])
            all["all_dayallprice"].append(all_dayprice[dayname])
        all["all_i"] = json.dumps(all["all_i"], ensure_ascii=False)
        all["all_daycount"] = json.dumps(all["all_daycount"], ensure_ascii=False)
        all["all_dayallprice"] = json.dumps(all["all_dayallprice"], ensure_ascii=False)
    context['all'] = all
    return render(request, "salesDATA/finance_year.html", context=context)


# 接口
def finance_medicine_datas(request):
    # 判断是否登录
    context = {
        'page': 'order_list',
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        storeid = request.session.get('storeid')
        store = medstore.objects.get(pk=storeid)
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
        orders = Orders.objects.filter(drugstore=store)
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


def finance_staff_datas(request):
    # 判断是否登录
    context = {
        'page': 'order_list',
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        storeid = request.session.get('storeid')
        store = medstore.objects.get(pk=storeid)
        context['username'] = username
    else:
        return login(request)

    if request.method == 'GET':
        startdate = request.GET.get('startdate')
        enddate = request.GET.get('enddate')
        if startdate > enddate:
            startdate, enddate = enddate, startdate
        orders = Orders.objects.filter(drugstore=store)
        if orders == None:
            return HttpResponse("None")
        order1 = orders[0]
        if startdate == None:
            startdate = order1.time.strftime('%Y-%m-%d')
        if enddate == None:
            enddate = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        all = {
            "title": "从{}到{}的各员工销售数据：".format(startdate, enddate),
            "allnum": 0,
            "allmoney": 0,
            "all_staffname": [],
            "all_staffcount": [],
            "all_staffallprice": [],
        }
        orders = orders.filter(time__range=(startdate, enddate))
        if orders == None:
            return HttpResponse("None")
        all_staffcount = {}
        all_staffprice = {}
        all_staff = Staff.objects.filter(store=store)
        for staff in all_staff:
            staffname = staff.name
            all_staffcount[staffname] = 0
            all_staffprice[staffname] = 0

        # all["all_med"] = all_medcount
        for order in orders:  # 读取每一笔订单
            med_price = order.med_price
            all["allmoney"] += med_price
            total_count = order.total_count
            all["allnum"] += total_count
            staffname = order.staff.name
            if staffname in all_staffcount:
                all_staffcount[staffname] += total_count
                all_staffprice[staffname] += med_price
            else:
                all_staffcount[staffname] = total_count
                all_staffprice[staffname] = med_price
        for staffname in all_staffcount.keys():
            all["all_staffname"].append(staffname)
            all["all_staffcount"].append(all_staffcount[staffname])
            all["all_staffallprice"].append(all_staffprice[staffname])
    data = json.dumps(all, ensure_ascii=False)
    return HttpResponse(data)


def finance_month_datas(request):
    # 判断是否登录
    context = {
        'page': 'order_list',
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        storeid = request.session.get('storeid')
        store = medstore.objects.get(pk=storeid)
        context['username'] = username
    else:
        return login(request)

    if request.method == 'GET':
        year = request.GET.get('year')
        month = request.GET.get('month')
        # if startdate > enddate:
        #     startdate, enddate = enddate, startdate
        orders = Orders.objects.filter(drugstore=store)
        if orders == None:
            return HttpResponse("None")
        if year == None and month == None:
            year = datetime.datetime.now().strftime('%Y')
            month = datetime.datetime.now().strftime('%m')
        all = {
            "title": "{}年{}月的每日销售数据：".format(year, month),
            "allnum": 0,
            "allmoney": 0,
            "all_i": [],
            "all_daycount": [],
            "all_dayallprice": [],
        }
        allorders = orders.filter(time__year=year, time__month=month)
        if allorders == None:
            return HttpResponse("None")
        all_daycount = {}
        all_dayprice = {}
        days = int(calendar.monthrange(int(year), int(month))[1])
        for i in range(1, days + 1):
            orders = allorders.filter(time__day=i)
            all_daycount[i] = 0
            all_dayprice[i] = 0
            if orders == None:
                continue
            else:
                for order in orders:
                    med_price = order.med_price
                    all["allmoney"] += med_price
                    total_count = order.total_count
                    all["allnum"] += total_count
                    all_daycount[i] += total_count
                    all_dayprice[i] += med_price

        for dayname in all_daycount.keys():
            all["all_i"].append(str(month) + "-" + str(dayname))
            all["all_daycount"].append(all_daycount[dayname])
            all["all_dayallprice"].append(all_dayprice[dayname])
    data = json.dumps(all, ensure_ascii=False)
    return HttpResponse(data)


def finance_year_datas(request):
    # 判断是否登录
    context = {
        'page': 'order_list',
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        storeid = request.session.get('storeid')
        store = medstore.objects.get(pk=storeid)
        context['username'] = username
    else:
        return login(request)

    if request.method == 'GET':
        year = request.GET.get('year')
        # if startdate > enddate:
        #     startdate, enddate = enddate, startdate
        orders = Orders.objects.filter(drugstore=store)
        if orders == None:
            return HttpResponse("None")
        if year == None:
            year = datetime.datetime.now().strftime('%Y')
        all = {
            "title": "{}年的每月销售数据：".format(year),
            "allnum": 0,
            "allmoney": 0,
            "all_i": [],
            "all_daycount": [],
            "all_dayallprice": [],
        }
        allorders = orders.filter(time__year=year)
        if allorders == None:
            return HttpResponse("None")
        all_daycount = {}
        all_dayprice = {}
        for i in range(1, 13):
            orders = allorders.filter(time__month=i)
            all_daycount[i] = 0
            all_dayprice[i] = 0
            if orders == None:
                continue
            else:
                for order in orders:
                    med_price = order.med_price
                    all["allmoney"] += med_price
                    total_count = order.total_count
                    all["allnum"] += total_count
                    all_daycount[i] += total_count
                    all_dayprice[i] += med_price

        for dayname in all_daycount.keys():
            all["all_i"].append(str(dayname) + "月")
            all["all_daycount"].append(int(all_daycount[dayname]))
            all["all_dayallprice"].append(int(all_dayprice[dayname]))
    data = json.dumps(all, ensure_ascii=False)
    return HttpResponse(data)


def Echarts(request):
    return render(request, "salesDATA/Echarts1.html")
