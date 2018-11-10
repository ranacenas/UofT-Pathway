from django.shortcuts import render
from .forms import CourseForm, AutoTree

# Create your views here.

def index(request):
    
    nest = AutoTree()
    if 'course' in request.GET:
        form = CourseForm(request.GET)
        if form.is_valid():
            SEARCH_RESULT = form.search() #SEARCHES THE COURSE CODE
            if SEARCH_RESULT == 'sorry, try again':  #if course code does not exist
                nest['code'] = 'Sorry try again, the course information cannot be found'
            
            else:
                recent =  SEARCH_RESULT['id'] 
                nest['id'] = recent

                
                COURSE_CODE = SEARCH_RESULT['code'] #TAKES ONLY THE CODE VALUE from dict
                nest['code'] = COURSE_CODE #adds it into the dictionary 
                PREREQUISITE_INITIAL = SEARCH_RESULT['prerequisites'] #TAKES THE PREREQUISITE OF THE RESULT
                

                if len(PREREQUISITE_INITIAL) == 0: 
                    nest['prerequisites']['prerequisites_zero'] = "Prerequisites were not found for this course"
                else:
                    Prereq_list = CourseForm.check(PREREQUISITE_INITIAL)  #STRIPS AND TURNS THE PREREQUISITES INTO A LIST

                    nest['prerequisites']['prerequisites_zero'] = PREREQUISITE_INITIAL #ADDS IT INTO THE DICTIONARY
                    

                    P1 = CourseForm.catch_rel(Prereq_list) #Generates a list containing only course codes
                    nest['P1'] = P1

                    if len(P1) > 0:
                        P2_list = [] #Once the loop finishes, it returns a list of lists with the prerequisites split.
                        P2_all = [] #returns a list of lists of the prerequisites - unsplit
                        
#=========================== second layer ==============================================================================================                
                        for course in P1:
                            P2_search = CourseForm.second_search(course) #searches each course code in P1
                            P2_pre = CourseForm.PRQ(P2_search) #Takes the prerequisites if they exist. Returns a long string
                            
                            if P2_pre == 'none':
                                pass
                            else:
                                P2_all.append(P2_pre) 
                                
                                P2_check = CourseForm.check(P2_pre) #Splits the prerequisites
                                P2_list.append(P2_check)

                                P2_zip = dict(zip(P1, P2_list)) #zips the course code and its corresponding prerequisites
                                P2_all_zip = dict(zip(P1, P2_all))
                                
                                nest['P2_all'] = P2_all_zip
                                nest['P2_list'] = P2_list
                                nest['P2_zip_list'] = P2_zip
                                pass
                            pass
#=================================== third layer ========================================================================================================                            
                        P3_list = [] #same as P2_list
                        for num in range(len(P2_list)): #P2 list is multidimensional 
                            P3_catch = CourseForm.catch_rel(P2_list[num]) #filters out P2 list to ensure only course codes are in the new list
                            L = [x for x in P3_catch if CourseForm.PRQ(CourseForm.second_search(x)) != 'none'] #checks if prerequisites exist
                            P3_list.append(L)
                            nest['P3_listt'] = P3_list #multidimensional list
                            pass
                            
        
                        P3_final = [[] for items in range(len(P3_list))] #multidimensional list depending on the dimensions of P3_list
                        P3_Split_final = [[] for items in range(len(P3_list))]
                        P3_to_P4 = [[] for items in range(len(P3_list))]
                        for i in range(len(P3_list)):
                            for q in P3_list[i]:
                                P3_search = CourseForm.second_search(q) 
                                if P3_search != 'none': 
                                    P3_Pre = P3_search["prerequisites"]
                                    P3_check = CourseForm.check(P3_Pre)
                                    P3_to_P4.append(P3_check)
                                    nest['P3_to_P4'] = P3_to_P4
                                    P3_Split_final[i].append(P3_check)
                                    nest['P3_split_final'] = P3_Split_final
                                
                                    
                                    P3_final[i].append(P3_Pre) #appends to corresponding list in the index <- did I use the right terms here?
                                    nest['P3_final'] = P3_final
                                    pass
                                

                        P3_dict = {}          
                        P3_split_dict = {}
                        for i in range(len(P3_final)):
                            P3_dict.update(dict(zip(P3_list[i], P3_final[i]))) #Update = removes duplicates = bad. Taken care of below
                            P3_split_dict.update(dict(zip(P3_list[i], P3_Split_final[i])))
                            nest["P3_dict"] = P3_dict
                            nest["P3_I"] = P3_split_dict
                            continue
                        for j, k in P2_zip.items():
                            for i in k:
                                for l, p in P3_dict.items():
                                    if i in l:
                                        nest['TEST'][j][i] = p
                                    else:
                                        pass
# ===================================== fourth layer =================================================================================================
                        P4_list = []
                        for num in range(len(P3_to_P4)): #P2 list is multidimensional 
                            P4_catch = CourseForm.catch_rel(P3_to_P4[num]) #filters out P2 list to ensure only course codes are in the new list
                            
                            L = [x for x in P4_catch if CourseForm.PRQ(CourseForm.second_search(x)) != 'none'] #checks if prerequisites exist
                            P4_list.append(L)
                            nest['P4_list'] = P4_list #multidimensional list
                            pass
                        
                        P4_final = [[] for items in range(len(P4_list))] #multidimensional list depending on the dimensions of P3_list
                        P4_Split_final = [[] for items in range(len(P4_list))]
                        for i in range(len(P4_list)):
                            for q in P4_list[i]:
                                P4_search = CourseForm.second_search(q) 
                                if P4_search != 'none': 
                                    P4_Pre = P4_search["prerequisites"]
                                    P4_check = CourseForm.check(P4_Pre)
                                    P4_Split_final.append(P4_check)
                                    nest['P4_split_final'] = P4_Split_final
                                
                                    
                                    P4_final[i].append(P4_Pre) #appends to corresponding list in the index <- did I use the right terms here?
                                    nest['P4_final'] = P4_final
                                    pass
                        P4_dict = {}          
                        for i in range(len(P4_final)):
                            P4_dict.update(dict(zip(P4_list[i], P4_final[i]))) #Update = removes duplicates = bad. Taken care of below
                            nest["P4_dict"] = P4_dict
                            pass

                                     
    else:
        form = CourseForm() #if invalid, it reverts back here. important.

    return render(request, 'UofT/UofTpreReq.html', {'form': form, 'nest':nest})




    