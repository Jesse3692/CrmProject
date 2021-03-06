#!/usr/bin/python3
# coding: utf-8
# @File: customer.py
# @Author:lcfzh
# @Time: 2019年03月17日 13:43
# 说明:
from django.db.models import Q
from django.http.request import QueryDict
from django.shortcuts import HttpResponse, redirect, render, reverse
from django.views import View

from crm import models
from crm.forms import CustomerForm
from utils.pagination import Pagination


# 以列表形式展示客户信息
def customer_list(request):
    if request.path_info == reverse('customer_list'):  # 如果是请求的所有的客户信息，给所有的
        all_customer = models.Customer.objects.filter(
            consultant__isnull=True)  # 销售为空
    else:
        all_customer = models.Customer.objects.filter(
            consultant=request.user_obj)  # 已登录的用户对象
    page = Pagination(
        request.GET.get('page', 1),
        all_customer.count(),
    )
    return render(
        request,
        'customer_list.html',
        {
            'all_customer': all_customer[page.start:page.end],
            'page_html': page.page_html,  # 分页的页面
        })


# 以CBV的方式显示客户列表
class CustomerList(View):
    def get(self, request, *args, **kwargs):
        q = self.search(['qq', 'name', 'sex'])
        if request.path_info == reverse('customer_list'):
            all_customer = models.Customer.objects.filter(q, consultant__isnull=True)  # 销售为空
        else:
            all_customer = models.Customer.objects.filter(q, consultant=request.user_obj)  # 已登录的用户对象
        page = Pagination(
            request.GET.get('page', 1),
            all_customer.count(),
            request.GET.copy(),
        )
        return render(
            request,
            'customer_list.html',
            {
                'all_customer': all_customer[page.start:page.end],
                'page_html': page.page_html,  # 分页的页面
            })

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')  # multi_pub multi_apply
        # 用反射判断是否有相应的操作
        if hasattr(self, action):
            # 如果有获取并执行
            func = getattr(self, action)
            print(func)
            func()
        else:
            return HttpResponse('非法操作')
        return self.get(request, *args, **kwargs)

    def multi_apply(self, ):  # 公户转私户
        ids = self.request.POST.getlist('ids')
        # 方式一 查询的客户
        # models.Customer.objects.filter(pk__in=ids).update(consultant=self.request.user_obj)
        # models.Customer.objects.filter(pk__in=ids).update(consultant_id=self.request.session.get('pk'))
        # 方式二 查用户
        self.request.user_obj.customers.add(*models.Customer.objects.filter(
            pk__in=ids))

    def multi_pub(self):  # 私户转公户
        ids = self.request.POST.getlist('ids')  # 获取客户提交的ID
        # 方式一 查询的客户
        models.Customer.objects.filter(pk__in=ids).update(consultant=None)

        # 方式二 查用户
        # self.request.user_obj.customers.remove(*models.Customer.objects.filter(pk__in=ids))
    
    def search(self, field_list):
        query = self.request.GET.get('query', '')
        # Q(Q(qq__contains=query) | Q(name__contains=query)),
        q = Q()
        q.connector = 'OR'
        # q.children.append(Q(qq__contains=query))
        # q.children.append(Q(name__contains=query))
        
        for field in field_list:
            # q.children.append(Q(qq__contains=query))
            # 替换搜索的内容
            if field == 'sex':
                if query == '男':
                    sex = 'male'
                elif query == '女':
                    sex = 'female'
                else:
                    sex = ''
                q.children.append(Q(sex=sex))
            q.children.append(Q(('{}__contains'.format(field), query)))
        return q


# 添加修改用户
def customer_change(request, edit_id=None):
    obj = models.Customer.objects.filter(pk=edit_id).first()
    # 处理POST
    if request.method == 'POST':
        # 包含提交的数据 原始数据
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()  # 保存修改
            # 重定向到展示页面
            next = request.GET.get('next')
            print('next>>>>>', next)
            return redirect(next)
    else:
        # 包含原始数据的form表单
        form_obj = CustomerForm(instance=obj)
    title = '编辑客户' if edit_id else '添加客户'
    return render(request, 'customer_edit.html', {
        'form_obj': form_obj,
        'title': title
    })
