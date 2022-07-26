from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core import serializers
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from requests import request
from .models import Poraka


@login_required()
def gledaj(request):
    poraki = Poraka.objects.all()

    return render(request, 'chatapp/strimanje.html', context={'poraki': poraki})


def send(request):
    message = request.POST['message']
    # username = request.POST['username']
    # room_id = request.POST['room_id']

    new_message = Poraka.objects.create(message=message, sender=request.user)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request):
    poraki = Poraka.objects.all()
    messages = [i.get_text() for i in poraki]
    users = [i.get_username() for i in poraki]
    return JsonResponse({"messages": list(messages), "users": list(users)})





@login_required()
def gledajSTARO(request):
    if request.method == 'POST':
        nova_poraka = Poraka.objects.create(sender=request.user, message=request.POST['message'])
        nova_poraka.save()

        poraki = Poraka.objects.all()   
        context = {
            "poraki": poraki,
        }
        return redirect('chatapp:chatapp-gledaj')

    poraki = Poraka.objects.all()   
    context = {
        "poraki": poraki,
    }
    return render(request, 'chatapp/strimanje.html', context=context)
