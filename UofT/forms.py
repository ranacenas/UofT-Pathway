from django import forms
from django.conf import settings
import requests
from decouple import config

API_KEY = config("API_KEY")
class CourseForm(forms.Form):
    course = forms.CharField(max_length=10)

    def catch_rel(self):
      Codes = ['H1', 'H3', 'H5', 'Y']
      catch = []
      for course in self:
          for code in Codes:
            if code in course:
              catch.append(course)
            else:
              pass
      return catch



    

    def check(self):
      L1_pre = self.replace("/", " ").split()
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
      L1_pre = strip_charac
      Session = ['S', 'F', 'F2']
      for i in Session:
        if i in L1_pre[:-1]:
          [x[:-1] for x in L1_pre]
        else:
          continue
      return L1_pre
    
    def second_search(self):
      
      url = """https://cobalt.qas.im/api/1.0/courses/filter?q=term:"{term}"%20AND%20code:"{code}"%20&key={key}"""
      urlfinal = url.format(code= self, term = 2018, key = API_KEY)
      response = requests.get(urlfinal)
      result_preq = response.json()
      if len(result_preq) == 0:
        result_preq = "none"
        
      else:
        result_preq = result_preq[0]
      return result_preq
    
    def PRQ(self):
      if self != 'none':
        PRE = self["prerequisites"]
      else:
        PRE = 'none'
      return PRE


    def search(self):
      course = self.cleaned_data['course']
      url = """https://cobalt.qas.im/api/1.0/courses/filter?q=term:"{term}"%20AND%20code:"{code}"%20&key={key}"""
      urlfinal = url.format(code= course, term = 2018, key = API_KEY)
      response = requests.get(urlfinal)
      result = response.json()

#       NO PREREQUISITE / ERROR 
      if len(result) == 0:
              Level_one = "sorry, try again"
              pass

#       A LEVEL PREREQUISITE
      else:
          Level_one = result[0]
          
      return Level_one


class AutoTree(dict):

  def __missing__(self, key):
    value = self[key] = type(self)()
    return value

class Loop(dict):

  def Loop(self, list):
    master_list = []
    for i in list:
      S2 = CourseForm.second_search(i)
      S2 = S2["prerequisites"]
      S2 = CourseForm.check(S2)
      master_list.append(S2)
    return master_list
  
  def dict(self, one, two):
    dictionary = dict(zip(one, two))
    return dictionary

