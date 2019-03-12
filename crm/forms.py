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
    re_password = forms.CharField(widget=forms.PasswordInput, label='确认密码', min_length=6)
    
    class Meta:
        #  元类
        model = models.UserProfile  # 指定model
        fields = '__all__'
        labels = {
            'username': '用户名'
        }
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control', 'placeholder':'用户名'}),
        }
        error_messages = {
            'min_length':'不能少于6位'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自定义操作
        for filed in self.fields.values():
            filed.widget.attrs.update({'class':'form-control'})
            
    # def clean(self):
    
        