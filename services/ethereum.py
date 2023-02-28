from web3 import Web3, Account
from dotenv import load_dotenv
import os

load_dotenv()


class EthereumConnection:
    def __init__(self):
        self.private_key = os.getenv("ETH_PRIVATE_KEY")
        self.public_key = os.getenv("ETH_PUBLIC_KEY")
        self.contract_address = os.getenv("CONTRACT_ADDRESS")
        self.contract_abi = [
            {
                "inputs": [],
                "stateMutability": "nonpayable",
                "type": "constructor"
            },
            {
                "inputs": [
                    {
                        "internalType": "string",
                        "name": "id_number",
                                "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "email",
                                "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "password",
                                "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "name",
                                "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "nationality",
                                "type": "string"
                    },
                    {
                        "internalType": "uint256",
                        "name": "date_of_birth",
                                "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "phone",
                                "type": "string"
                    }
                ],
                "name": "addPassport",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "",
                        "type": "address"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "",
                        "type": "bytes32"
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "publicKey",
                                "type": "address"
                    }
                ],
                "name": "deletePassport",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getAllPassports",
                "outputs": [
                        {
                            "components": [
                                {
                                    "internalType": "string",
                                    "name": "id_number",
                                    "type": "string"
                                },
                                {
                                    "internalType": "string",
                                    "name": "email",
                                    "type": "string"
                                },
                                {
                                    "internalType": "string",
                                    "name": "password",
                                    "type": "string"
                                },
                                {
                                    "internalType": "string",
                                    "name": "name",
                                    "type": "string"
                                },
                                {
                                    "internalType": "string",
                                    "name": "nationality",
                                    "type": "string"
                                },
                                {
                                    "internalType": "uint256",
                                    "name": "date_of_birth",
                                    "type": "uint256"
                                },
                                {
                                    "internalType": "address",
                                    "name": "public_key",
                                    "type": "address"
                                },
                                {
                                    "internalType": "bytes32",
                                    "name": "private_key",
                                    "type": "bytes32"
                                },
                                {
                                    "internalType": "string",
                                    "name": "phone",
                                    "type": "string"
                                }
                            ],
                            "internalType": "struct HumanID.Passport[]",
                            "name": "",
                            "type": "tuple[]"
                        }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "_address",
                                "type": "address"
                    }
                ],
                "name": "getPassport",
                "outputs": [
                    {
                        "components": [
                            {
                                "internalType": "string",
                                "name": "id_number",
                                "type": "string"
                            },
                            {
                                "internalType": "string",
                                "name": "email",
                                "type": "string"
                            },
                            {
                                "internalType": "string",
                                "name": "password",
                                "type": "string"
                            },
                            {
                                "internalType": "string",
                                "name": "name",
                                "type": "string"
                            },
                            {
                                "internalType": "string",
                                "name": "nationality",
                                "type": "string"
                            },
                            {
                                "internalType": "uint256",
                                "name": "date_of_birth",
                                "type": "uint256"
                            },
                            {
                                "internalType": "address",
                                "name": "public_key",
                                "type": "address"
                            },
                            {
                                "internalType": "bytes32",
                                "name": "private_key",
                                "type": "bytes32"
                            },
                            {
                                "internalType": "string",
                                "name": "phone",
                                "type": "string"
                            }
                        ],
                        "internalType": "struct HumanID.Passport",
                        "name": "",
                        "type": "tuple"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "string",
                        "name": "id_number",
                                "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "email",
                                "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "password",
                                "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "name",
                                "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "nationality",
                                "type": "string"
                    },
                    {
                        "internalType": "uint256",
                        "name": "date_of_birth",
                                "type": "uint256"
                    },
                    {
                        "internalType": "address",
                        "name": "publicKey",
                                "type": "address"
                    },
                    {
                        "internalType": "string",
                        "name": "phone",
                                "type": "string"
                    }
                ],
                "name": "updatePassport",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
        self.w3 = Web3(Web3.HTTPProvider(os.getenv("ETH_NODE_URL")))
        self.contract = self.w3.eth.contract(
            address=self.contract_address, abi=self.contract_abi)
        self.account = Account.from_key(self.private_key)
        def add_passport(self, id_number, email, password, name, nationality, date_of_birth, phone):
        sender = self.account.address
        gas_price = self.w3.eth.gas_price
        transaction = {
            'to': self.contract_address,
            'from': sender,
            'gas': 2000000,
            'gasPrice': gas_price,
            'nonce': self.w3.eth.getTransactionCount(sender),
        }
        tx_hash = self.contract.functions.addPassport(
            id_number,
            email,
            password,
            name,
            nationality,
            date_of_birth,
            phone
        ).transact(transaction, private_key=self.private_key)

        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        event = self.contract.events.PassportAdded().processReceipt(tx_receipt)[
            0]
        passport_address = event.args.publicKey
        private_key_hash = event.args.privateKeyHash.hex()

        return {"address": passport_address, "private_key_hash": private_key_hash}
