from django.shortcuts import render

def create(request):
    return render(request, 'www/create.html')
