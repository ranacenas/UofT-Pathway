from django import forms
from django.conf import settings
import requests
from decouple import config
import psycopg2
#from config1 import config2
from .models import Course
import os
import string 
from django.core.validators import MinLengthValidator

#API Key
API_KEY = config("API_KEY")

class CourseForm(forms.Form):
    course = forms.CharField(max_length=8, validators=[MinLengthValidator(8)])
    

    #params = config2()
    def search(self):
      """User inputs a course code and returns a dictionary"""
      course = self.cleaned_data['course']
      
      return course

    def c(self):
      #for local dev
      # db1 = config('NAME')
      # user = config('USER')
      # pw = config('PASSWORD')
      # host = config('HOST')
      # port = config('PORT')
      # conn = psycopg2.connect(dbname = db1, user = user, password = pw, host = host, port=port)

      #heroku dev
      DATABASE_URL = os.environ['DATABASE_URL']
      conn = psycopg2.connect(DATABASE_URL, sslmode='require')

      cur = conn.cursor()
      sql = """SELECT info from prereqjson where info ->> 'code' ilike '{code}'"""
      new = sql.format(code=self)
      cur.execute(new)
      y = (cur.fetchone())
      cur.close()
      
      #you = [list(i) for i in y]
      return y
      


    

    def catch_rel(self):
      """type(self) = list
      
      returns a list with strings containing the Codes. 
      This function is usually used after the check function 
      (see below)
      
      catch_rel(['Completion', 'of', 'BIO325H1F']
      => ['BIO325H1F'] """
      Codes = ['H1', 'H3', 'H5', 'Y']
      
      catch = [course for code in Codes for course in self if code in course]
      return catch



    
    def check(self):
      """type(self) = str
      generates a new list
      
      check(['MATA36H3F and BIOA01H3F', 'Completion of CSC411H1F/CSC404H1F'])
      => ['MATA36H3', 'BIOA01H3', 'CSC411H1', 'CSC404H1F']"""
      
      L1_pre = self.replace("/", " ").split()
      # stripchars = ['[](),;']
      # for c in stripchars:
      #   s = L1_pre.replace(c, " ")
      strip_and = [code for code in L1_pre if code != "and"]
      strip_or = [code for code in strip_and if code != "or"]
      strip_charac = [s.strip("[") for s in strip_or]
      strip_charac = [s.strip("]") for s in strip_charac]
      strip_charac = [s.strip(")") for s in strip_charac]
      strip_charac = [s.strip("(") for s in strip_charac]
      strip_charac = [s.strip("/") for s in strip_charac]
      strip_charac = [s.strip("/(") for s in strip_charac]
      strip_charac = [s.strip(")/") for s in strip_charac]
      strip_charac = [s.strip(",") for s in strip_charac]
      strip_charac = [s.strip(";") for s in strip_charac]
      strip_charac = [s.strip("(70%") for s in strip_charac]
      

      L1_pre = strip_charac
      
      return L1_pre
 
    
   

    


class AutoTree(dict):
  #This helps make nested dictionaries.
  def __missing__(self, key):
    value = self[key] = type(self)()
    return value


