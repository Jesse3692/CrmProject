import hashlib
from django.shortcuts import render,HttpResponse,redirect,reverse
from crm import models
from crm.forms import RegForm

# Create your views here.

# 主页
def index(request):
    return HttpResponse('这是主页')

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
        
        obj = models.UserProfile.objects.filter(username=user,password=pwd,is_active=True).first()
        # print('>>>', obj)
        # print(user,pwd)
        if obj:
            # 登陆成功跳转到主页
            return redirect(reverse('index'))
        else:
            # 登录失败
            return render(request,'login.html',{'login_error':'用户名或密码错误'})
    else:
        # GET方法则返回一个登陆页面
        return render(request,'login.html')
    
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
        return render(request, 'register.html', {'form_obj':form_obj})
    else:
        form_obj = RegForm()
    return render(request, 'register.html', {'form_obj':form_obj})

# 以列表形式展示客户信息
def customer_list(request):
    customer_obj = models.Customer.objects.all()
    return render(request, 'customer_list.html',{'all_customer':customer_obj})

# 模拟大量用户
users = [{'username':'zhang{}'.format(i),'password':'123'} for i in range(1,202)]
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
    # 从网页获取的页码（加判断）
    try:
        # 如果没有页数值传过来
        page_num = int(request.GET.get('page',1))
        if page_num <= 0:
            page_num = 1
    except ValueError as e:
        page_num = 1
    print(">>>", page_num)
    # 每页显示的数量
    per_num = 10
    
    # 总数据量
    all_count = len(users)
    
    # 总页数
    page_count, more = divmod(all_count, per_num)
    if more:
        page_count += 1
    
    # 最大显示页数（显示多少个分页按钮）
    max_show = 11
    half_show = max_show // 2
    
    #          对页码显示的逻辑判断
    if page_count < max_show:  # 总页码数 < 最大显示页码数
        page_start = 1  # 起始页数
        page_end = page_count  # 结束页数
    else:  # 总页码数 > 最大显示页码数    -- 一般情况下
        if page_num <= half_show:  # 请求的页码小于中间值时（左边极值）
            page_start = 1
            page_end = max_show
        elif page_num + half_show >= page_count:  # 请求的页码加上中间值大于总页数时 （右边极值）
            page_start = page_count - max_show + 1
            page_end = page_count
        else:
            page_start = page_num - half_show
            page_end = page_num + half_show
        
        # 在后端直接处理前端的HTML代码，然后发送过去
        
        # 添加上一页
        page_list = []
        if page_num == 1:  # 如果是第一页则上一页没法使用
            page_list.append('<li class="disabled"><a>上一页</a></li>')
        else:
            page_list.append('<li><a href="?page={}">上一页</a></li>'.format(page_num - 1 ,))
        
        # 添加分页按钮
        for i in range(page_start, page_end + 1):
            if i == page_num:  # 当前标签高亮
                page_list.append('<li class="active"><a href="?page={}">{}</a></li>'.format(i,i))
            else:
                page_list.append('<li><a href="?page={}">{}</a></li>'.format(i,i))
        
        # 添加下一页按钮
        if page_num == page_count:  # 如果是最后一页则下一页没法使用
            page_list.append('<li class="disabled"><a>下一页</a></li>')
        else:
            page_list.append('<li><a href="?page={}">下一页</a></li>'.format(page_num + 1, ))
        
        # 对列表中的标签拼接成字符串
        page_html = ''.join(page_list)
    
        return render(request, 'user_list.html',{'all_users':users[page_start:page_end], 'page_html':page_html})