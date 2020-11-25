from store.models import medstore
from staff.models import Staff
from django.http import HttpResponseRedirect,HttpResponse

from django.shortcuts import render
import re,json

# Create your views here.
# def shiyan_index(request):
#     return render(request, 'layui样式.html')
# def shiyan(request):
#     data =[
# {"medicineMaterialName": "海风藤", "medicineMaterialAlias": "满坑香、荖藤、大风藤、岩胡椒。", "EnglishName": "Caulis Piperis Kadsurae。", "medicineMaterialSource": "为胡椒科胡椒属植物风藤Piper kadsura (Choisy)Ohwi[P.futokadsura Sieb.et Zucc.的藤茎。", "channelTropism": "性微温，味辛、苦。归肝经。","button":"<button>nothibg</button>"},
# {"medicineMaterialName": "青羊参 qingyangshe", "medicineMaterialAlias": "青阳参、白石参、毒狗药、地藕、小白蔹、白药、白芪、青洋参、闹狗药、牛尾参、牛尾七。", "EnglishName": "Radix Cynanchi Otophylli。", "medicineMaterialSource": "为萝藦科鹅绒属植物青羊参Cynanchum otophyllum Schneid.的根。", "channelTropism": "性温，味甘、辛。归心经、肝经、脾经。","button":"<button>nothibg</button>"},
# ]
#     return HttpResponse('{"code":0,"msg":"","count":20,"data":'+json.dumps(data, ensure_ascii=False)+"}", content_type="application/json")
# 药店，店主注册
def register(request):
    # 注册界面逻辑的处理
    # 接收参数
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        password = request.POST.get('password')
        cpwd = request.POST.get('cpwd')
        ypjyxkzcode = request.POST.get('ypjyxkzcode')
        time = request.POST.get('time')
        gspcode = request.POST.get('gspcode')
        desc = request.POST.get('desc')
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        allow = request.POST.get('allow')

        info = {}
        info["username"] = username
        info["name"] = name
        info["password"] = password
        info["cpwd"] = cpwd
        info["ypjyxkzcode"] = ypjyxkzcode
        info["time"] = time
        info["gspcode"] = gspcode
        info["desc"] = desc
        info["address"] = address
        info["postcode"] = postcode


        # 参数验证
        if not all([username, name, password, cpwd, ypjyxkzcode,
                    gspcode, desc, address, postcode]):
            # 参数不完整
            return render(request, 'store/REGISTER.html', {'info' : info, 'errmsg': '数据不完整'})

        # 用户名验证
        if len(username) > 20 or len(username) < 5:
            # 用户名不合格
            return render(request, 'store/REGISTER.html', {'info': info, 'errmsg': '请输入5-20个字符的用户名'})

        # 密码验证
        if len(password) <8 or len(password) >20:
            # 密码不合格
            return render(request, 'store/REGISTER.html', {'info': info, 'errmsg': '密码最少8位，最长20位'})

        # 密码一致性验证
        if password != cpwd:
            # 密码不一致
            return render(request, 'store/REGISTER.html', {'info' : info,'errmsg': '密码不一致'})

        # 是否同意使用协议
        if allow != 'on':
            # 协议不同意
            return render(request, 'store/REGISTER.html', {'info' : info,'errmsg': '请首先同意协议'})

        #用户名是否存在
        store = medstore.objects.filter(username=username)
        if store:
            return render(request, 'store/REGISTER.html', {'info' : info,'errmsg': '用户已存在'})

        # 注册
        try:
            store = medstore()
            store.username = username
            store.password = password
            store.cpwd = cpwd
            store.ypjyxkzcode = ypjyxkzcode
            store.gspcode = gspcode
            store.name = name
            store.desc = desc
            store.address = address
            store.postcode = postcode
            if time != "":
                store.time = time
            store.save()
        except:
            return render(request, 'store/REGISTER.html', {'info': info,'errmsg': '用户注册失败，请重试'})
        else: # try成功的奖励
            # 直接登录
            request.session['is_login'] = True
            request.session['username'] = store.username
            request.session['storeid'] = store.pk
            request.session['storename'] = store.name
            request.session['identity'] = "shopkeeper"
            return HttpResponseRedirect('/store/login')
    # 显示注册界面
    else:
        return render(request, 'store/REGISTER.html')

