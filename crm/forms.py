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
    # 重写字段信息
    password = forms.CharField(widget=forms.PasswordInput, label='密码', min_length=6)
    re_password = forms.CharField(widget=forms.PasswordInput, label='确认密码', min_length=6)
    
    class Meta:
        #  元类
        model = models.UserProfile  # 指定model
        fields = '__all__'
        exclude = ['is_active']
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
        super(RegForm, self).__init__(*args, **kwargs)
        # 自定义操作
        for filed in self.fields.values():
            filed.widget.attrs.update({'class':'form-control'})
            print('>>>>', filed)  # <django.forms.fields.CharField object at 0x000002BDC81B6828>
        print(self.fields.values()) # odict_values([<django.forms.fields.EmailField object at 0x000002BDC81B6630>, <django.forms.fields.CharField object at 0x000002BDC81B66D8>, <django.forms.fields.CharField object at 0x000002BDC81B6748>, <django.forms.models.ModelChoiceField object at 0x000002BDC81B67B8>, <django.forms.fields.CharField object at 0x000002BDC81B6828>, <django.forms.fields.CharField object at 0x000002BDC81B6978>, <django.forms.fields.CharField object at 0x000002BDC81B69E8>])
            # 设置标签的属性信息
            # filed.widget.attrs['class'] = 'form-control'
            
    def clean(self):
        pwd = self.cleaned_data.get('password', '')
        re_pwd = self.cleaned_data.get('re_password', '')
        print('>>>', self.cleaned_data)
        if pwd == re_pwd:
            return self.cleaned_data
        
        # 两次密码不一致
        self.add_error('re_password','两次密码不一致！！')
        raise ValidationError('两次密码不一致')
    
        