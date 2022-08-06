import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Poraka
from formula_app.models import Trka


@login_required()
@require_http_methods(["GET"])
def gledaj(request):
    poraki = Poraka.objects.all()
    sledna_trka = Trka.objects.filter(pocetok__gte=datetime.datetime.now()).order_by("pocetok").first()
    context = {
        "poraki": poraki,
        "sledna_trka": sledna_trka,
    }
    return render(request, 'chatapp/strimanje.html', context=context)


@require_http_methods(["POST"])
def send(request):
    message = request.POST['message']
    new_message = Poraka.objects.create(message=message, sender=request.user)
    new_message.save()
    return HttpResponse('Message sent successfully')


@require_http_methods(["GET"])
def getMessages(request):
    poraki = Poraka.objects.all()
    messages = [i.get_text() for i in poraki]
    users = [i.get_username() for i in poraki]
    return JsonResponse({"messages": list(messages), "users": list(users)})





@login_required()
def gledajSTARO(request):
    """
    Treba refresh za da pokazuva porakite, toa gore e podobro so AJAX so e
    """
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
