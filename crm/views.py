from django.shortcuts import render,HttpResponse

# Create your views here.

# 主页
def index(request):
    return HttpResponse('这是主页')

# 登陆页面
def login(request):
    print(request.POST)
    if request.method == 'POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        print(user,pwd)
        return render(request,'login.html',{'login_error':'用户名或密码错误'})
    
# 注册页面
def register(request):
    return render(request, 'register.html')