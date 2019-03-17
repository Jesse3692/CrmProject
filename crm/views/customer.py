#!/usr/bin/python3
# coding: utf-8
# @File: customer.py
# @Author:lcfzh
# @Time: 2019年03月17日 13:43
# 说明:
from django.shortcuts import render
from crm import models
from utils.pagination import Pagination

# 以列表形式展示客户信息
def customer_list(request):
    customer_obj = models.Customer.objects.all()
    return render(request, 'customer_list.html', {'all_customer': customer_obj})


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