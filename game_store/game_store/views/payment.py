from django.shortcuts import render, get_object_or_404
from game_store.models import Game, PlayerGame, Payment
from game_store.forms import PaymentForm
from django.contrib.auth.models import User
from django.conf import settings
from hashlib import md5

#Login checked in function code
def payment_initialize(request):
    if (request.method == 'POST'):
        if request.user.is_authenticated():
            game = get_object_or_404(Game, id=request.POST.get('game'))
            #creating a payment entry
            payment = Payment.objects.create(user=request.user, game=game, amount=game.price)
            payment.pid = 'payment' + str(payment.id)
            payment.sid = settings.PAYMENT_SELLER_ID
            #creating checksum as required by payment service
            md5rawstr = "pid={}&sid={}&amount={}&token={}".format(payment.pid, payment.sid, payment.amount, settings.PAYMENT_SECRET_KEY)
            payment.checksum = md5(md5rawstr.encode("ascii")).hexdigest()
            payment.save()
            payment_form = PaymentForm(instance=payment)
            context = {'game': game, 'payment_form': payment_form}
        else:
            context = {'error': True, 'error_text': 'user is not authenticated'}
    else:
        context = {'error': True, 'error_text': 'GET not allowed'}
    return render(request, 'game_store/payment.html', context)


def payment_response(request, action):
    if request.method == 'GET' and request.GET.get('pid') and request.GET.get('ref') and request.GET.get('result') and request.GET.get('checksum'):
        if request.user.is_authenticated():
            #verifying the checksum
            md5rawstr = "pid={}&ref={}&result={}&token={}".format(request.GET.get('pid'), request.GET.get('ref'), request.GET.get('result'), settings.PAYMENT_SECRET_KEY)
            our_checksum = md5(md5rawstr.encode("ascii")).hexdigest()
            if (our_checksum == request.GET.get('checksum')):
                #if checksum gets verified, get the payment entry for further action
                try:
                    payment = Payment.objects.get(pid=request.GET.get('pid'))
                    #Check the url called for finding out if the payment was success or not
                    if (action == 'success'):
                        #if successful, create an entry in PlayerGame table to complete the purchase
                        payment.ref = request.GET.get('ref')
                        payment.completed = True
                        payment.save()
                        player_game = PlayerGame(game=payment.game, user=payment.user, purchased_price=payment.amount)
                        player_game.save()
                        context = {'response_success': True, 'payment': payment}
                    elif (action == 'cancel'):
                        context = {'response_cancel': True, 'payment': payment}
                    elif (action == 'error'):
                        context = {'response_error': True, 'payment': payment}
                except Payment.DoesNotExist:
                    payment.ref = request.GET.get('ref')
                    payment.save()
                    context = {'error': True, 'error_text': 'Payment request could not be found in database. Pid={}, Ref={}'.format(request.GET.get('pid'),  request.GET.get('ref'))}
            else:
                context = {'error': True, 'error_text': 'Checksum verification failed'}
        else:
            context = {'error': True, 'error_text': 'user is not authenticated'}
    else:
        context = {'error': True, 'error_text': 'Invalid GET parameters'}
    return render(request, 'game_store/payment.html', context)
