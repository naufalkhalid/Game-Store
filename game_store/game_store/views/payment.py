from django.shortcuts import render, get_object_or_404
from game_store.models import Game, PlayerGame, Payment
from game_store.forms import PaymentForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.conf import settings
from hashlib import md5

#Login checked in function code
def payment(request, action):
    if ((request.method == 'POST') and (action == 'initialize') and request.user.is_authenticated()):
        game = get_object_or_404(Game, id=request.POST.get('game'))
        payment = Payment.objects.create(user=request.user, game=game, amount=game.price)
        payment.pid = 'payment' + str(payment.id)
        payment.sid = settings.PAYMENT_SELLER_ID
        md5rawstr = "pid={}&sid={}&amount={}&token={}".format(payment.pid, payment.sid, payment.amount, settings.PAYMENT_SECRET_KEY)
        payment.checksum = md5(md5rawstr.encode("ascii")).hexdigest()
        payment.save()
        payment_form = PaymentForm(instance=payment)
        context = {
            'game': game,
            'payment_form': payment_form
        }
    elif request.method == 'GET' and request.user.is_authenticated() :
        #Handle payment response
        if action == 'success':
            return HttpResponse('Success')
        elif action == 'error':
            return HttpResponse('error')
        elif action == 'cancel':
            return HttpResponse('cancel')
        elif action == 'initialize':
            return HttpResponseBadRequest('Direct Access to initialize payment not allowed')
    else:
        return HttpResponse('User should be signed in')

    return render(request, 'game_store/payment.html', context)
