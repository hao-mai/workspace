from django.shortcuts import render

def homepage(request):
    return render(request, 'virtual_library/homepage.html')

def libraryhomepage(request):
    return render(request, 'virtual_library/libraryhome.html')