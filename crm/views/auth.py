#!/usr/bin/python3
# coding: utf-8
# @File: auth.py
# @Author:lcfzh
# @Time: 2019年03月17日 13:44
# 说明:
from django.shortcuts import HttpResponse,render,redirect,reverse
import hashlib
from crm import models
from crm.forms import RegForm

# 主页
def index(request):
    return render(request, 'index.html')


# 登陆页面
def login(request):
    # print(request.POST)
    if request.method == 'POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        
        # MD5加密（登陆时加密）
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        pwd = md5.hexdigest()
        
        obj = models.UserProfile.objects.filter(username=user, password=pwd, is_active=True).first()
        # print('>>>', obj)
        # print(user,pwd)
        if obj:
            # 登陆成功跳转到主页并保存当前用户的ID
            request.session['pk'] = obj.pk
            return redirect(reverse('index'))
        else:
            # 登录失败
            return render(request, 'login.html', {'login_error': '用户名或密码错误'})
    else:
        # GET方法则返回一个登陆页面
        return render(request, 'login.html')


# 注册页面
def register(request):
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        # print(form_obj)
        if form_obj.is_valid():
            form_obj.save()
            # print(form_obj.is_valid())
            return redirect(reverse('login'))
        # print(">>>>",form_obj.is_valid())
        return render(request, 'register.html', {'form_obj': form_obj})
    else:
        form_obj = RegForm()
    return render(request, 'register.html', {'form_obj': form_obj})
