from django.views.generic import DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)    

from models import MyUser    
from django.views.generic import CreateView
import forms
from django.contrib.auth import authenticate, login

def login_user(request):
    user = authenticate(username=request.POST['username'],  password=request.POST['password'])
    login(request, user)
    return HttpResponse("Logged In")

class CreateUserView(CreateView):
    form_class = forms.UserCreateForm
    model = MyUser
    template_name= 'register.html'
    def get_success_url(self):
        print self.request.POST
        new_user = authenticate(username=self.request.POST['username'],
                                    password=self.request.POST['password1'])
        login(self.request, new_user)
        return reverse('profiles_profile_detail')
    
    def get_context_data(self, **kwargs):
        context = super(CreateUserView, self).get_context_data(**kwargs)
        context['action'] = reverse('users-new')
        return context

class CreateProfileView(LoggedInMixin, CreateView):
    model = MyUser
    template_name = 'register.html'
    def get_success_url(self):
        return reverse('django.contrib.auth.views.login')
    
class EditProfileView(LoggedInMixin, UpdateView):
    model = MyUser
    template_name = 'edit_contact.html'
    form_class = forms.UserProfileForm
    def get_success_url(self):
        return reverse('profiles_profile_detail')
    
    
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import json
class ProfileView(LoggedInMixin, DetailView):
    model = MyUser
    template_name = "contact.html"
    form_class = forms.UserProfileForm
    def get_object(self):
        return self.request.user.get_profile()
    
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['like']=Like.objects.filter(profile = self.request.user.get_profile())
        return context
    
class OtherProfileView(LoggedInMixin, DetailView):
    model = MyUser
    template_name = "other_profile.html"
    form_class = forms.UserProfileForm


from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
import socket
from django.core.exceptions import ObjectDoesNotExist
from models import Like
def main(request):
    return render_to_response('ajaxtemplate.html', context_instance=RequestContext(request))
 
def ajax(request):
    if request.POST.has_key('client_response'):
        x = request.POST['client_response']                  
        y = socket.gethostbyname(x)                           
        response_dict = {}                                          
        response_dict.update({'server_response': y 
        })                                                                   
        return HttpResponse(json.dumps(response_dict), mimetype='application/javascript') 
    else:
        return render_to_response('ajaxtemplate.html', context_instance=RequestContext(request))
def mlikes(request):
    return render_to_response('contact.html', context_instance=RequestContext(request))
def likes(request):
    id1 = request.POST['client_id']
    print request.POST
    loggeduserid=request.user.id
    myUser = get_object_or_404(User, id=loggeduserid)
    y = get_object_or_404(MyUser, id=int(id1))
    try:
        likee = Like.objects.get(user = myUser, profile = y)
    except ObjectDoesNotExist:
        y.like_number += 1
        likee = Like()
        likee.user = myUser
        likee.profile = y
        likee.save()
    #print like
    x = y.like_number
    y.save()
    response_dict = {}
    response_dict.update({'server_response': x})
    return HttpResponse(json.dumps(response_dict), mimetype='application/javascript')
    
    