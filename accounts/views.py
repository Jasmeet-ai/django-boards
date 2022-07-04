from myproject import settings
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from django.views.generic import View
from .forms import SignUpForm
# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form':form})

# def LogInView(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'accounts/login.html',{'form':form})

# class LogoutView(View):
#      def get(self, request):
#         logout(request)
#         return redirect(settings.LOGIN_REDIRECT_URL)

# class LogInView(View):
#      def post(self, request):
#         username = request.POST['username']
#         password = request.POST['password']
       

      
#         return render(request,'accounts/login.html')