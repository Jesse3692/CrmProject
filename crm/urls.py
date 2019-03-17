"""CrmProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from crm.views import auth,customer

urlpatterns = [
    url(r'^login/', auth.login, name='login'),
    url(r'^register/', auth.register, name='register'),
    url(r'^index/', auth.index, name='index'),
    # 展示公户
    url(r'^customer_list/', customer.customer_list, name='customer_list'),
    # 展示私户
    url(r'^my_customer/', customer.my_customer, name='my_customer'),
    
    # # 添加客户
    # url(r'^customer_add/', customer.customer_add, name='customer_add'),
    # # 编辑客户
    # url(r'^customer_edit/(\d+)/', customer.customer_edit, name='customer_edit'),
    
    # 添加客户
    url(r'^customer_add/',customer.customer_change, name='customer_add'),
    # 修改客户
    url(r'customer_edit/(\d+)', customer.customer_change, name='customer_edit')
]
