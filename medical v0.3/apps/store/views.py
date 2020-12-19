from store.models import medstore, EmailVerifyRecord
from staff.models import Staff
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
import re, json


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
        email = request.POST.get('email')

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
        info["email"] = email

        # 参数验证
        if not all([username, name, password, cpwd, ypjyxkzcode,
                    gspcode, desc, address, postcode]):
            # 参数不完整
            return render(request, 'store/REGISTER.html', {'info': info, 'errmsg': '数据不完整'})

        # 用户名验证
        if len(username) >= 5 and len(username) <= 20:
            # pattern = "/^1(?:3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8|8\d|9|d)\d{8}$"
            # if re.match(pattern,)
            True
        else:
            # 用户名不合格
            return render(request, 'store/REGISTER.html', {'info': info, 'errmsg': '请输入5-20个字符的用户名'})

        # 密码验证
        if len(password) < 8 or len(password) > 20:
            # 密码不合格
            return render(request, 'store/REGISTER.html', {'info': info, 'errmsg': '密码最少8位，最长20位'})

        # 密码一致性验证
        if password != cpwd:
            # 密码不一致
            return render(request, 'store/REGISTER.html', {'info': info, 'errmsg': '密码不一致'})

        # GSP编号
        pattern = "^[A-C]{1}\-[A-Z]{2,5}[0-9]{2}\-[0-9]{3,4}$"
        b = re.match(pattern, gspcode)
        if b == None:
            return render(request, 'store/REGISTER.html', {'info': info, 'errmsg': 'GSP编号不合格'})

        # 邮箱格式
        pattern = "^[A-Za-z0-9\u4e00-\u9fa5]*@[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*$"
        b = re.match(pattern, email)
        if b == None:
            return render(request, 'store/REGISTER.html', {'info': info, 'errmsg': '邮箱格式不正确'})

        # 经营许可证编号
        pattern = "^[\u4e00-\u9fff]{1}[A-D]{1}[A-B]{1}[0-9]{7}$"
        b = re.match(pattern, ypjyxkzcode)
        if b == None:
            return render(request, 'store/REGISTER.html', {'info': info, 'errmsg': '经营许可证编号不合格'})

        # 时间编号
        pattern = "^[0-9]{4}\-(((0[13578]|(10|12))\-(0[1-9]|[1-2][0-9]|3[0-1]))|(02\-(0[1-9]|[1-2][0-9]))|((0[469]|11)\-(0[1-9]|[1-2][0-9]|30)))$"
        b = re.match(pattern, time)
        if b == None:
            return render(request, 'store/REGISTER.html', {'info': info, 'errmsg': '时间编号不合格'})

        # 是否同意使用协议
        if allow != 'on':
            # 协议不同意
            return render(request, 'store/REGISTER.html', {'info': info, 'errmsg': '请首先同意协议'})

        # 用户名是否存在
        store = medstore.objects.filter(username=username)
        if store:
            return render(request, 'store/REGISTER.html', {'info': info, 'errmsg': '用户已存在'})

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
            store.email = email
            store.emailstatus = "未激活"

            if time != "":
                store.time = time
            store.save()
        except:
            return render(request, 'store/REGISTER.html', {'info': info, 'errmsg': '用户注册失败，请重试'})
        else:  # try成功的奖励
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
def login(request, user=None):
    # print (request)
    # print(type(request))
    # 判断是否登录，已登录则返回信息详情页
    if request.session.get('is_login', None):
        return store_homepage(request)

    if request.method == "GET":
        if request.GET.get('errmsg') == "重置成功":
            return render(request, 'store/login.html', {'errmsg': '密码修改成功请登录'})
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
                store = medstore.objects.get(username=username)
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
                re = render(request, 'store/LOGIN.html', {'username': store.username})

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
                # return staff_views
            # 用户名或密码错误
            else:
                return render(request, 'store/login.html', {'errmsg': '用户名或密码错误'})
        # 用户名或密码错误
        else:
            return render(request, 'store/login.html', {'errmsg': '登录失败，请重试'})


