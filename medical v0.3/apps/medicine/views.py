from medicine.models import Medicine, Cart
from store.models import medstore
from store.views import login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import jieba
from django.forms.models import model_to_dict
import simplejson as json


def add_medicine(request):
    context = {
        "page": "add_medicine"
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        context['username'] = username

    else:
        return login(request)

    drugstore = request.session.get('storeid')
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        desc = request.POST.get("desc")
        status = request.POST.get("status")
        stock = request.POST.get("stock")
        medicinecode = request.POST.get("medicinecode")
        unite = request.POST.get("unite")
        type = request.POST.get("type")
        # image=request.FILES.get("medicineimg")
        if not all([name, price, desc, status, stock, medicinecode, unite, type]):
            context['errmsg'] = '数据不完整'
            return render(request, "medicine/add_medicine.html", context=context)
        medicine = Medicine()
        medicine.name = name
        medicine.price = price
        medicine.status = status
        medicine.desc = desc
        medicine.stock = stock
        medicine.medicinecode = medicinecode
        medicine.unite = unite
        medicine.type = type
        medicine.drugstore_id = drugstore

        medicine.save()

    return render(request, "medicine/add_medicine.html", context=context)


# def find_medicine(request):
#     context = {
#         "page": "find_medicine"
#     }
#     if request.session.get('is_login', None):
#         username = request.session.get('username')
#         store = request.session.get('storeid')
#         context['username'] = username
#         # if request.session.get('identity') != 'shopkeeper':
#         #     context['errmsg'] = '请以店主账号登录'
#         #     shopkeeper = False
#         #     return render(request, 'store/find_staff.html', context=context)
#         # else:
#         #     shopkeeper = True
#     else:
#         return login(request)
#
#     drugstore=request.session.get('storeid')
#     if request.method=="POST":
#         search = request.POST.get("name")
#         search_list = jieba.lcut(search)
#         # print(search_list)
#         med_details_ = Medicine.objects.filter(drugstore_id=drugstore).values()
#         med_details = []
#         for med_detail in med_details_:
#             # print(med_detail)
#             med_str = str(med_detail)
#             # print(med_str)
#             tag0 = 0
#             tag1 = 0
#             tag = 0
#             for word in search_list:
#                 if med_str.find(word) != -1:
#                     word_count = med_str.count(word)
#                     tag0 = tag0 + 10
#                     tag1 = tag1 + word_count
#                     tag = tag0 + tag1
#             if tag == 0:
#                 continue
#             med_detail.setdefault('tag', tag)
#             med_details.append(med_detail)
#         med_details.sort(key=get_tag, reverse=True)
#         # print(med_details)
#         context["medicine_model"] =med_details
#         return render(request, "medicine/find_medicine_1.html", context =context)
#     else:
#         medicine_model = Medicine.objects.filter(drugstore_id=drugstore)
#         context["medicine_model"] = medicine_model
#         return render(request, "medicine/find_medicine_1.html",context = context)

def find_medicine(request):
    context = {
        "page": "find_medicine"
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username

    else:
        return login(request)
    if request.method == 'POST':
        name = request.POST.get("name")
        context["name"] = name
    return render(request, "medicine/find_medicine.html", context=context)


def del_medicine(request):
    context = {
        "page": "find_medicine"
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username

    else:
        return login(request)

    pk = request.GET.get('id')
    obj = Medicine.objects.get(id=pk)
    obj.delete()
    return redirect(reverse('medicine:find_medicine'))
    # return HttpResponse('删除成功')


def edit_medicine(request):
    context = {
        "page": "find_medicine"
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username

    else:
        return login(request)

    pk = request.GET.get('id')
    obj = Medicine.objects.get(id=pk)
    if request.method == "POST":
        name = request.POST.get("name")
        medicinecode = request.POST.get("medicinecode")
        price = request.POST.get("price")
        desc = request.POST.get("desc")
        stock = request.POST.get("stock")
        unite = request.POST.get("unite")
        type = request.POST.get("type")
        status = request.POST.get("status")
        # image=request.FILES.get("medicineimg")

        obj.name = name
        obj.price = price
        obj.status = status
        obj.desc = desc
        obj.stock = stock
        obj.medicinecode = medicinecode
        obj.unite = unite
        obj.type_id = type

        obj.save()
        return redirect(reverse('medicine:find_medicine'))
    context['obj'] = obj
    return render(request, "medicine/edit_medicine.html", context=context)


def medicine_detail(request):
    context = {
        "page": "find_medicine"
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username

    else:
        return login(request)

    pk = request.GET.get('id')
    obj = Medicine.objects.get(id=pk)
    context["obj"] = obj
    return render(request, "medicine/medicine_detail.html", context=context)


def add_to_cart(request):
    context = {
        "page": "find_medicine"
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username
    else:
        return login(request)

    if request.method == "POST":
        goodsid = request.POST.get('id')
        goodsnum = request.POST.get('goodsnum')
        Cart1 = Cart.objects.filter(C_goods_id=goodsid).filter(C_store_id=store)
        if Cart1.exists():
            Cart1 = Cart1[0]
            Cart1.C_goods_num = goodsnum
            Cart1.save()
        else:
            c_obj = Cart()
            c_obj.C_goods_id = goodsid
            c_obj.C_store_id = store
            c_obj.C_goods_num = goodsnum
            c_obj.save()

        if goodsnum == 0:
            Cart.objects.filter(C_goods_id=goodsid).filter(C_store_id=store).filter(C_goods_num=goodsnum).delete()
        return redirect(reverse('medicine:cart_list'))
    elif request.method == "GET":
        goodsid = request.GET.get('id')
        if (goodsid == None):
            return redirect(reverse('medicine:find_medicine'))
        # 获取购物车里的数据
        carts = Cart.objects.filter(C_store_id=request.session.get('storeid')).filter(C_goods_id=goodsid)
        # 有数据
        if carts.exists():
            c_obj = carts.first()
            goodsnum = c_obj.C_goods_num

        # 没有数据创建新的
        else:
            goodsnum = 1

        if goodsnum == 0:
            Cart.objects.filter(pk=c_obj.id).delete()
    else:
        print("ok")
        return redirect(reverse('medicine:find_medicine'))
    good = Medicine.objects.filter(pk=goodsid)
    context["good"] = good[0]
    context["goodnum"] = goodsnum
    return render(request, "medicine/add_to_cart.html", context=context)


def cart_list(request):
    context = {
        "page": "find_medicine"
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username
        allprice = get_allprice(request)
    else:
        return login(request)
    context['allprice'] = allprice
    return render(request, "medicine/cart_list.html", context=context)


def del_cart_list(request):
    context = {
        "page": "find_medicine"
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username

    else:
        return login(request)

    pk = request.GET.get('id')
    obj = Cart.objects.get(id=pk)
    obj.delete()
    return redirect(reverse('medicine:cart_list'))


def get_tag(dict_):
    tag = dict_.get('tag')
    return tag


def cart_list_data(request):
    context = {
        "page": "find_medicine"
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username

    else:
        return login(request)

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
        data['med_price'] = str(data['med_price']) + "元"
        data['price'] = str(data['price']) + "元"
        data['del_cart'] = '<button class="button1" onclick="del_cart(' + id + ')">删除</button>'
        data['edit_cart'] = '<button class="button1" onclick="add(' + med_id + ')">修改数量</button>'
    num = len(carts_) + 1
    cart1 = {
        'id': "总价",
        'price': str(allprice) + "元",
    }
    carts_.append(cart1)
    return HttpResponse(
        '{"code":0,"msg":"","count":' + str(num) + ',"data":' + json.dumps(carts_, ensure_ascii=False) + "}",
        content_type="application/json")


# 返回json数据
def find_medicine_data(request):
    context = {
        "page": "find_medicine"
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username
    else:
        return login(request)

    drugstore = request.session.get('storeid')
    page = 1
    if request.GET.get("page") != None:
        page = int(request.GET.get("page"))
    limit = 30
    if request.GET.get("limit") != None:
        limit = int(request.GET.get("limit"))

    if request.GET.get("name") != None:
        search = request.GET.get("name")
        search_list = jieba.lcut(search)
        # print(search_list)
        med_details_ = Medicine.objects.filter(drugstore_id=drugstore).values()
        med_details = []
        for med_detail in med_details_:
            # print(med_detail)
            med_str = str(med_detail)
            # print(med_str)
            tag0 = 0
            tag1 = 0
            tag = 0
            for word in search_list:
                if med_str.find(word) != -1:
                    word_count = med_str.count(word)
                    tag0 = tag0 + 10
                    tag1 = tag1 + word_count
                    tag = tag0 + tag1
            if tag == 0:
                continue
            med_detail.setdefault('tag', tag)
            med_details.append(med_detail)
        med_details.sort(key=get_tag, reverse=True)
        # print(med_details)
        medicine_model = med_details
        all_medicine = []
        for medicine in medicine_model:
            id = str(medicine["id"])
            data = medicine
            data['del_medicine'] = '<button class="button1" onclick="del_medicine(' + id + ')">删除</button>'
            data[
                'edit_medicine'] = '<button class="button1" onclick="window.location.href=\'../edit_medicine/?id=' + id + '\'">编辑</button>'
            data[
                'medicine_detail'] = '<button class="button1" onclick="window.location.href=\'../medicine_detail/?id=' + id + '\'">详情</button>'
            data[
                'add_to_cart'] = '<button class="button1" onclick="add(' + id + ')">添加到购物车</button>'
            del data['image']
            all_medicine.append(data)
        num = len(all_medicine)

    else:
        medicine_model = Medicine.objects.filter(drugstore_id=drugstore)
        all_medicine = []
        for medicine in medicine_model:
            id = str(medicine.pk)
            data = model_to_dict(medicine)
            data['del_medicine'] = '<button class="button1" onclick="del_medicine(' + id + ')">删除</button>'
            data[
                'edit_medicine'] = '<button class="button1" onclick="window.location.href=\'../edit_medicine/?id=' + id + '\'">编辑</button>'
            data[
                'medicine_detail'] = '<button class="button1" onclick="window.location.href=\'../medicine_detail/?id=' + id + '\'">详情</button>'
            data['add_to_cart'] = '<button class="button1" onclick="add(' + id + ')">添加到购物车</button>'
            del data['image']
            all_medicine.append(data)
        num = len(all_medicine)

    x = (page - 1) * limit
    y = x + limit - 1
    medicines = []
    for i in range(x, y + 1):
        if i >= num:
            break
        medicines.append(all_medicine[i])
    return HttpResponse(
        '{"code":0,"msg":"","count":' + str(num) + ',"data":' + json.dumps(medicines, ensure_ascii=False) + "}",
        content_type="application/json")


def get_allprice(request):
    context = {
        "page": "find_medicine"
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username
    else:
        return login(request)

    carts = Cart.objects.filter(C_store=store)
    allprice = 0
    for med in carts:
        price = med.C_goods.price * med.C_goods_num
        allprice += price
    return allprice
