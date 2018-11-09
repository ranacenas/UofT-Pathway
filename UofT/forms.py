from django import forms
from django.conf import settings
import requests
from decouple import config
#

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
      urlfinal = url.format(code= self, term = 2018, key = config('key'))
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
      urlfinal = url.format(code= course, term = 2018, key = config('key'))
      response = requests.get(urlfinal)
      result = response.json()

#       NO PREREQUISITE / ERROR 
      if len(result) == 0:
              Level_one = "sorry, try again"
              pass

#       A LEVEL PREREQUISITE
      else:
          Level_one = result[0]
          # Level_one_course = Level_one['code']
          # L1_prereq = Level_one["prerequisites"] #returns prerequisite of a course
          

          # if len(L1_prereq) == 0:
          #   L1_prereq = "No Prerequisites for this course"
          
          # # if "Any" or "Credits" or "Grade" in L1_prereq:
          # #   L1_prereq = "L1_prere222q"

          # else:
          #   L1_prereq_stage_2 = CourseForm.check(L1_prereq)
          #   Level_One_Req = []
            
          #   for i in L1_prereq_stage_2:
          #     urlsec = url.format(code=i)
          #     Level_One_Req.append(urlsec)
          #     Level_one_Res = []
          #     for req in Level_One_Req:
          #       resp = requests.get(req)
          #       result_sec = resp.json()
          #       secondary = result_sec[0]
          #       secondary = secondary["prerequisites"]
          #       Level_one_Res.append(secondary)


                       

            # if "or" in L1_prereq_step_two:
            #   ONLY_OR = [crs_code for crs_code in L1_prereq_step_two if crs_code != "or"]
            #   Level_one_requests = []
         
            #   for i in ONLY_OR:
            #     urlsec = url.format(code= i)
            #     Level_one_requests.append(urlsec)
            #     # Level_one_pre = []
            #     # for req in Level_one_requests:
            #     #   resp2 = requests.get(req)
            #     #   result_sec = resp2.json()
            #     #   ffinal_sec = result_sec[0]
            #     #   tes = ffinal_sec["code"]
            #     #   final_sec = ffinal_sec["prerequisites"]
            #     #   Level_one_pre.append(final_sec)
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

