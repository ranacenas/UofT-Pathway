from django import forms
from django.conf import settings
import requests
from decouple import config

#API Key
API_KEY = config("API_KEY")

class CourseForm(forms.Form):
    course = forms.CharField(max_length=10)

    def catch_rel(self):
      """type(self) = list
      
      returns a list with strings containing the Codes. 
      This function is usually used after the check function 
      (see below)
      
      catch_rel(['Completion', 'of', 'BIO325H1F']
      => ['BIO325H1F'] """
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
      """type(self) = list
      generates a new list
      
      check(['MATA36H3F and BIOA01H3F', 'Completion of CSC411H1F/CSC404H1F'])
      => ['MATA36H3', 'BIOA01H3', 'CSC411H1', 'CSC404H1F']"""
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
      strip_charac = [s.strip("(70%") for s in strip_charac]

      L1_pre = strip_charac
      Session = ['S', 'F', 'F2']
      for i in Session:
        if i in L1_pre[:-1]:
          [x[:-1] for x in L1_pre]
        else:
          continue
      return L1_pre
    
    def second_search(self):
      """type(self) = string 
      returns a dictionary
      
      searches the course code and returns a dictionary"""
      
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
      """type(self) = dictionary

      PRQ(dict):
      returns string

      This function is used after the catch_rel function

      If the dictionary is not empty (meaning the course code exists)
      it takes the prerequisites information from that dictionary and returns a string."""
      if self != 'none':
        PRE = self["prerequisites"]
      else:
        PRE = 'none'
      return PRE


    def search(self):
      """User inputs a course code and returns a dictionary"""
      course = self.cleaned_data['course']
      url = """https://cobalt.qas.im/api/1.0/courses/filter?q=term:"{term}"%20AND%20code:"{code}"%20&key={key}"""
      urlfinal = url.format(code= course, term = 2018, key = API_KEY)
      response = requests.get(urlfinal) 
      result = response.json() #returns a dictionary IN a list
      if len(result) == 0:
        Level_one = "sorry, try again"
        pass

      else:
          Level_one = result[0]  
      return Level_one


class AutoTree(dict):
  #This helps make nested dictionaries.
  def __missing__(self, key):
    value = self[key] = type(self)()
    return value


