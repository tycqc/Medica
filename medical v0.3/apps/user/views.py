from django.shortcuts import render
from user.models import User
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import re, random, uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection

from user import models
from user.serializer.account import MessageSerializer, LoginSerializer


class MessageView(APIView):
    def get(self, request, *args, **kwargs):
        """
        发送手机短信验证码
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 1.获取手机号
        # 2.手机格式校验
        ser = MessageSerializer(data=request.query_params)
        if not ser.is_valid():
            return Response({'status': False, 'message': '手机格式错误'})
        phone = ser.validated_data.get('phone')

        # 3.生成随机验证码
        random_code = random.randint(1000, 9999)
        # 5.把验证码+手机号保留（30s过期）
        """
        result = send_message(phone,random_code)
        if not result:
            return Response({"status": False, 'message': '短信发送失败'})
        """
        #省略发送验证码到手机环节
        print(random_code)

        #连接redis，用于缓存
        conn = get_redis_connection()
        conn.set(phone, random_code, ex=60)

        return Response({"status": True, 'message': '发送成功'})


class LoginView(APIView):

    def post(self, request, *args, **kwargs):

        # 1. 校验手机号是否合法
        # 2. 校验验证码，数据库
        #     - 无验证码
        #     - 有验证码，输入错误
        #     - 有验证码，成功
        #
        # 4. 将一些信息返回给小程序

        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"status": False, 'message': '验证码错误'})

        # 3. 去数据库中获取用户信息（获取/创建）
        phone = ser.validated_data.get('phone')
        user_object, flag = models.User.objects.get_or_create(phone=phone)
        user_object.token = str(uuid.uuid4())
        user_object.save()

        return Response({"status": True, "data": {"token": user_object.token, 'phone': phone}})


























