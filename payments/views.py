from django.shortcuts import render
import uuid
import hashlib
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .utility import encrypt_aes_ecb_base64


class OpenVirtualAccount(APIView):
    def post(self, request):
        data = request.data

        # ✅ Visible test keys (only use for sandbox/development)
        api_key = data.get("api_key", "iGFX9Yg2AypaiUKMVTYk_b1ea9221596642848af9bdf39a7efc6c")
        app_secret = data.get("app_secret", "9dREG1FeyoE3Slxp")

        if not api_key or not app_secret:
            return Response({"error": "API key and App secret are required."}, status=status.HTTP_400_BAD_REQUEST)

        request_ref = str(uuid.uuid4())
        transaction_ref = str(uuid.uuid4())

        signature_raw = f"{request_ref};{app_secret}"
        signature = hashlib.md5(signature_raw.encode()).hexdigest()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Signature": signature
        }

        payload = {
            "request_ref": request_ref,
            "request_type": "open_account",
            "auth": {
                "type": None,
                "secure": None,
                "auth_provider": "FidelityVirtual",
                "route_mode": None
            },
            "transaction": {
                "mock_mode": "Live",
                "transaction_ref": transaction_ref,
                "transaction_desc": "Open virtual account",
                "transaction_ref_parent": None,
                "amount": 0,
                "customer": {
                    "customer_ref": data.get("phone"),
                    "firstname": data.get("first_name"),
                    "surname": data.get("last_name"),
                    "email": data.get("email"),
                    "mobile_no": data.get("phone")
                },
                "meta": {
                    "amount": data.get("amount", 1000)
                },
                "details": {
                    "name_on_account": f"{data.get('first_name')} {data.get('last_name')}",
                    "middlename": data.get("middle_name", ""),
                    "dob": data.get("dob"),
                    "gender": data.get("gender"),
                    "title": data.get("title", "Mr"),
                    "address_line_1": data.get("address1"),
                    "address_line_2": data.get("address2"),
                    "city": data.get("city"),
                    "state": data.get("state"),
                    "country": data.get("country", "Nigeria")
                }
            }
        }

        response = requests.post("https://api.paygateplus.ng/v2/transact", headers=headers, json=payload)

        return Response(response.json(), status=response.status_code)




 # Fund Transfer

class TransferFundsView(APIView):
    def post(self, request):
        data = request.data

        # Required keys from settings
        api_key = data.get("api_key", "iGFX9Yg2AypaiUKMVTYk_b1ea9221596642848af9bdf39a7efc6c")
        app_secret = data.get("app_secret", "9dREG1FeyoE3Slxp")


        # Generate IDs
        request_ref = str(uuid.uuid4())
        transaction_ref = str(uuid.uuid4())

        # Signature = MD5(request_ref + ";" + app_secret)
        signature_raw = f"{request_ref};{app_secret}"
        signature = hashlib.md5(signature_raw.encode()).hexdigest()

        # Encrypt source account
        source_account = data.get("source_account")
        encrypted_source_account = encrypt_aes_ecb_base64(source_account, app_secret)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Signature": signature,
        }

        payload = {
            "request_ref": request_ref,
            "request_type": "transfer_funds",
            "auth": {
                "type": "bank.account",
                "secure": encrypted_source_account,
                "auth_provider": "Fidelity",
                "route_mode": None
            },
            "transaction": {
                "mock_mode": "Live",
                "transaction_ref": transaction_ref,
                "transaction_desc": data.get("description", "A random transaction"),
                "transaction_ref_parent": None,
                "amount": data.get("amount"),  # amount in kobo
                "customer": {
                    "customer_ref": data.get("customer_id"),
                    "firstname": data.get("firstname"),
                    "surname": data.get("surname"),
                    "email": data.get("email"),
                    "mobile_no": data.get("mobile_no")
                },
                "meta": data.get("meta", {}),
                "details": {
                    "destination_account": data.get("destination_account"),
                    "destination_bank_code": data.get("destination_bank_code"),
                    "otp_override": True
                }
            }
        }

        url = "https://api.paygateplus.ng/v2/transact"
        response = requests.post(url, json=payload, headers=headers)
        return Response(response.json(), status=response.status_code)






        #Verify Account

