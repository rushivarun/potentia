from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
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
    return render(request, 'post/AddTrans.html', {'trans_form':trans_form, 'rate':rate})


def my_trans(request):
    Flare = (request.user.additional.Potentia / rate)
    all_trans = Transactions.objects.filter(user__exact=request.user)
    return render(request, 'post/AllTrans.html',{'all_trans':all_trans,'PotentiaWallet': request.user.additional.Potentia, 'Flare':Flare})
