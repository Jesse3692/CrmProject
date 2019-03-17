# 1 登陆注册功能
# 2 显示客户列表

## 2.1 前置配置

### 2.1.1 超级管理员和models类的注册

```python
# 1 创建超级管理员账号
python manage.py createsuperuser  # 账号默认为当前计算机用户，邮箱可为空，密码最少8位必须包含字母和数字

# 2 在后台管理中注册客户类 \crm\admin.py
from django.contrib import admin
from crm import models
# Register your models here.
admin.site.register(models.Customer)
```



### 2.1.2 配置对象显示相应内容

1. models类在后台管理注册好，页面不显示客户信息，显示的是客户对象

![AkMcJe.png](https://s2.ax1x.com/2019/03/13/AkMcJe.png)

2. 在models的客户类下面，添加魔法函数str，可以随意配置显示内容

   ```python
   from django.db import models
   from multiselectfield import MultiSelectField
   class Customer(models.Model):
       """
       客户表....
       """
       
       # 将客户对象显示为对应内容
       def __str__(self):
           return "{}-{}".format(self.name,self.qq)
   ```

   ![AkQatS.png](https://s2.ax1x.com/2019/03/13/AkQatS.png)

### 2.1.3 配置后台管理页面显示中文

1. 后台管理页面默认显示英文，但是可以进行本地化设置

   ![AkQrXn.png](https://s2.ax1x.com/2019/03/13/AkQrXn.png)

2. 设置Django本地化为中文

   ```python
   # 在settings.py文件中配置
   LANGUAGE_CODE = 'zh-hans'
   ```

   ![AkQWhF.png](https://s2.ax1x.com/2019/03/13/AkQWhF.png)

### 2.1.4 配置Django为本地时间

修改settings.py的配置项如下

```python
TIME_ZONE = 'Asia/Shanghai'
USE_TZ = False
```



### 2.1.5 数据库字段为空时，设置页面填写字段可为空

数据库中字段没有设置非空约束，但是页面却要求填写内容，此时可以在models文件的对应字段配置以下内容

```python
class Customer(models.Model):
    """
    客户表...
    """
	class_list = models.ManyToManyField('ClassList', verbose_name="已报班级", blank=True)
```



​	![AkQLtO.png](https://s2.ax1x.com/2019/03/13/AkQLtO.png)

2.1.6 使用mark_safe方式在网页显示响应代码



## 2.2 在页面展示客户信息



# 3 分页功能

分页的本质就是对所有数据的一个切片操作，根据请求的不同显示不同的数据

