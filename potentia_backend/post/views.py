from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from loginSignup.models import AddSignup

# Create your views here.
from post.forms import AddTransactionForm
from post.models import Transactions

rate = 8

def add_transaction(request):
    fail= False
    if request.method == 'POST':
        trans_form = AddTransactionForm(data=request.POST)
        if trans_form.is_valid():
            trans = trans_form.save(commit = False)
            trans.user = request.user
            trans.cost = trans.amount * rate
            sentuser = AddSignup.objects.get(user__exact=trans.tosenduser)
            if (sentuser.Potentia-trans.cost>=0):
                sentuser.Potentia = sentuser.Potentia - trans.cost
                sentuser.save()
                trans.save()
                return redirect('post:My_Trans')
            else:
                fail = True
                return render(request, 'post/AddTrans.html', {'trans_form': trans_form, 'rate': rate, 'fail': fail})

        else:
            return HttpResponseRedirect(request, 'AllTrans')
    else:
        trans_form = AddTransactionForm()
    return render(request, 'post/AddTrans.html', {'trans_form':trans_form, 'rate':rate, 'fail':fail})


def my_trans(request):
    Flare = (request.user.additional.Potentia / rate)
    all_trans = Transactions.objects.filter(user__exact=request.user)
    return render(request, 'post/AllTrans.html',{'all_trans':all_trans,'PotentiaWallet': request.user.additional.Potentia, 'Flare':Flare})
