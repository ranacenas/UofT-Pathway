from django.shortcuts import render
from .forms import CourseForm, AutoTree, Loop

# Create your views here.

def index(request):
    step_two = {}
    prereq_list = {}
    nest = AutoTree()
    loop = Loop()
    if 'course' in request.GET:
        form = CourseForm(request.GET)
        if form.is_valid():
            #SEARCHES THE COURSE CODE
            SEARCH_RESULT = form.search()
            if SEARCH_RESULT == 'sorry, try again':
                nest['code'] = 'Sorry try again, the course information cannot be found'
            
            else:

                recent =  SEARCH_RESULT['id']

                nest['id'] = recent

                

                #RETURNS RESULT AND TAKES ONLY THE CODE VALUE
                COURSE_CODE = SEARCH_RESULT['code']

                #TAKES THE PREREQUISITE OF THE RESULT
                PREREQUISITE_INITIAL = SEARCH_RESULT['prerequisites']
                nest['code'] = COURSE_CODE

                if len(PREREQUISITE_INITIAL) == 0:
                    nest['prerequisites']['prerequisites_zero'] = "Prerequisites were not found for this course"
                else:

                #STRIPS AND TURNS THE PREREQUISITES INTO A LIST
                    Prereq_list = CourseForm.check(PREREQUISITE_INITIAL)

                    #ADDS IT INTO THE DICTIONARY
                    
                    nest['prerequisites']['prerequisites_zero'] = PREREQUISITE_INITIAL
                    

                    #Campus codes filters
                    CAMPUS = ["H3", "H1", "H5", "Y1"]

                    #New list of course codes

                    P1 = CourseForm.catch_rel(Prereq_list)
                    nest['P1'] = P1

                    if len(P1) > 0:
                        P2_list = []
                        P2_all = []
                        
                        for course in P1:
                            P2_search = CourseForm.second_search(course)

                            P2_pre = CourseForm.PRQ(P2_search)
                            
                            if P2_pre == 'none':
                                pass
                            else:
                                P2_all.append(P2_pre)
                                
                                P2_check = CourseForm.check(P2_pre)
                                P2_list.append(P2_check)

                                P2_zip = dict(zip(P1, P2_list))
                                P2_all_zip = dict(zip(P1, P2_all))
                                
                                nest['P2_all'] = P2_all_zip
                                nest['P2_list'] = P2_list
                                nest['P2_zip_list'] = P2_zip
                                pass
                            pass
                            
                        P3_list = []
                        
                        #P3 = {}
                        for num in range(len(P2_list)):
                            P3_catch = CourseForm.catch_rel(P2_list[num])
                            
                            L = [x for x in P3_catch if CourseForm.PRQ(CourseForm.second_search(x)) != 'none']
                            P3_list.append(L)
                            nest['LLLLLLLLLLLLLLLLLL'] = P3_list
                            pass
                            
                                
                            
                            
                        


                        
                        P3_final = [[] for items in range(len(P3_list))]
                        for i in range(len(P3_list)):
                            
                            for q in P3_list[i]:
                                P3_search = CourseForm.second_search(q)
                                

                                
                                if P3_search != 'none':
                                    P3_Pre = P3_search["prerequisites"]
                                
                                    
                                    P3_final[i].append(P3_Pre)
                                    nest['PEEEEEEE'] = P3_final
                                    pass
                                

                        P3_dict = {}          
                        for i in range(len(P3_final)):
                            P3_dict.update(dict(zip(P3_list[i], P3_final[i])))
                            nest["P3_dict"] = P3_dict
                            continue
                        for j, k in P2_zip.items():
                            for i in k:
                                for l, p in P3_dict.items():
                                    if i in l:
                                        nest['TEST'][j][i] = p
                                    else:
                                        pass
                                     

                       




                
            



    else:
        form = CourseForm()
        preq = CourseForm()
    return render(request, 'UofT/UofTpreReq.html', {'form': form, 'nest':nest})

# def test(request):
#     if request.method == 'GET':step_three_
#         h = .get('get_get')
#         step = CourseForm.second_search(h)
#         return render(request,'uoftapp/UofTpreReq.html', {'ste': step} )




    