# 药店，店主，员工登录
def login(request,user = None):
    # print (request)
    # print(type(request))
    # 判断是否登录，已登录则返回信息详情页
    if request.session.get('is_login', None):
        return store_homepage(request)

    if request.method == "GET":
        # 判断是否已经记录了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request, 'store/login.html', {'username': username, 'checked': checked})

    # 登录
    elif request.method == "POST":
        is_staff = request.POST.get('is_staff')

        # 如果不是员工，即账号是店主
        if is_staff != "on":
            username = request.POST.get('username')
            password = request.POST.get('pwd')
            remember = request.POST.get('remember')


            # 重复登录检验
            if request.session.get('is_login', None):
                # 重复登录
                return render(request, 'store/login.html', {'errmsg': '已登陆其他账户(或其他设备)；请刷新试试'})

            # 参数验证
            if not all([username, password]):
                # 参数不完整
                return render(request, 'store/login.html', {'errmsg': '数据不完整'})

            # 业务处理：用户注册，验证用户是否存在
            # 业务处理:登录校验
            try:
                store = medstore.objects.get(username = username)
            except:
                return render(request, 'store/login.html', {'errmsg': '用户名不存在'})

            # 用户名密码正确
            if store.password == password:
                # 记录用户的登录状态
                request.session['is_login'] = True
                request.session['username'] = store.username
                request.session['storeid'] = store.pk
                request.session['storename'] = store.name
                request.session['identity'] = "shopkeeper"
                # 登录成功返回信息界面
                re = render(request, 'store/USER_INFO_homepage.html', {'username': store.username})

                # 判断是否需要记住用户名
                if remember == 'on':
                    # 记住用户名
                    re.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    re.delete_cookie('username')
                # 返回response
                return store_homepage(request)
            # 用户名或密码错误
            else:
                return render(request, 'store/login.html', {'errmsg': '用户名或密码错误'})


        elif is_staff == "on":
            username = request.POST.get('username')
            password = request.POST.get('pwd')
            remember = request.POST.get('remember')

            # 重复登录检验
            if request.session.get('is_login', None):
                # 重复登录
                return render(request, 'store/login.html', {'errmsg': '已登陆其他账户(或其他设备)；请刷新试试'})

            # 参数验证
            if not all([username, password]):
                # 参数不完整
                return render(request, 'store/login.html', {'errmsg': '数据不完整'})

            # 业务处理：用户注册，验证用户是否存在
            # 业务处理:登录校验
            try:
                staff = Staff.objects.get(username=username)
            except:
                return render(request, 'store/login.html', {'errmsg': '用户名不存在,或确认是否是员工'})

            # 用户名密码正确
            if staff.password == password:
                # 记录用户的登录状态
                request.session['is_login'] = True
                request.session['staffid'] = staff.id
                request.session['username'] = staff.username
                request.session['storeid'] = staff.store.pk
                request.session['staffname'] = staff.name
                request.session['identity'] = "staff"
                # 登录成功返回信息界面
                # 调用的函数
                return store_homepage(request)
                #return staff_views
            # 用户名或密码错误
            else:
                return render(request, 'store/login.html', {'errmsg': '用户名或密码错误'})
        # 用户名或密码错误
        else:
            return  render(request, 'store/login.html', {'errmsg': '登录失败，请重试'})

# 登出
def logout(request):
    """退出登录"""
    #if request.session.get('is_login', None):
    request.session.flush()
    return index(request)

# 药店信息详情页
def store_homepage(request):
    # 判断是否登录
    if request.session.get('is_login', None):
        storeid = request.session.get('storeid')
    else:
        return login(request)
    store = medstore.objects.get(pk=storeid)
    username = request.session.get('username')
    # 组织上下文
    context = {
        'username':username,
        'store': store,
        'page': 'homepage',
    }

    return render(request, 'store/USER_INFO_homepage.HTML', context=context)

