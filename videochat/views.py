from django.shortcuts import render

# Create your views here.

def html_view(request):
    context ={}

    return render(request,'main.html',context=context)