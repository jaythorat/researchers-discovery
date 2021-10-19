from django.shortcuts import render,redirect
from hexapod.vidwanquery import query
from hexapod.vidwanprofilepage import author_profile
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse, response
import time
# Create your views here.

def home(request):

    if request.method == "POST":
        search_query = request.POST.get('search')
        query(search_query)
        # context = query.listnameaff
        home.context = query.auth_dict
        return redirect('/results')
        # return render(request, 'home.html')
    return render(request,"home.html")


def results(request):
    if request.method == "GET":
        context = home.context
        return render(request, 'results.html', context)
    
    if request.method == "POST":
        id = request.POST.get('id')
        expertid = home.context['authdata'][int(id)]['expertid']
        results.url = "https://vidwan.inflibnet.ac.in/profile/"+str(expertid)
        author_profile(results.url)
        results.authdatadict = author_profile.authorprofiledata
        response = redirect('profile')
        return response

def profile(request):
    if request.method == "GET":
        time.sleep(12)
        context = results.authdatadict
        # return JsonResponse(context)
        return render(request,"profile.html",context)
    else:
        return render(request,"home.html")

    