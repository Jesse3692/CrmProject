#!/usr/bin/python3
# coding: utf-8
# @File: consult.py
# @Author:lcfzh
# @Time: 2019年03月19日 01:32
# 说明:

from django.db.models import Q
from django.http.request import QueryDict
from django.shortcuts import HttpResponse, redirect, render, reverse
from django.views import View

from crm import models
from crm.forms import ConsultForm
from utils.pagination import Pagination

class ConsultList(View):
    """
    
    """
    def get(self, request, *args, **kwargs):
        q = self.search([])
        
        all_consult = models.ConsultRecord.objects.filter(q, consultant=request.user_obj, delete_status=False)
        page = Pagination(
            request.GET.get('page', 1),
            all_consult.count(),
            request.GET.copy(),
        )
        return render(
            request,
            'consult_list.html',
            {
                'all_consult': all_consult[page.start:page.end],
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
    

# 添加跟进
def consult_add(request):
    form_obj = ConsultForm()
    return render(request, 'consult_add.html', {'form_obj':form_obj})
