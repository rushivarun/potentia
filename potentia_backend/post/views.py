from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from post.forms import AddTransactionForm
from post.models import Transactions

rate = 8

def add_transaction(request):
    if request.method == 'POST':
        trans_form = AddTransactionForm(data=request.POST)
        if trans_form.is_valid():
            trans = trans_form.save(commit = False)
            trans.user = request.user
            trans.cost = trans.amount * rate
            trans.save()
            return redirect('index')
        else:
            return HttpResponseRedirect(request, 'MyTrans')
    else:
        trans_form = AddTransactionForm()
    return render(request, 'post/AddTrans.html', {'trans_form':trans_form, 'rate':rate})


def my_trans(request):
    all_trans = Transactions.objects.filter(user__exact=request.user)
    return render(request, 'post/AllTrans.html',{'all_trans':all_trans})
