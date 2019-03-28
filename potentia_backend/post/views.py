from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView

from loginSignup.models import AddSignup
from .block_init import *
from post.forms import AddTransactionForm
from post.models import Transactions
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

#rated constants 
rate = 8
sender, reciever = generate_keypair(), generate_keypair()


def trasact_block(sender, reciever, flares):
    sender_key, reciever_key = generate_keypair(), generate_keypair()

    # Use YOUR BigchainDB Root URL here
    bdb_root_url = 'https://test.bigchaindb.com/'

    bdb = BigchainDB(bdb_root_url)

    energy = {
        'data': {
            'flares': {
                # sameeran replace timestamp, public key sender dictionaties with real values from views
                'timestamp': 'timestamp',
                # they are not supposed to be string but variables.
                'public_key_sender': sender_key.public_key,
                'sender': sender,
                'public_key_reciever': reciever_key.public_key,
                'flares': flares
            }
        }
    }

    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=sender_key.public_key,
        asset=energy
    )

    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx,
        private_keys=sender_key.private_key
    )

    sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)

    txid = fulfilled_creation_tx['id']

    asset_id = txid

    transfer_asset = {
        'id': asset_id
    }

    output_index = 0
    output = fulfilled_creation_tx['outputs'][output_index]

    transfer_input = {
        'fulfillment': output['condition']['details'],
        'fulfills': {
            'output_index': output_index,
            'transaction_id': fulfilled_creation_tx['id']
        },
        'owners_before': output['public_keys']
    }

    prepared_transfer_tx = bdb.transactions.prepare(
        operation='TRANSFER',
        asset=transfer_asset,
        inputs=transfer_input,
        recipients=reciever_key.public_key,
    )

    fulfilled_transfer_tx = bdb.transactions.fulfill(
        prepared_transfer_tx,
        private_keys=sender_key.private_key,
    )

    sent_transfer_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)
    return sent_transfer_tx, sent_creation_tx


def add_transaction(request):
    av_flares = request.user.additional.flares
    if request.method == 'POST':
        trans_form = AddTransactionForm(data=request.POST)
        if trans_form.is_valid():
            trans = trans_form.save(commit = False)
            trans.user = request.user
            trans.cost = trans.amount * rate
            if trans.amount >= request.user.additional.flares:
                return render(request, 'post/TransUploadFail.html',{'user':request.user})
            trans.status = False
            trans.save()
            return render(request, 'post/TransUploadSuccess.html',{'user':request.user, 'trans_id':trans.trans_id})



        else:
            return HttpResponseRedirect(request, 'AllTrans')
    else:
        trans_form = AddTransactionForm()
    return render(request, 'post/AddTrans.html', {'trans_form':trans_form, 'rate':rate, 'av_flares':av_flares})


def my_trans(request):
    av_flares = request.user.additional.flares
    all_trans = Transactions.objects.filter(user__exact=request.user).filter(status__exact=True)
    return render(request, 'post/AllTrans.html',{'all_trans':all_trans, 'PotentiaWallet': request.user.additional.Potentia, 'av_flares':av_flares})

class open_trans(ListView):
    template_name = 'post/opentrans.html'
    context_object_name = 'OpenTrans'
    queryset = Transactions.objects.filter(status__exact=False)


def make_trans(request, pk):
    trans = Transactions.objects.filter(trans_id__exact=pk)
    if trans.cost <= request.user.additional.Potentia:
        trans.tosenduser = request.user
        trans.sent_transfer_tx, trans.sent_creation_tx = trasact_block(trans.user,trans.tosenduser,trans.amount)
        trans.save()
        return render(request, 'post/TransComplete.html',{'trans':trans})
    else:
        return render(request, 'post/TransFail.html')
