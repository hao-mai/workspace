from django.shortcuts import render

def home(request):
    return render(request, 'virtual_library/home.html')

def libraryhomepage(request):
    return render(request, 'virtual_library/libraryhome.html')

def resume(request):
    return render(request, 'virtual_library/resume.html')
