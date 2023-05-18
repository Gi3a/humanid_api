import json


from web3 import Web3, HTTPProvider
from fastapi import FastAPI, HTTPException
from web3.middleware import geth_poa_middleware

from models import Face, Human
from configs.settings import settings


w3 = Web3(HTTPProvider(settings.ETH_PROVIDER))


w3.middleware_onion.inject(geth_poa_middleware, layer=0)

abi = json.loads(settings.CONTRACT_ABI)
contract_address = w3.toChecksumAddress(settings.CONTRACT_ADDRESS)
contract = w3.eth.contract(address=contract_address, abi=abi)

your_private_key = settings.ETH_PRIVATE_KEY
your_account = w3.eth.account.from_key(your_private_key)


def send_transaction(function, *args):
    nonce = w3.eth.getTransactionCount(your_account.address)
    gas_price = w3.eth.gasPrice
    estimated_gas = function(*args).estimateGas({'from': your_account.address})

    transaction = function(*args).buildTransaction({
        'gas': estimated_gas,
        'gasPrice': gas_price,
        'nonce': nonce,
    })
    signed = w3.eth.account.signTransaction(transaction, your_private_key)
    return w3.eth.sendRawTransaction(signed.rawTransaction)


async def add_human(human_data: Human):
    print("Add Human process Store")
    # Add user exsist verification
    checksum_address = Web3.toChecksumAddress(human_data.public_key)
    try:
        tx_hash = send_transaction(contract.functions.addHuman, checksum_address, human_data.personal_data,
                                   human_data.face_encodings, human_data.encrypted_public_key, human_data.encrypted_private_key)
        print("hash", tx_hash.hex())
        return {'transaction_hash': tx_hash.hex()}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))


async def refresh_human(old_public_key, human_data: Human):
    print("Update Human process Store")
    old_checksum_address = Web3.toChecksumAddress(old_public_key)
    new_checksum_address = Web3.toChecksumAddress(human_data.public_key)
    try:
        tx_hash = send_transaction(contract.functions.updateHuman, old_checksum_address, new_checksum_address,
                                   human_data.personal_data, human_data.face_encodings,
                                   human_data.encrypted_public_key, human_data.encrypted_private_key)
        return {'transaction_hash': tx_hash.hex()}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))


async def kill_human(human_data: Human):
    checksum_address = Web3.toChecksumAddress(human_data.public_key)
    try:
        tx_hash = send_transaction(
            contract.functions.deleteHuman, checksum_address)
        return {'transaction_hash': tx_hash.hex()}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))


async def get_face_encodings(public_key: str):
    print("Get Human Face proccess")
    checksum_address = Web3.toChecksumAddress(public_key)
    try:
        face_encodings = contract.functions.getFaceEncodings(
            checksum_address).call()
        return {'face_encodings': face_encodings}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))


async def get_human(public_key: str):
    print("Get Human process Store")
    checksum_address = Web3.toChecksumAddress(public_key)
    try:
        human = contract.functions.humans(checksum_address).call()
        return {
            'public_key': human[0],
            'personal_data': human[1],
            'face_encodings': human[2],
            'encrypted_public_key': human[3],
            'encrypted_private_key': human[4]
        }
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))