class VerifyAccountView(APIView):
    def post(self, request):
        data = request.data

        account_number = data.get("account_number")
        bank_code = data.get("bank_code")

        if not account_number or not bank_code:
            return Response({"error": "Account number and bank code are required."}, status=400)

        api_key = data.get("api_key", "iGFX9Yg2AypaiUKMVTYk_b1ea9221596642848af9bdf39a7efc6c")
        app_secret = data.get("app_secret", "9dREG1FeyoE3Slxp")


        request_ref = str(uuid.uuid4())
        transaction_ref = str(uuid.uuid4())
        signature = hashlib.md5(f"{request_ref};{app_secret}".encode()).hexdigest()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Signature": signature
        }

        payload = {
            "request_ref": request_ref,
            "request_type": "verify_account",
            "auth": {
                "type": None,
                "secure": None,
                "auth_provider": "FidelityVirtual",
                "route_mode": None
            },
            "transaction": {
                "mock_mode": "Live",
                "transaction_ref": transaction_ref,
                "transaction_desc": "Verify recipient account name",
                "amount": 0,
                "customer": {
                    "customer_ref": account_number,
                    "firstname": "",
                    "surname": "",
                    "email": "",
                    "mobile_no": ""
                },
                "details": {
                    "destination_account": account_number,
                    "destination_bank_code": bank_code
                }
            }
        }

        url = "https://api.paygateplus.ng/v2/transact"
        response = requests.post(url, headers=headers, json=payload)
        return Response(response.json(), status=response.status_code)







class GetAccountBalance(APIView):
    def post(self, request):
        data = request.data

        

        request_ref = str(uuid.uuid4())
        transaction_ref = str(uuid.uuid4())
        encrypted_account = encrypt_aes_ecb_base64(data["account_number"], app_secret)

        signature_raw = f"{request_ref};{app_secret}"
        signature = hashlib.md5(signature_raw.encode()).hexdigest()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Signature": signature
        }

        payload = {
            "request_ref": request_ref,
            "request_type": "get_balance",
            "auth": {
                "type": "bank.account",
                "secure": encrypted_account,
                "auth_provider": "Fidelity",
                "route_mode": None
            },
            "transaction": {
                "mock_mode": "Live",
                "transaction_ref": transaction_ref,
                "transaction_desc": "Get account balance",
                "transaction_ref_parent": None,
                "amount": 0,
                "customer": {
                    "customer_ref": data["customer_ref"],
                    "firstname": data.get("first_name", ""),
                    "surname": data.get("last_name", ""),
                    "email": data.get("email", ""),
                    "mobile_no": data.get("mobile_no", "")
                },
                "meta": {
                    "a_key": "value_a",
                    "b_key": "value_b"
                },
                "details": None
            }
        }

        response = requests.post("https://api.paygateplus.ng/v2/transact", headers=headers, json=payload)
        return Response(response.json(), status=response.status_code)





        

class PaymentWebhookView(APIView):
    def post(self, request):
        data = request.data

        # ✅ Verify Signature
        request_ref = data.get("request_ref")
        signature_header = request.headers.get("Signature")
        app_secret = "YOUR_APP_SECRET"

        expected_signature = hashlib.md5(f"{request_ref};{app_secret}".encode()).hexdigest()
        if signature_header != expected_signature:
            return Response({"error": "Invalid signature"}, status=403)

        # ✅ Process only successful credits
        details = data.get("details", {})
        if details.get("status") != "Successful":
            return Response({"status": "Ignored non-success transaction"}, status=200)

        # ✅ Extract transaction details
        amount = details.get("amount")
        account = details.get("meta", {}).get("cr_account")
        sender_name = details.get("meta", {}).get("originator_account_name")
        narration = details.get("meta", {}).get("narration")

        # TODO: match this cr_account to a user in your system
        # TODO: update their wallet balance or trigger related service

        return Response({"status": "Payment processed"}, status=200)

