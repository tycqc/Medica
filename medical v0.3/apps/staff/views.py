from apps.staff.models import Staff
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
# from django.contrib.auth import authenticate, login, logout
from store.views import login


# Create your views here.

def register_staff(request):
    context = {
        'page': 'register_staff',
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username
        if request.session.get('identity') != 'shopkeeper':
            context['errmsg'] = '请以店主账号登录'
            shopkeeper = False
            return render(request, 'staff/register_staff.html', context=context)
        else:
            shopkeeper = True
    else:
        return login(request)

    if request.method == "POST" and shopkeeper:
        username = request.POST.get('username')
        name = request.POST.get('name')
        password = request.POST.get('password')
        phonenumber=request.POST.get("phonenumber")
        desc=request.POST.get("desc")
        user_model = Staff.objects.filter(username=username).filter(store_id=store)

        # 参数验证
        if not all([username, name, password, phonenumber, desc]):
            # 参数不完整
            context['errmsg'] = '数据不完整'
            return render(request, 'staff/register_staff.html', context = context)

        if user_model: #不为NULL
            context['errmsg'] = '用户名已存在'
            return render(request, 'staff/register_staff.html',context = context)
        else:
            user = Staff()
            user.username = username
            user.name = name
            user.password = password
            user.phonenumber = phonenumber
            user.desc = desc
            user.store_id = store
            user.save()
            return redirect(reverse('staff:find_staff'))
    return render(request,'staff/register_staff.html',context = context)

def find_staff(request):
    context = {
        "page": "find_staff"
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username
        # if request.session.get('identity') != 'shopkeeper':
        #     context['errmsg'] = '请以店主账号登录'
        #     shopkeeper = False
        #     return render(request, 'store/find_staff.html', context=context)
        # else:
        #     shopkeeper = True
    else:
        return login(request)

    if request.method=="POST":
        name = request.POST.get("name")
        staff_model = Staff.objects.filter(store_id=store).filter(name=name)
        context["staff_model"] = staff_model
        return render(request, "staff/find_staff.html",context = context)
    else:
        staff_model = Staff.objects.filter(store_id=store)
        context["staff_model"] = staff_model
        return render(request, "staff/find_staff.html",context = context)

def detail_staff(request):
    context = {
        "page": "find_staff"
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username
        # if request.session.get('identity') != 'shopkeeper':
        #     context['errmsg'] = '请以店主账号登录'
        #     shopkeeper = False
        #     return render(request, 'store/find_staff.html', context=context)
        # else:
        #     shopkeeper = True
    else:
        return login(request)
    pk = request.GET.get('id')
    obj = Staff.objects.get(id=pk)
    context["staff"] = obj
    return render(request,'staff/detail_staff.html', context = context)

def del_staff(request):
    context = {
        "page": "find_staff"
    }
    shopkeeper = False
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username
        staff_model = Staff.objects.filter(store_id=store)
        context["staff_model"] = staff_model
        if request.session.get('identity') != 'shopkeeper':
            context['errmsg'] = '请以店主账号登录'
            shopkeeper = False
            return render(request, 'staff/find_staff.html', context=context)
        else:
            shopkeeper = True
    else:
        return login(request)

    if shopkeeper:
        pk = request.GET.get('id')
        obj = Staff.objects.get(id=pk)
        obj.delete()
        return redirect(reverse('staff:find_staff'))
    #return HttpResponse('删除成功')

def edit_staff(request):
    context = {
        "page": "find_staff"
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        store = request.session.get('storeid')
        context['username'] = username
        staff_model = Staff.objects.filter(store_id=store)
        context["staff_model"] = staff_model
        if request.session.get('identity') != 'shopkeeper':
            context['errmsg'] = '请以店主账号登录'
            shopkeeper = False
            # return redirect(reverse('staff:find_staff'))
            return render(request, 'staff/find_staff.html', context=context)
        else:
            shopkeeper = True
    else:
        return login(request)

    pk = request.GET.get('id')
    obj = Staff.objects.get(id=pk)
    if request.method == "POST" and shopkeeper:
        name = request.POST.get("name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        phonenumber = request.POST.get("phonenumber")
        desc = request.POST.get("desc")

        obj.name = name
        obj.username = username
        obj.password = password
        obj.phonenumber = phonenumber
        obj.desc = desc
        obj.save()
        return redirect(reverse('staff:find_staff'))
    context["obj"]  = obj
    return render(request, "staff/edit_staff.html",context = context)