import os
from datetime import datetime
import jieba
import simplejson as json
from django.db import transaction
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from staff.models import Staff
from medicine.models import Medicine, Cart
from orders.models import Orders, OrderGoods
from store.models import medstore
from store.views import login



# 线下订单添加
def staff_order_add(request):
    # 判断是否登录
    context = {
        'page': 'staff_order_add',
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username
        if request.session.get('identity') == 'shopkeeper':
            context['page'] = 'find_staff'
            context['errmsg'] = '请以员工账号登录，用以生成订单'
            shopkeeper = True
            return render(request, 'staff/find_staff.html', context=context)
        else:
            shopkeeper = False
    else:
        return login(request)

    store_id = request.session.get('storeid')
    staff_id = request.session.get('staffid')

    if request.POST.get('pay_method'):
        pay_method = request.POST.get('pay_method')
        carts = Cart.objects.filter(C_store=request.session.get('storeid'))
        med_price = 0
        count = 0
        ordergoods = []
        for med in carts:
            price = med.C_goods.price * med.C_goods_num
            context1 = {
                'med_name': med.C_goods.name,
                'med_price': price,
                'med_count': med.C_goods_num,
            }
            ordergoods.append(context1)
            med_price += price
            count += med.C_goods_num

        order = Orders()
        order.order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(store_id) + str(staff_id)
        order.staff_id = staff_id
        order.drugstore_id = store_id
        order.med_price = med_price
        order.transit_price = 0
        order.total_price = med_price
        order.total_count = count
        order.order_status = 4
        order.pay_method = int(pay_method)
        order.sale_method = 0  # 默认线下销售
        order.save()

        paymethod = ['现金支付', '微信支付', '支付宝']
        orderstatus = ['待支付', '待配送', '已送达', '待评价', '已完成']

        order_ = {
            'order_id': order.order_id,
            'staff': order.staff.name,
            # 'address': Order.addr,
            # 'receiver': address_.receiver,
            # 'phone': address_.phone,
            # 'drugstore': drug_store.name,
            'pay_method': paymethod[order.pay_method],
            'med_price': order.med_price,
            'total_count': order.total_count,
            'total_price': order.total_price,
            'transit_price': order.transit_price,
            'order_status': orderstatus[order.order_status],
        }

        for med in carts:
            price = med.C_goods.price * med.C_goods_num
            ordergood = OrderGoods()
            ordergood.sku_id = med.C_goods_id
            ordergood.order_id = order.order_id
            ordergood.count = med.C_goods_num
            ordergood.price = price
            ordergood.save()
            med_ = Medicine.objects.get(id=med.C_goods_id)
            med_.stock -= med.C_goods_num
            med_.sales += med.C_goods_num
            med_.save()
            med.delete()

        return redirect('orders:order_list')

    else:
        carts = Cart.objects.filter(C_store=request.session.get('storeid'))
        med_price = 0
        count = 0
        ordergoods = []
        for med in carts:
            price = med.C_goods.price * med.C_goods_num

            context1 = {
                'med_name': med.C_goods.name,
                'med_price': price,
                'med_count': med.C_goods_num,
            }
            ordergoods.append(context1)
            med_price += price
            count += med.C_goods_num

        order = Orders()
        order.order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(store_id) + str(staff_id)
        order.staff_id = staff_id
        order.drugstore_id = store_id
        order.med_price = med_price
        order.transit_price = 0
        order.total_price = med_price
        order.total_count = count
        order.order_status = 4

        paymethod = ['现金支付', '微信支付', '支付宝']
        orderstatus = ['待支付', '待配送', '已送达', '待评价', '已完成']
        staffname = Staff.objects.get(id=staff_id).name
        order_ = {
            'order_id': order.order_id,
            'staff': staffname,
            # 'address': Order.addr,
            # 'receiver': address_.receiver,
            # 'phone': address_.phone,
            # 'drugstore': drug_store.name,
            'med_price': order.med_price,
            'total_count': order.total_count,
            'total_price': order.total_price,
            'transit_price': order.transit_price,
            'order_status': orderstatus[order.order_status],
        }
    context['ordergoods'] = ordergoods
    context['order'] = order_
    return render(request, "orders/staff_order_add.html", context = context)


def order_details(request):
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

    id = request.GET.get("order_id")

    Order = Orders.objects.get(order_id=id)

    paymethod = ['现金支付', '微信支付', '支付宝']
    orderstatus = ['待支付', '待配送', '已送达', '待评价', '已完成']

    context1 = {
        'order': {
            'order_id': Order.order_id,
            'staff': Order.staff.name,
            # 'address': Order.addr,
            # 'receiver': address_.receiver,
            # 'phone': address_.phone,
            # 'drugstore': drug_store.name,
            'pay_method': paymethod[Order.pay_method],
            'med_price': Order.med_price,
            'total_count': Order.total_count,
            'total_price': Order.total_price,
            'transit_price': Order.transit_price,
            'order_status': orderstatus[Order.order_status],
        },
        'order_med': [
        ]
    }

    order_med = OrderGoods.objects.filter(order=Order.order_id)
    for med in order_med:
        med_detail = {
            'med_code': med.sku.medicinecode,
            'med_name': med.sku.name,
            'med_count': med.count,
            'med_price': med.price,
        }
        context1['order_med'].append(med_detail)
    context['context'] = context1
    return render(request, "orders/order_details.html", context = context)


def order_list(request):
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

    if request.POST.get("search_text") != None:
        search = request.POST.get("search_text")
        context['search_text'] = search
        id = request.session.get('storeid')
        Orders_ = Orders.objects.filter(drugstore=id)

        search_list = jieba.lcut(search)

        Orderlist = []
        paymethod = ['现金支付', '微信支付', '支付宝']
        orderstatus = ['待支付', '待配送', '已送达', '待评价', '已完成']

        for Order in Orders_:

            order_detail = {
                'order': {
                    'order_id': Order.order_id,
                    'staff': Order.staff.name,
                    # 'address': Order.addr,
                    # 'receiver': address_.receiver,
                    # 'phone': address_.phone,
                    # 'drugstore': drug_store.name,
                    'pay_method': paymethod[Order.pay_method],
                    'med_price': Order.med_price,
                    'total_count': Order.total_count,
                    'total_price': Order.total_price,
                    'transit_price': Order.transit_price,
                    'order_status': orderstatus[Order.order_status],
                },
                'order_med': []
            }

            order_med = OrderGoods.objects.filter(order=Order.order_id)
            for med in order_med:
                med_detail = {
                    'med_code': med.sku.medicinecode,
                    'med_name': med.sku.name,
                    'med_count': med.count,
                    'med_price': med.price,
                }
                order_detail['order_med'].append(med_detail)
            tag0 = 0
            tag1 = 0
            tag = 0
            order_str = str(order_detail)
            for word in search_list:
                if order_str.find(word) != -1:
                    word_count = order_str.count(word)
                    tag0 = tag0 + 10
                    tag1 = tag1 + word_count
                    tag = tag0 + tag1
            if tag == 0:
                continue

            # address_ = Order.addr
            # drug_store = Order.drugstore
            context1 = {
                'order_id': Order.order_id,
                'staff': Order.staff.name,
                # 'address': address_.addr,
                # 'receiver': address_.receiver,
                # 'phone': address_.phone,
                # 'drugstore': drug_store.name,
                # 'pay_method': paymethod[Order.pay_method],
                'total_count': Order.total_count,
                'total_price': Order.total_price,
                'order_status': orderstatus[Order.order_status],
                'tag': tag,
            }
            Orderlist.append(context1)
        Orderlist.sort(key=get_tag, reverse=True)
    else:
        id = request.session.get('storeid')
        Orders_ = Orders.objects.filter(drugstore=id)

        Orderlist = []
        # paymethod = ['现金支付', '微信支付', '支付宝']
        orderstatus = ['待支付', '待配送', '已送达', '待评价', '已完成']

        for Order in Orders_:
            # address_ = Order.addr
            # drug_store = Order.drugstore
            context1 = {
                'order_id': Order.order_id,
                'staff': Order.staff.name,
                # 'address': address_.addr,
                # 'receiver': address_.receiver,
                # 'phone': address_.phone,
                # 'drugstore': drug_store.name,
                # 'pay_method': paymethod[Order.pay_method],
                'total_count': Order.total_count,
                'total_price': Order.total_price,
                'order_status': orderstatus[Order.order_status],
            }

            Orderlist.append(context1)
    context['orderlist'] = Orderlist
    return render(request, "orders/find_orders.html", context = context)


def find_order_data(request):
    context = {
        "page": "find_medicine"
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username
    else:
        return login(request)

    if request.GET.get("search_text"):
        search = request.GET.get("search_text")
        id = request.session.get('storeid')
        Orders_ = Orders.objects.filter(drugstore=id)

        search_list = jieba.lcut(search)

        Orderlist = []
        paymethod = ['现金支付', '微信支付', '支付宝']
        orderstatus = ['待支付', '待配送', '已送达', '待评价', '已完成']

        for Order in Orders_:

            order_detail = {
                'order': {
                    'order_id': Order.order_id,
                    'staff': Order.staff.name,
                    # 'address': Order.addr,
                    # 'receiver': address_.receiver,
                    # 'phone': address_.phone,
                    # 'drugstore': drug_store.name,
                    'pay_method': paymethod[Order.pay_method],
                    'med_price': Order.med_price,
                    'total_count': Order.total_count,
                    'total_price': Order.total_price,
                    'transit_price': Order.transit_price,
                    'order_status': orderstatus[Order.order_status],
                },
                'order_med': []
            }

            order_med = OrderGoods.objects.filter(order=Order.order_id)
            for med in order_med:
                med_detail = {
                    'med_code': med.sku.medicinecode,
                    'med_name': med.sku.name,
                    'med_count': med.count,
                    'med_price': med.price,
                }
                order_detail['order_med'].append(med_detail)
            tag0 = 0
            tag1 = 0
            tag = 0
            order_str = str(order_detail)
            for word in search_list:
                if order_str.find(word) != -1:
                    word_count = order_str.count(word)
                    tag0 = tag0 + 10
                    tag1 = tag1 + word_count
                    tag = tag0 + tag1
            if tag == 0:
                continue

            # address_ = Order.addr
            # drug_store = Order.drugstore
            context1 = {
                'order_id': Order.order_id,
                'staff': Order.staff.name,
                # 'address': address_.addr,
                # 'receiver': address_.receiver,
                # 'phone': address_.phone,
                # 'drugstore': drug_store.name,
                # 'pay_method': paymethod[Order.pay_method],
                'total_count': Order.total_count,
                'total_price': Order.total_price,
                'order_status': orderstatus[Order.order_status],
                'tag': tag,
            }
            Orderlist.append(context1)
        Orderlist.sort(key=get_tag, reverse=True)
    else:
        id = request.session.get('storeid')
        Orders_ = Orders.objects.filter(drugstore=id)

        Orderlist = []
        # paymethod = ['现金支付', '微信支付', '支付宝']
        orderstatus = ['待支付', '待配送', '已送达', '待评价', '已完成']

        for Order in Orders_:
            # address_ = Order.addr
            # drug_store = Order.drugstore
            context1 = {
                'order_id': Order.order_id,
                'staff': Order.staff.name,
                # 'address': address_.addr,
                # 'receiver': address_.receiver,
                # 'phone': address_.phone,
                # 'drugstore': drug_store.name,
                # 'pay_method': paymethod[Order.pay_method],
                'total_count': Order.total_count,
                'total_price': Order.total_price,
                'order_status': orderstatus[Order.order_status],
            }

            Orderlist.append(context1)
    num = len(Orderlist)
    page = 1
    if request.GET.get("page") != None:
        page = int(request.GET.get("page"))
    limit = 30
    if request.GET.get("limit") != None:
        limit = int(request.GET.get("limit"))
    x = (page - 1) * limit
    y = x + limit - 1
    order = []
    for i in range(x, y + 1):
        if i >= num:
            break
        order.append(Orderlist[i])
    for order1 in order:
        id = order1['order_id']
        order1['del_cart'] ='<button class="button1" onclick="del_order('+id+')">删除</button>'
        order1['order_details'] ='<button class="button1" onclick="window.location.href=\'../order_details/?order_id=' + id + '\'">详情</button>'

    return HttpResponse(
        '{"code":0,"msg":"","count":' + str(num) + ',"data":' + json.dumps(order, ensure_ascii=False) + "}",
        content_type="application/json")


    carts = Cart.objects.filter(C_store=store)
    carts_ = []
    allprice = 0
    for med in carts:
        price = med.C_goods.price * med.C_goods_num
        allprice += price
        cart1 = {
            'id': med.id,
            'med_name': med.C_goods.name,
            'price': price,
            'med_count': med.C_goods_num,
            'med_id': med.C_goods_id,
            'med_price': med.C_goods.price
        }
        carts_.append(cart1)
    for data in carts_:
        med_id = str(data['med_id'])
        id = str(data['id'])
        data['med_price'] = str(data['med_price'])+"元"
        data['price'] = str(data['price'])+"元"
        data['del_cart'] ='<button class="button1" onclick="del_cart('+id+')">删除</button>'
        data['edit_cart'] ='<button class="button1" onclick="add('+med_id+')">修改数量</button>'


def del_order(request):
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

    id = request.GET.get('order_id')
    obj = Orders.objects.get(order_id=id)
    obj.delete()
    order_med = OrderGoods.objects.filter(order=id)
    for med in order_med:
        med.delete()
    return redirect(reverse('orders:order_list'))


def finance(request):
    # 判断是否登录
    context = {
        'page': 'homepage_update',
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        storeid = request.session.get('storeid')
        context['username'] = username

    else:
        return login(request)

    year = request.POST.get('time1')
    month = request.POST.get('time2')
    id = request.session.get('storeid')
    Orders_ = Orders.objects.filter(drugstore=id)

    order_y_m = []
    for order in Orders_:
        if year and month:
            if order.time.strftime('%Y%m') == str(year) + str(month):
                order_y_m.append(order)
        if year and not month:
            if order.time.strftime('%Y') == str(year):
                order_y_m.append(order)

    total_in = 0
    for i in order_y_m:
        total_in += i.med_price
    return render(request, "orders/finance.html", total_in)


def get_tag(dict_):
    tag = dict_.get('tag')
    return tag
