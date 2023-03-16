from flask import Flask, request, jsonify
import requests
from werkzeug.datastructures import FileStorage
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

MESHULAM_PAGE_CODE = '539888f537b7'
MESHULAM_API_KEY = 'b60e1d4cbd29'
MESHULAM_USER_ID = 'cf2ebf779f618e59'
MESHULAM_API_URL = 'https://sandbox.meshulam.co.il/api/light/server/1.0/'

@app.route('/')
def index():
    return app.send_static_file('index.html')
 

@app.route('/api/payment/getPaymentLink', methods=['POST'])
def get_payment_link():

    sum = request.json['sum']
    paymentsNum = request.json['paymentsNum']
    description = request.json['description']

    formData = {
        'pageCode': MESHULAM_PAGE_CODE,
        'userId': MESHULAM_USER_ID,
        'apiKey': MESHULAM_API_KEY,
        'sum': sum,
        'paymentNum': str(paymentsNum),
        'description': description,
        'transactionTypes': ['1', '6', '13', '14'], #[Credit, Bit, ApplePay, GooglePay] If you don't need one of them, give it a value of '1'
        'cField1': MESHULAM_PAGE_CODE,
        'cField2': 'blabla',
        'cField3': 'blabla',
        'cField4': 'blabla',
        'cField5': 'blabla'
    }

    form = {}
    for key, value in formData.items():
        if key == 'transactionTypes':
            form[key] = []
            for item in value:
                form[key].append(item)
        else:
            form[key] = value
            
    try:
        print(form)
        response = requests.post(f'{MESHULAM_API_URL}createPaymentProcess', data=form)
        data = response.json()
        status = data['status']
        authCode = data['data']['authCode'] if 'data' in data and 'authCode' in data['data'] else None
        message = data['err']['message'] if 'err' in data and 'message' in data['err'] else None
        result = {
            'isSuccess': int(status) > 0,
            'message': authCode if int(status) > 0 else message
        }
        return jsonify(result)
    except Exception as e:
        return '', 500

@app.route('/api/payment/confirmPayment', methods=['POST'])
def confirm_payment():
    data = request.form.to_dict()
    response = approve_transaction(data)
    if response:
        # you can save data['data'] in DB
        return 'OK'
    else:
        # display error message
        return 'Error'

async def approve_transaction(details):
    data = {
        'apiKey': MESHULAM_API_KEY,
        'pageCode': details['customFields[cField3]'],
        'transactionId': str(details['transactionId']),
        'transactionToken': details['transactionToken'],
        'transactionTypeId': details['transactionTypeId'],
        'paymentType': details['paymentType'],
        'processId': str(details['processId']),
        'sum': details['sum'],
        'firstPaymentSum': details['firstPaymentSum'],
        'periodicalPaymentSum': details['periodicalPaymentSum'],
        'paymentsNum': details['paymentsNum'],
        'allPaymentsNum': details['allPaymentsNum'],
        'paymentDate': details['paymentDate'],
        'asmachta': details['asmachta'],
        'description': details['description'],
        'fullName': details['fullName'],
        'payerPhone': details['payerPhone'],
        'payerEmail': details.get('payerEmail', ''),
        'cardSuffix': details['cardSuffix'],
        'cardType': details['cardType'],
        'cardTypeCode': details['cardTypeCode'],
        'cardBrand': details['cardBrand'],
        'cardBrandCode': details['cardBrandCode'],
        'cardExp': details['cardExp'],
        'processToken': details['processToken']
    }
    response = requests.post(f'{MESHULAM_API_URL}/approveTransaction', data=data)
    response_data = response.json()
    if response_data['err'] and response_data['err']['message']:
        # display error message
        return False

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(MESHULAM_API_URL + 'approveTransaction', data=formData) as response:
                res = await response.json()
                if 'err' in res and 'message' in res['err']:
                    # display error message
                    return res['status'] == 1
        except Exception as error:
            # handle error
            dess

if __name__ == '__main__':
    app.run(debug=True)
