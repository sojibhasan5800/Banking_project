from django.shortcuts import render,redirect
from django.views.generic import FormView
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import UpdateView

from django.urls import reverse_lazy
from .forms import UserRegistrationForm,UserUpdateForm
from django.views import View




# Create your views here.

class UserRegistrationView(FormView):
    template_name='accounts_html/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request,user)
        print(user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name='accounts_html/login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    

class UserLogoutView(LogoutView):
    
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')



class UserBankAccountUpdateView(View):
    template_name = 'accounts_html/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
    
    
    
    
        

    
    
