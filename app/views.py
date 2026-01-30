from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        "title":"home page",
    }
    return render(request,"app/index.html",context)

