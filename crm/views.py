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
        print(form_obj)
        if form_obj.is_valid():
            form_obj.save()
            print(form_obj.is_valid())
        print(">>>>",form_obj.is_valid())
        return render(request, 'register.html')
    else:
        form_obj = RegForm()
        return render(request, 'register.html', {'form_obj':form_obj})