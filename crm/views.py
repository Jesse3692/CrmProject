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
    
    # 起始页数
    start_page = (page_num - 1)*per_num
    # 结束页数
    end_page = page_num*per_num
    return render(request, 'user_list.html',{'all_users':users[start_page:end_page], 'page_count':range(page_num,page_count + 1)})