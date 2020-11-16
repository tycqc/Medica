from staff.models import Staff
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def register_staff(request):
    store = request.session.get('storeid')
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        password = request.POST.get('password')
        phonenumber=request.POST.get("phonenumber")
        desc=request.POST.get("desc")
        user_model = Staff.objects.filter(username=username).filter(store_id=store)

        # 参数验证
        if not all([username, name, password, phonenumber, desc]):
            # 参数不完整
            return render(request, 'staff/register_staff.html', {'error_name': '数据不完整'})

        if user_model: #不为NULL

            return render(request, 'staff/register_staff.html',{'error_name':'用户名已存在'})
        else:
            user = Staff()
            user.username = username
            user.name = name
            user.password = password
            user.phonenumber = phonenumber
            user.desc = desc
            user.store_id = store
            user.save()
    return render(request,'staff/register_staff.html')



def find_staff(request):
    store = request.session.get('storeid')
    if request.method=="POST":
        name = request.POST.get("name")
        staff_model = Staff.objects.filter(store_id=store).filter(name=name)
        print(staff_model)
        return render(request, "staff/find_staff.html",{"staff_model":staff_model})
    else:
        staff_model = Staff.objects.filter(store_id=store)
        return render(request, "staff/find_staff.html",{"staff_model":staff_model})

def detail_staff(request):
    pk = request.GET.get('id')
    obj = Staff.objects.get(id=pk)
    return render(request,('staff/detail_staff.html'), {'staff': obj})

def del_staff(request):
    pk = request.GET.get('id')
    obj = Staff.objects.get(id=pk)
    obj.delete()
    return redirect(reverse('staff:find_staff'))
    #return HttpResponse('删除成功')

def edit_staff(request):
    pk = request.GET.get('id')
    obj = Staff.objects.get(id=pk)
    if request.method == "POST":
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
    return render(request, "staff/edit_staff.html",{'obj':obj})