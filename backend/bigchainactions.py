#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Sat Apr  7 13:48:11 2018

                bdb = BigchainDB('https://test.bigchaindb.com', headers=tokens)
                parcel_asset = {
                    'data': {
                        'parcel': {
                            'serial_number': '9999',
                            'manufacturer': 'producer'
                        },
                    },
                }


@author: alex
"""
from settings import tokens
from settings import master_receiver_private_key, master_receiver_public_key 
from settings import master_sender_private_key,master_sender_public_key
from bigchaindb_driver import BigchainDB
from time import sleep
import random #used to generate random string
import string #used to generate random string



def createAsset(pri_key, pub_key):
    bdb = BigchainDB('https://test.bigchaindb.com', headers=tokens)
    rnd_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    parcel_asset = {
        'data': {
            'parcel': {
                'serial_number': rnd_str,
                'manufacturer': 'producer'
            },
        },
    }
        
    parcel_asset_metadata = {
        'parceltype': 'box'
    }            
    tx1 = bdb.transactions.prepare(
    operation='CREATE',
        signers=pub_key,
        recipients=pub_key,
        asset=parcel_asset,
        metadata=parcel_asset_metadata
    )
    #print('Transaction 1', tx1)
    #print('Transaction 1', tx1)
    tx_signed1 = bdb.transactions.fulfill(
        tx1,
        private_keys=pri_key
    )
    # this function does the actual transaction
    dummy_sent_creation_tx = bdb.transactions.send(tx_signed1)
    txid = tx_signed1['id']
    trials = 0
    while trials < 10:
        try:
            if bdb.transactions.status(txid).get('status') == 'valid':
                print('[createAsset]: Succes', trials, 'secs')
                break
        except:
            trials += 1
            sleep(1)
        if trials == 10:
            print('[createAsset]: FAIL ... Bye!')
            # alex removed error catching!!!                   
            break 

def transferAsset(sender_public_key,sender_private_key,receiver_public_key, receiver_private_key): # sender shoul dbe in here but need todo define crytokey from pair which is why now direct reference to master_sender_public_key master_sender_private_key
    print('transferAsset function called')   
    bdb = BigchainDB('https://test.bigchaindb.com', headers=tokens)
    # get transaction owned by alice_pubkey
    list_of_assets = bdb.outputs.get(sender_public_key,False)
        
    # test
    #list_of_assets = bdb.outputs.get(sender.public_key,False) # false is assets that are not yet transferred 
    
    if list_of_assets: #check whether an asset exists before continuing
        top_transaction =list_of_assets[0]
        current_transaction_id = top_transaction['transaction_id']
        current_transaction = bdb.transactions.retrieve(top_transaction['transaction_id'])
        transfer_asset = {
            'id': current_transaction_id
        }
        output_index = 0
        output = current_transaction['outputs'][output_index]

        transfer_input = {
           'fulfillment': output['condition']['details'],
           'fulfills': {
               'output_index': output_index,
               'transaction_id': top_transaction['transaction_id']
            },
            'owners_before': output['public_keys']
        }        
        
        prepared_transfer_tx = bdb.transactions.prepare(
            operation='TRANSFER',
            asset=transfer_asset,
            inputs=transfer_input, # hwat i need from the transaction
            #recipients='kRkyL8X2AavMvcPB2NGPGFr1S8BvYeTZfQ8kTeZM1X4'
            recipients=receiver_public_key
        )
        
        fulfilled_transfer_tx = bdb.transactions.fulfill(
            prepared_transfer_tx,
            #private_keys='tSc2YBW4gYUzXWeoUB8QmB3D5BpezGrTCvaUCCowAUx',
            private_keys=sender_private_key,
        )
        
        sent_transfer_tx = bdb.transactions.send(fulfilled_transfer_tx) # finally we will send the transaction
        #sent_transfer_tx == fulfilled_transfer_tx
        
        txid = fulfilled_transfer_tx['id']
        trials = 0
        while trials < 10:
            try:
                if bdb.transactions.status(txid).get('status') == 'valid':
                    print('[transferAsset]: Success in ', trials, 'secs')
                    break
            except:
                trials += 1
                sleep(1)
            if trials == 10:
                print('[transferAsset]: FAIL ... Bye!')
                # alex removed error catching!!!                   
                break                         
        return True
    else:
        return False
    # list_of_assets = bdb.outputs.get(master_sender_private_key,False) #test line, assets need to be in bigchaindb
    #x = bdb.outputs.get(master_sender.public_key, false)
    
    # if this returns whole transaction then grab one from list and use it to sign transfer
    # if this returns lsit of transaction ids use 
    
#    print(list_of_assets)
#    prepared_transfer_tx = bdb.transactions.prepare(
#        operation='TRANSFER',
#        asset=transfer_asset,
#        inputs=transfer_input, # hwat i need from the transaction
#        recipients=carol.public_key
#    )    
#    
#    fulfilled_transfer_tx = bdb.transactions.fulfill(
#        prepared_transfer_tx,
#        private_keys=[sender.private_key, receiver.private_key],
#    )    
#    
#    print('Prepared transfer', prepared_transfer_tx)
#    sent_transfer_tx = bdb.transactions.send(fulfilled_transfer_tx)
#    
#    trials = 0
#   while trials < 60:
#       try:
#           if bdb.transactions.status(sent_transfer_tx['id']).get('status') == 'valid':
#               print('Tx Transfer valid in:', trials, 'secs')
#               break
#       except bigchaindb_driver.exceptions.NotFoundError:
#           trials += 1
#           sleep(1)




                            