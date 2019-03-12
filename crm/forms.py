#!/usr/bin/python3
# coding: utf-8
# @File: forms.py
# @Author:lcfzh
# @Time: 2019年03月12日 21:09
# 说明:

from django import forms
from crm import models
from django.core.exceptions import ValidationError
import hashlib


# 注册的form
class RegForm(forms.ModelForm):
    
    class Meta:
        #  元类
        model = models.UserProfile  # 指定model
        fields = '__all__'