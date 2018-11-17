from django.shortcuts import render
from .forms import AutoTree, CourseForm
from UofT.models import Course
from decouple import config
import psycopg2
# Create your views here.

def index(request):
    
    nest = AutoTree()
    if 'course' in request.GET:
        A = CourseForm(request.GET)
        nest = {}
        if A.is_valid():
            Initial_search = A.search()
            result = CourseForm.c(Initial_search)
        else:
            result = CourseForm()  
              
    else:
        A = CourseForm()
        result = CourseForm()
    

    return render(request, 'UofT/UofTpreReq.html', {"A": A, "nest": result})
    
    





    