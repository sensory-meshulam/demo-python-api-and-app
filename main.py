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

if __name__ == '__main__':
    app.run(debug=True)
