#!/usr/bin/python3
# coding: utf-8
# @File: customer.py
# @Author:lcfzh
# @Time: 2019年03月17日 13:43
# 说明:
from django.shortcuts import render,redirect,reverse,HttpResponse
from crm import models
from utils.pagination import Pagination
from crm.forms import CustomerForm

# 以列表形式展示客户信息
def customer_list(request):
    customer_obj = models.Customer.objects.all()
    return render(request, 'customer_list.html', {'all_customer': customer_obj})

# 展示私户
def my_customer(request):
    
    return HttpResponse('ojbk')

# 添加客户
def customer_add(request):
    form_obj = CustomerForm() # 不包含数据的form
    if request.method == 'POST':
        # 包含用户提交数据的form
        form_obj = CustomerForm(request.POST)
        # 对数据进行校验
        if form_obj.is_valid():
            form_obj.save()  # 创建对象
            # 跳转到展示页面
            return  redirect(reverse('customer_list'))
    return render(request, 'customer_add.html', {'form_obj':form_obj})

# 编辑客户
def customer_edit(request, edit_id):
    obj = models.Customer.objects.filter(pk=edit_id).first()
    # 处理POST
    if request.method == 'POST':
        # 包含提交的数据 原始数据
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()  # 保存修改
            # 重定向到展示页面
            return redirect(reverse('customer_list'))
    else:
        # 包含原始数据的form表单
        form_obj = CustomerForm(instance=obj)
    return render(request, 'customer_edit.html', {'form_obj': form_obj})


# 模拟大量用户
users = [{'username': 'zhang{}'.format(i), 'password': '123'} for i in range(1, 202)]


# 分页功能简单
def user_list(request):
    """
    一页显示20

    第1页  0      20
    第2页  20     40

      n   (n-1)*20   20*n
    :param request:
    :return:
    """
    
    page = Pagination(request.GET.get('page', '1'), len(users))
    
    return render(request, 'user_list.html', {'all_users': users[page.start:page.end], 'page_html': page.page_html})