import re
import random
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection

from user import models
from user.serializer.account import MessageSerializer, LoginSerializer


class MessageView(APIView):
    def get(self, request, *args, **kwargs):

        #发送手机短信验证码

        # 1.获取手机号
        # 2.手机格式校验
        ser = MessageSerializer(data=request.query_params)
        if not ser.is_valid():
            return Response({'status': False, 'message': '手机格式错误'})
        phone = ser.validated_data.get('phone')

        # 3.生成随机验证码
        random_code = random.randint(1000, 9999)
        # 5.把验证码+手机号保留 存入缓存
        # 省略调用第三方api发送短信过程
        print(random_code)


        # 搭建redis服务器
        # django中方便使用redis的模块 django-redis
        conn = get_redis_connection()
        conn.set(phone, random_code, ex=300) #有效期300s

        return Response({"status": True, 'message': '发送成功'})


class LoginView(APIView):

    def post(self, request, *args, **kwargs):

        # 1. 校验手机号是否合法
        # 2. 校验验证码

        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"status": False, 'message': '验证码错误'})

        # 3. 去数据库中获取用户信息（获取/创建）
        phone = ser.validated_data.get('phone')
        user_object, flag = models.User.objects.get_or_create(phone=phone)
        user_object.token = str(uuid.uuid4())
        user_object.save()

        return Response({"status": True, "data": {"token": user_object.token, 'phone': phone}})

class EditView(APIView):

    def post(self, request):
        token = request.data.get('token')
        name = request.data.get('name')
        addr = request.data.get('addr')
        desc = request.data.get('desc')
        user_object= models.User.objects.get(token=token)
        user_object.name=name
        user_object.addr=addr
        user_object.desc=desc
        user_object.save()

        return Response({"status": True})
























