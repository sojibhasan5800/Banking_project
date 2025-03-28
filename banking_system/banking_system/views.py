from django.shortcuts import render,redirect


def homepage(request):
    return render(request,'main_temp/base.html')