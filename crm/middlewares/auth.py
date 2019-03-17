#!/usr/bin/python3
# coding: utf-8
# @File: auth.py
# @Author:lcfzh
# @Time: 2019年03月17日 16:02
# 说明:

from django.shortcuts import reverse,redirect
from crm import models
from django.utils.deprecation import MiddlewareMixin

class AuthMiddleware(MiddlewareMixin):
    # 对要进来的请求进行验证
    def process_request(self,request):
        # 白名单 登陆和注册
        if request.path_info in [reverse('login'), reverse('register')]:
            return
        # 白名单 后台管理
        if request.path_info.startswith('/admin/'):
            return
        pk = request.session.get('pk')
        user = models.UserProfile.objects.filter(pk=pk).first()
        # 如果没有登陆，则跳转到登陆页面
        if not user:
            return redirect(reverse('login'))
        
        request.user_obj = user
        