# 登出
def logout(request):
    """退出登录"""
    # if request.session.get('is_login', None):
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
        'username': username,
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
            store = medstore.objects.get(pk=storeid)
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
            email = request.POST.get('email')

            info = {}
            info['username'] = store.username
            info["name"] = name
            info["email"] = email
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
            if email != store.email:
                # 参数不完整
                emailstatus1 = "未激活"

            if Opassword != store.password:
                # 参数不完整
                context['errmsg'] = '原密码不正确'
                return render(request, 'store/USER_INFO_update.html', context=context)

            # 用户名验证
            if len(username) > 20 or len(username) < 5:
                # 用户名不合格
                context['errmsg'] = '请输入5-20个字符的用户名'
                return render(request, 'store/USER_INFO_update.html', context=context)

            # 密码验证
            if len(password) < 8 or len(password) > 20:
                # 密码不合格
                context['errmsg'] = '密码最少8位，最长20位'
                return render(request, 'store/USER_INFO_update.html', context=context)

            # 密码一致性验证
            if password != cpwd:
                # 密码不一致
                context['errmsg'] = '新密码不一致'
                return render(request, 'store/USER_INFO_update.html', context=context)

            # GSP编号
            pattern = "^[A-C]{1}\-[A-Z]{2,5}[0-9]{2}\-[0-9]{3,4}$"
            b = re.match(pattern, gspcode)
            if b == None:
                context['errmsg'] = 'GSP编号不合格'
                return render(request, 'store/REGISTER.html', context=context)

            # 邮箱格式
            pattern = "^[A-Za-z0-9\u4e00-\u9fa5]*@[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*$"
            b = re.match(pattern, email)
            if b == None:
                context['errmsg'] = '邮箱格式不正确'
                return render(request, 'store/REGISTER.html', context=context)

            # 经营许可证编号
            pattern = "^[\u4e00-\u9fff]{1}[A-D]{1}[A-B]{1}[0-9]{7}$"
            b = re.match(pattern, ypjyxkzcode)
            if b == None:
                context['errmsg'] = '经营许可证编号不合格'
                return render(request, 'store/REGISTER.html', context=context)

            # 时间编号
            pattern = "^[0-9]{4}\-(((0[13578]|(10|12))\-(0[1-9]|[1-2][0-9]|3[0-1]))|(02\-(0[1-9]|[1-2][0-9]))|((0[469]|11)\-(0[1-9]|[1-2][0-9]|30)))$"
            b = re.match(pattern, time)
            if b == None:
                context['errmsg'] = '时间编号不合格'
                return render(request, 'store/REGISTER.html', context=context)

            # 是否同意使用协议
            if allow != 'on':
                # 协议不同意
                context['errmsg'] = '请首先同意协议'
                return render(request, 'store/USER_INFO_update.html', context=context)

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
                store.email = email
                store.emailstatus = emailstatus1
                if time != "":
                    store.time = time
                store.save()
                print("OK")
            except:
                context['errmsg'] = '信息修改失败（可能是时间格式不正确），请重试'
                return render(request, 'store/USER_INFO_update.html', context=context)
            else:
                return store_homepage(request)
    else:
        # 员工不可操作
        if request.session.get('identity') != 'shopkeeper':
            context['errmsg'] = '请以店主账号登录'
            return render(request, 'store/USER_INFO_update.html', context=context)

        else:
            store = medstore.objects.get(pk=storeid)
            context = {
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
        context["store"] = store
        if request.session.get('identity') != 'shopkeeper':
            context['errmsg'] = '请以店主账号登录'
            shopkeeper = False
            return render(request, 'store/CANCELLATION.HTML', context=context)
        else:
            shopkeeper = True
    else:
        return login(request)

    if request.method == "POST" and shopkeeper:
        # 员工不可操作
        context['errmsg'] = '请以店主账号登录'
        if request.session.get('identity') != 'shopkeeper':
            return render(request, 'store/CANCELLATION.HTML', context=context)

        else:
            store = medstore.objects.get(pk=storeid)
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
            return render(request, 'store/CANCELLATION.HTML', context=context)

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
        store = medstore.objects.get(username=username)
        return render(request, 'store/AAAshiyan.html', {'store': store})
    else:
        return render(request, 'store/AAAshiyan.html')


def forget_password(request):
    # 判断是否登录
    context = {}
    if request.session.get('is_login', None):
        storeid = request.session.get('storeid')
        username = request.session.get('username')
        context['username'] = username
        store = medstore.objects.get(pk=storeid)
        email = store.email
        context["store"] = store
        context["email"] = email
        if request.session.get('identity') != 'shopkeeper':
            return redirect('store:homepage_update')
        else:
            request.session.flush()
            return render(request, 'store/forget_password.html', context=context)

    if request.method == 'POST':
        email = request.POST.get("email")
        if email:
            store = medstore.objects.get(email=email)
            context['email'] = email
        else:
            context['check_errmsg'] = "这个邮箱不在系统"
            return render(request, 'store/forget_password.html', context=context)
        try:
            email_record = EmailVerifyRecord.objects.get(email=email)
        except:
            context['check_errmsg'] = "还未发送邮件"
            return render(request, 'store/forget_password.html', context=context)

        code = request.POST.get("code")
        if code:
            if code == email_record.code:
                try:
                    emailrecord = {
                        'email': store.email,
                        'emailstatus': store.emailstatus
                    }
                    context['emailrecord'] = emailrecord
                    context["check_errmsg"] = "激活成功"
                    request.session['is_check'] = True
                    request.session['email'] = email
                    return redirect('store:reset_password')
                except:
                    context["check_errmsg"] = "未激活，请稍后重试"
            else:
                context["check_errmsg"] = "验证码不正确，请稍后重试"
        else:
            context["check_errmsg"] = "请填写验证码"
        return render(request, 'store/forget_password.html', context=context)

    if request.method == 'GET':
        email = request.GET.get('email')
        if email:
            context['email'] = email
        return render(request, 'store/forget_password.html', context=context)


def email_s2(request):
    context = {
        'page': 'forget_password',
    }
    if request.method == "POST":
        mail_message = {}
        try:
            try:
                email = request.POST.get("email")
                context['email'] = email
            except:
                context['send_errmsg'] = "请输入验证码"
                return render(request, 'store/forget_password.html', context=context)
            try:
                store = medstore.objects.get(email=email)
            except:
                context['send_errmsg'] = "该邮箱未注册"
                return render(request, 'store/forget_password.html', context=context)
            mail_message = {
                'code': "0", 'email': email, 'error_email': ''
            }

            emailrecord = EmailVerifyRecord.objects.filter(email=email).first()
            if emailrecord:
                nowtime = datetime.datetime.now()
                lasttime = emailrecord.send_time
                lasttime = lasttime.replace(tzinfo=None)
                sec = (nowtime - lasttime).seconds
                if int(sec) <= 60:
                    context['send_errmsg'] = "请{0}秒后重试".format(60 - sec)
                    return render(request, 'store/forget_password.html', context=context)

            # 发送邮箱
            res_email = send_code_email(email, 'forget')
            if res_email:
                mail_message['code'] = "OK"
                mail_message['error_email'] = "发送成功"
                context["send_errmsg"] = mail_message['error_email']
                return render(request, 'store/forget_password.html', context=context)
            else:
                mail_message['code'] = "fail"
                mail_message['error_email'] = "发送失败, 请稍后重试"
                context["send_errmsg"] = mail_message['error_email']
                return render(request, 'store/forget_password.html', context=context)

        except Exception as e:
            print("错误信息 : ", e)
            mail_message['code'] = "fail"
            mail_message['error_email'] = "验证错误, 请稍后重试(注意检查邮箱格式)"
            context["send_errmsg"] = mail_message['error_email']
        return render(request, 'store/forget_password.html', context=context)

    if request.method == "GET":
        if request.GET.get('email'):
            context['email'] = request.GET.get('email')
        return render(request, 'store/forget_password.html', context=context)


def reset_password(request):
    if request.session.get('is_check', None):
        email = request.session.get('email')
        store = medstore.objects.get(email=email)
    else:
        context = {
            "check_errmsg": "请填写验证码"
        }
        return render(request, 'store/email_check.html', context=context)

    if request.method == 'POST':
        password = request.POST.get('password')
        copypassword = request.POST.get('copypassword')
        info = {
            'password': password,
            'copypassword': copypassword
        }
        context = {
            'info': info
        }
        if not all([password, copypassword]):
            context = {
                "errmsg": "请填写密码"
            }
            return render(request, 'store/reset_password.html', context=context)
        if password != copypassword:
            context = {
                "errmsg": "两次密码不一致"
            }
            return render(request, 'store/reset_password.html', context=context)
        # 密码验证
        if len(password) < 8 or len(password) > 20:
            # 密码不合格
            context = {
                "errmsg": "密码最少8位，最长20位"
            }
            return render(request, 'store/REGISTER.html', context=context)

        try:
            store.password = password
            store.save()
            request.session.flush()
            # request.session['is_login'] = True
            # request.session['username'] = store.username
            # request.session['storeid'] = store.pk
            # request.session['storename'] = store.name
            # request.session['identity'] = "shopkeeper"
            context = {
                "errmsg": "重置成功"
            }
            return render(request, 'store/reset_password.html', context=context)
        except:
            context = {
                "errmsg": "重置失败，请重试"
            }
            return render(request, 'store/reset_password.html', context=context)

    if request.method == 'GET':
        return render(request, 'store/reset_password.html')


def forget_email(request):
    # 界面逻辑的处理
    # 验证参数
    # 接收参数
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        ypjyxkzcode = request.POST.get('ypjyxkzcode')
        gspcode = request.POST.get('gspcode')

        info = {}
        info["username"] = username
        info["name"] = name
        info["ypjyxkzcode"] = ypjyxkzcode
        info["gspcode"] = gspcode

        # 参数验证
        if not all([username, name, ypjyxkzcode, gspcode]):
            # 参数不完整
            return render(request, 'store/forget_email.html', {'info': info, 'errmsg': '数据不完整'})

        # 用户名验证
        try:
            try:
                store = medstore.objects.get(username=username)
            except:
                store = medstore.objects.get(name=name)
        except:
            return render(request, 'store/forget_email.html', {'info': info, 'errmsg': '用户或药店名不存在'})

        # 信息是否完整
        if store:
            check = [False, False, False, False]
            check[0] = (store.username == username)
            check[1] = (store.name == name)
            check[2] = (store.ypjyxkzcode == ypjyxkzcode)
            check[3] = (store.gspcode == gspcode)
            if False not in check:
                email = store.email
                emailstatus = store.emailstatus
                context = {'info': info, 'errmsg': '验证成功', 'email': email}
                context['emailstatus'] = emailstatus
                return render(request, 'store/forget_email.html', context=context)
            else:
                return render(request, 'store/forget_email.html', {'info': info, 'errmsg': '验证失败'})

    # 显示界面
    else:
        return render(request, 'store/forget_email.html')


def email_check(request):
    context = {
        'page': 'email_check',
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        storeid = request.session.get('storeid')
        store = medstore.objects.get(pk=storeid)
        emailrecord = {
            'email': store.email,
            'emailstatus': store.emailstatus
        }
        context['emailrecord'] = emailrecord
        context['username'] = username
        if request.session.get('identity') != 'shopkeeper':
            context['send_errmsg'] = '请以店主账号登录'
            shopkeeper = False
            return render(request, 'store/email_check.html', context=context)
        else:
            shopkeeper = True
    else:
        return login(request)

    if request.method == "POST" and shopkeeper:
        try:
            email = request.POST.get("email")
            email_record = EmailVerifyRecord.objects.get(email=email)
        except:
            context["check_errmsg"] = "还没有发送邮件"
            return render(request, 'store/email_check.html', context=context)
        code = request.POST.get("code")
        if code:
            if code == email_record.code:
                try:
                    store.emailstatus = "已激活"
                    store.save()
                    emailrecord = {
                        'email': store.email,
                        'emailstatus': store.emailstatus
                    }
                    context['emailrecord'] = emailrecord
                    context["check_errmsg"] = "激活成功"
                except:
                    context["check_errmsg"] = "未激活，请稍后重试"
            else:
                context["check_errmsg"] = "验证码不正确，请稍后重试"
        else:
            context["check_errmsg"] = "请填写验证码"
        return render(request, 'store/email_check.html', context=context)

    else:
        return render(request, 'store/email_check.html', context=context)


# 注册发送邮箱验证码
def email_s(request):
    context = {
        'page': 'email_check',
    }
    if request.session.get('is_login', None):
        username = request.session.get('username')
        storeid = request.session.get('storeid')
        store = medstore.objects.get(pk=storeid)
        emailrecord = {
            'email': store.email,
            'emailstatus': store.emailstatus
        }
        context['emailrecord'] = emailrecord
        context['username'] = username
        if request.session.get('identity') != 'shopkeeper':
            context['send_errmsg'] = '请以店主账号登录'
            shopkeeper = False
            return render(request, 'store/email_check.html', context=context)
        else:
            shopkeeper = True
    else:
        return login(request)

    if request.method == "POST" and shopkeeper:
        mail_message = {}
        try:
            email = request.POST.get("email")
            mail_message = {
                'code': "0", 'email': email, 'error_email': ''
            }

            user_obj = medstore.objects.filter(email=email, emailstatus="已激活").first()
            emailrecord = EmailVerifyRecord.objects.filter(email=email).first()
            if user_obj:
                mail_message['code'] = "fail"
                mail_message['error_email'] = "邮箱已注册"
                context['send_errmsg'] = "邮箱已注册"
                return render(request, 'store/email_check.html', context=context)
            else:
                if emailrecord:
                    nowtime = datetime.datetime.now()
                    lasttime = emailrecord.send_time
                    lasttime = lasttime.replace(tzinfo=None)
                    sec = (nowtime - lasttime).seconds
                    if int(sec) <= 60:
                        context['send_errmsg'] = "请{0}秒后重试".format(60 - sec)
                        return render(request, 'store/email_check.html', context=context)

                    # 发送邮箱

                res_email = send_code_email(email)
                if res_email:
                    mail_message['code'] = "OK"
                    mail_message['error_email'] = "发送成功"
                    context["send_errmsg"] = mail_message['error_email']
                    return render(request, 'store/email_check.html', context=context)
                else:
                    mail_message['code'] = "fail"
                    mail_message['error_email'] = "验证码发送失败, 请稍后重试"
                    context["send_errmsg"] = mail_message['error_email']
                    return render(request, 'store/email_check.html', context=context)

        except Exception as e:
            print("错误信息 : ", e)
            mail_message['code'] = "fail"
            mail_message['error_email'] = "验证错误, 请稍后重试(注意检查邮箱格式)"
            context["send_errmsg"] = mail_message['error_email']
            return render(request, 'store/email_check.html', context=context)
    else:
        return render(request, 'store/email_check.html', context=context)


# 邮箱发送所需函数
from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from store.models import EmailVerifyRecord  # 邮箱验证model
from django.conf import settings  # setting.py添加的的配置信息
import datetime


# 生成随机字符串
def random_str(randomlength=4):
    """
    随机字符串
    :param randomlength: 字符串长度
    :return: String 类型字符串
    """
    str = ""
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送电子邮件
def send_code_email(email, send_type="register"):
    """
    发送电子邮件
    :param email: 要发送的邮箱
    :param send_type: 邮箱类型
    :return: True/False
    """
    try:
        email_record = EmailVerifyRecord.objects.get(email=email)
    except:
        email_record = EmailVerifyRecord()
    # 将给用户发的信息保存在数据库中
    code = random_str()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.send_time = datetime.datetime.now().replace(tzinfo=None)
    # 初始化为空
    email_title = ""
    email_body = ""
    # 如果为注册类型
    if send_type == "register":
        email_title = "绑定邮箱"
        # email_body = "请点击下面的链接激活你的账号:http://127.0.0.1:8000/active/{0}".format(code)
        email_body = "您的邮箱注册验证码为：{0}, 请及时进行验证，若不是您本人操作，请忽略。".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    if send_type == "forget":
        email_title = "找回密码"
        email_body = "您正在找回密码，验证码为：{0}, 请及时进行验证，若不是您本人操作，请忽略。".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    email_record.save()
    return True

from rest_framework.views import APIView
from rest_framework.response import Response

from store.models import medstore
from medicine.models import Medicine
import requests
import json
import  jieba

from django.forms.models import model_to_dict

def get_tag(dict_):
    tag = dict_.get('tag')
    return tag

class store_li(APIView):
    def post(self,request):
        if request.data.get("search_text"):
            search = request.data.get("search_text")
            stall = medstore.objects.filter()

            search_list = jieba.lcut(search)

            x = request.data.get('x')
            y = request.data.get('y')

            stlist = []
            stlist0 = []
            stlist1 = []
            stlist2 = []
            stlist3 = []
            stlist4 = []

            for store in stall:
                key = 'TB6BZ-IDFLS-HHPOM-6OM6K-UQ245-S5BF2'
                api_url = 'https://apis.map.qq.com/ws/direction/v1/bicycling/?from=' + store.address + '&to=' + str(
                    x) + ',' + str(y) + '&key=' + key
                response = requests.get(api_url)
                way = json.loads(response.text)
                dis = way["result"]["routes"][0]["distance"]
                if dis <= 5000 :
                    st_det = {
                        'store':{
                            'name': store.name,
                            'desc': store.desc,
                            'code': store.ypjyxkzcode,
                            'dis': dis,
                        },
                        'store_med':[]
                    }

                    store_med = Medicine.objects.filter(drugstore=store.id)
                    for med in store_med:
                        med_detail = model_to_dict(med)
                        st_det['store_med'].append(med_detail)
                    tag0 = 0
                    tag1 = 0
                    tag = 0
                    order_str = str(st_det)
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
                    context = {
                        'id': store.id,
                        'name': store.name,
                        'code': store.ypjyxkzcode,
                        'dis': dis,
                        'tag': tag,
                    }
                    stlist.append(context)
            stlist.sort(key=get_tag, reverse=True)

            for a in stlist:
                if a['dis'] <= 500:
                    stlist0.append(a)
                if a['dis'] <= 1000:
                    stlist1.append(a)
                if a['dis'] <= 1500:
                    stlist2.append(a)
                if a['dis'] <= 2000:
                    stlist3.append(a)
                if a['dis'] <= 2500:
                    stlist4.append(a)
            return Response({"stlist": stlist,
                             "stlist0": stlist0,
                             "stlist1": stlist1,
                             "stlist2": stlist2,
                             "stlist3": stlist3,
                             "stlist4": stlist4,
                             })
        else:
            stall = medstore.objects.filter()
            x = request.data.get('x')
            y = request.data.get('y')

            stlist = []
            stlist0 = []
            stlist1 = []
            stlist2 = []
            stlist3 = []
            stlist4 = []

            for store in stall:
                key = 'TB6BZ-IDFLS-HHPOM-6OM6K-UQ245-S5BF2'
                api_url = 'https://apis.map.qq.com/ws/direction/v1/bicycling/?from=' + store.address + '&to=' + str(x) + ',' + str(y) + '&key=' + key
                response = requests.get(api_url)
                way = json.loads(response.text)
                print(way)
                dis = way["result"]["routes"][0]["distance"]
                context = {
                    'id': store.id,
                    'name': store.name,
                    'code': store.ypjyxkzcode,
                    'dis': dis,
                }
                if dis <= 3000:
                    stlist.append(context)
            for a in stlist:
                if a['dis'] <= 500:
                    stlist0.append(a)
                if a['dis'] <= 1000:
                    stlist1.append(a)
                if a['dis'] <= 1500:
                    stlist2.append(a)
                if a['dis'] <= 2000:
                    stlist3.append(a)
                if a['dis'] <= 2500:
                    stlist4.append(a)
            return Response({"stlist": stlist,
                             "stlist0": stlist0,
                             "stlist1": stlist1,
                             "stlist2": stlist2,
                             "stlist3": stlist3,
                             "stlist4": stlist4,
                             })

class store_det(APIView):
    def post(self,request):
        if request.data.get("search_text"):
            search = request.data.get("search_text")
            id = request.data.get('id')
            store = medstore.objects.get(id=id)
            medall = Medicine.objects.filter(drugstore=id)

            search_list = jieba.lcut(search)

            medlist = []

            for med in medall:
                med_detail =model_to_dict(med)
                tag0 = 0
                tag1 = 0
                tag = 0
                order_str = str(med_detail)
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
                context = {
                    'id': med.id,
                    'name': med.name,
                    'price': med.price,
                    'stock': med.stock,
                    'sales': med.sales,
                    'tag':tag,
                }
                medlist.append(context)
            medlist.sort(key=get_tag, reverse=True)

            return Response({"medlist": medlist,
                             "name": store.name,
                             })
        else:
            id = request.data.get('id')
            store = medstore.objects.get(id=id)
            medall = Medicine.objects.filter(drugstore=id)

            medlist = []
            medlist0 = []

            for med in medall:
                context = {
                    'id': med.id,
                    'name': med.name,
                    'price': med.price,
                    'stock': med.stock,
                    'sales': med.sales,
                    'tag':med.sales,
                }
                medlist0.append(context)
            medlist0.sort(key=get_tag, reverse=True)
            medlist = medlist0[0:5]
            return Response({"medlist": medlist,
                             "medlist0": medlist0,
                             "name": store.name,
                             })