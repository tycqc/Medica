from django.shortcuts import render
from user.models import User
from django.http import HttpResponse,HttpResponseRedirect
import json

def user_index(request):
    if request.session.get('is_login', None):
        storeid = request.session.get('userid')
    else:
        return login(request)
    user = User.objects.get(pk=storeid)
    output = {'username': user.username, 'nickname': user.name, 'phonenumber': user.phonenumber, 'desc': user.desc}
    output_json = json.dumps(output, ensure_ascii=False)
    return HttpResponse (output_json)