# 药店信息详情修改
def store_homepage_update(request):
    # 判断是否登录
    context = {
        'page': 'homepage_update',
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        storeid = request.session.get('storeid')
        context['username'] = username
        if request.session.get('identity') != 'shopkeeper':
            context['errmsg'] = '请以店主账号登录'
            shopkeeper = False
            return render(request, 'store/USER_INFO_update.html', context=context)
        else:
            shopkeeper = True
    else:
        return login(request)

    if request.method == "POST" and shopkeeper:
        # 员工不可操作
        if request.session.get('identity') != 'shopkeeper':
            context['errmsg'] = '请以店主账号登录'
            return render(request, 'store/USER_INFO_update.html', context=context)

        else:
            store = medstore.objects.get(pk = storeid)
            Opassword = request.POST.get('Opassword')
            name = request.POST.get('name')
            password = request.POST.get('password')
            cpwd = request.POST.get('cpwd')
            ypjyxkzcode = request.POST.get('ypjyxkzcode')
            time = request.POST.get('time')
            gspcode = request.POST.get('gspcode')
            desc = request.POST.get('desc')
            address = request.POST.get('address')
            postcode = request.POST.get('postcode')
            allow = request.POST.get('allow')

            info = {}
            info['username'] = store.username
            info["name"] = name
            info["password"] = password
            info["cpwd"] = cpwd
            info["ypjyxkzcode"] = ypjyxkzcode
            info["time"] = time
            info["gspcode"] = gspcode
            info["desc"] = desc
            info["address"] = address
            info["postcode"] = postcode
            username = request.session.get('username')
            # 组织上下文
            context = {
                'username': username,
                'store': store,
                'info': info,
                'page': 'homepage_update'
            }
            # 原密码验证
            if Opassword != store.password:
                # 参数不完整
                context['errmsg'] = '原密码不正确'
                return render(request, 'store/USER_INFO_update.html', context = context)

            # 用户名验证
            if len(username) > 20 or len(username) < 5:
                # 用户名不合格
                context['errmsg'] = '请输入5-20个字符的用户名'
                return render(request, 'store/USER_INFO_update.html', context = context)

            # 密码验证
            if len(password) < 8 or len(password) > 20:
                # 密码不合格
                context['errmsg'] = '密码最少8位，最长20位'
                return render(request, 'store/USER_INFO_update.html', context = context)

            # 密码一致性验证
            if password != cpwd:
                # 密码不一致
                context['errmsg'] = '新密码不一致'
                return render(request, 'store/USER_INFO_update.html', context = context)

            # 是否同意使用协议
            if allow != 'on':
                # 协议不同意
                context['errmsg'] = '请首先同意协议'
                return render(request, 'store/USER_INFO_update.html', context = context)


            # 注册
            try:
                store.password = password
                store.cpwd = cpwd
                store.ypjyxkzcode = ypjyxkzcode
                store.gspcode = gspcode
                store.name = name
                store.desc = desc
                store.address = address
                store.postcode = postcode
                if time != "":
                    store.time = time
                store.save()
                print("OK")
            except:
                context['errmsg'] = '信息修改失败（可能是时间格式不正确），请重试'
                return render(request, 'store/USER_INFO_update.html', context = context)
            else:
                return store_homepage(request)
    else:
        # 员工不可操作
        if request.session.get('identity') != 'shopkeeper':
            context['errmsg'] = '请以店主账号登录'
            return render(request, 'store/USER_INFO_update.html', context = context)

        else:
            store = medstore.objects.get(pk=storeid)
            context ={
                'username': username,
                'store': store,
                'info': store,
                'page': 'homepage_update'
            }
        return render(request, 'store/USER_INFO_update.html', context=context)

# 药店注销
def store_cancellation(request):
    # 判断是否登录
    context = {
        'page': 'cancellation',
    }
    if request.session.get('is_login', None):
        storeid = request.session.get('storeid')
        username = request.session.get('username')
        context['username'] = username
        store = medstore.objects.get(pk=storeid)
        context["store"] =store
        if request.session.get('identity') != 'shopkeeper':
            context['errmsg'] = '请以店主账号登录'
            shopkeeper = False
            return render(request, 'store/CANCELLATION.HTML', context = context)
        else:
            shopkeeper = True
    else:
        return login(request)

    if request.method == "POST" and shopkeeper:
        # 员工不可操作
        context['errmsg'] = '请以店主账号登录'
        if request.session.get('identity') != 'shopkeeper':
            return render(request, 'store/CANCELLATION.HTML', context = context)

        else:
            store = medstore.objects.get(pk = storeid)
            staffs = Staff.objects.filter(store_id=store)
            context = {
                'store': store,
                'info': '',
                'page': 'cancellation'
            }
            # 是否同意使用协议
            allow = request.POST.get('allow')
            if allow != 'on':
                # 协议不同意
                context['errmsg'] = '请选勾选择确认注销'
                return render(request, 'store/CANCELLATION.html', context=context)

            # 注销
            try:
                # for staff in staffs:
                #     staff.delete()
                #
                store.delete()
                request.session.flush()
            except:
                context['errmsg'] = '注销失败，请重试'
                return render(request, 'store/CANCELLATION.html', context=context)
            else:
                return store_homepage(request)
    else:
        # 员工不可操作
        if request.session.get('identity') != 'shopkeeper':
            context['errmsg'] = '请以店主账号登录'
            return render(request, 'store/CANCELLATION.HTML', context =context)

        else:
            store = medstore.objects.get(pk=storeid)
            username = request.session.get('username')
            context = {
                'store': store,
                'info': store,
                'page': 'cancellation',
                'username': username

            }
        return render(request, 'store/CANCELLATION.HTML', context=context)

# 临时主页
def index(request):
    if request.session.get('is_login', None):
        username = request.session.get('storeusername')
        store = medstore.objects.get(username = username)
        return render(request, 'store/AAAshiyan.html', {'store':store})
    else:
        return render(request, 'store/AAAshiyan.html')
