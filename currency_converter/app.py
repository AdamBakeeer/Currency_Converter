from flask import Flask, render_template, request, redirect, url_for
import requests
import os


app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')


def get_supported_currencies(api_key):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    response = requests.get(url)

    print(f"Response Status Code: {response.status_code}")
    

    if response.status_code == 200:  
        data = response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")

    return data.get('conversion_rates', {})


    

@app.route('/', methods=['GET', 'POST'])
def index():
    api_key = "2bfaa0e2b8f803debb73a5d1" 
    currencies = get_supported_currencies(api_key).keys()
    print(currencies)

    result = None
    error_message = None

    if request.method == 'POST':
        base_currency = request.form.get('base_currency')
        target_currency = request.form.get('target_currency')
        amount = request.form.get('amount')

        print(amount)
        print(base_currency)
        print(target_currency)

        if not base_currency or not target_currency or not amount:
            error_message = "Please fill out all fields."
        else:
            
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
            response = requests.get(url)


            if response.status_code == 200:
                data = response.json()
                
                conversion_rates = data.get('conversion_rates', {})
                rate = conversion_rates.get(target_currency)
                print(rate)
                result = float(amount) * rate            


    return render_template('index.html', currencies=currencies, result=result, error_message=error_message)

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)