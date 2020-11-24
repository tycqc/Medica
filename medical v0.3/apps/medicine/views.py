from apps.medicine.models import Medicine, Cart
from store.models import medstore
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import jieba



def add_medicine(request):
    drugstore = request.session.get('storeid')
    if request.method=="POST":
        name=request.POST.get("name")
        price=request.POST.get("price")
        desc=request.POST.get("desc")
        status=request.POST.get("status")
        stock=request.POST.get("stock")
        medicinecode=request.POST.get("medicinecode")
        unite = request.POST.get("unite")
        type=request.POST.get("type")
        # image=request.FILES.get("medicineimg")

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

    return render(request,"medicine/add_medicine.html")

def find_medicine(request):
    drugstore=request.session.get('storeid')
    if request.method=="POST":
        search = request.POST.get("name")
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
        return render(request, "medicine/find_medicine.html", {"medicine_model": med_details})
    else:
        medicine_model = Medicine.objects.filter(drugstore_id=drugstore)
        return render(request, "medicine/find_medicine.html",{"medicine_model":medicine_model})

def del_medicine(request):
    pk = request.GET.get('id')
    obj= Medicine.objects.get(id=pk)
    obj.delete()
    return redirect(reverse('medicine:find_medicine'))
    #return HttpResponse('删除成功')

def edit_medicine(request):
    pk = request.GET.get('id')
    obj = Medicine.objects.get(id=pk)
    if request.method == "POST":
        name=request.POST.get("name")
        medicinecode=request.POST.get("medicinecode")
        price=request.POST.get("price")
        desc=request.POST.get("desc")
        stock=request.POST.get("stock")
        unite = request.POST.get("unite")
        type=request.POST.get("type")
        status=request.POST.get("status")
        #image=request.FILES.get("medicineimg")

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
    return render(request, "medicine/edit_medicine.html",{'obj':obj})

def medicine_detail(request):
    pk = request.GET.get('id')
    obj = Medicine.objects.get(id=pk)
    return render(request, "medicine/medicine_detail.html",{"obj": obj})

def add_to_cart(request):

    goodsid = request.GET.get('id')
    goodsnum = request.GET.get('goodsnum')

    # 获取购物车里的数据
    carts = Cart.objects.filter(C_store_id=request.session.get('storeid')).filter(C_goods_id=goodsid)
    # 有数据
    if carts.exists():
        c_obj = carts.first()
        c_obj.C_goods_num = goodsnum

    # 没有数据创建新的
    else:
        c_obj = Cart()
        c_obj.C_goods_id = goodsid
        c_obj.C_store_id = request.session.get('storeid')
        c_obj.C_goods_num = goodsnum

    c_obj.save()

    if c_obj.C_goods_num == 0:
        Cart.objects.filter(pk=c_obj.id).delete()

    return redirect(reverse('medicine:cart_list'))


def cart_list(request):
    carts = Cart.objects.filter(C_store=request.session.get('storeid'))
    carts_ = []
    for med in carts:
        price = med.C_goods.price * med.C_goods_num
        context = {
            'id': med.id,
            'med_name': med.C_goods.name,
            'med_price': price,
            'med_count': med.C_goods_num,
            'med_id': med.C_goods_id,
        }
        carts_.append(context)
    return render(request, "medicine/cart_list.html", {"carts": carts_})


def del_cart_list(request):
    pk = request.GET.get('id')
    obj = Cart.objects.get(id=pk)
    obj.delete()
    return redirect(reverse('medicine:cart_list'))

def get_tag(dict_):
    tag = dict_.get('tag')
    return tag
