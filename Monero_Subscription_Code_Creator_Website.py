import os
import gzip
import json
import base64
import random
from datetime import datetime
from flask import Flask, request, render_template


# FUNCTIONS ############################################################################################################
def make_payment_id():
    payment_id = ''.join([random.choice('0123456789abcdef') for _ in range(16)])
    return payment_id


def make_monero_subscription_code(json_data):
    # Convert the JSON data to a string
    json_str = json.dumps(json_data)

    # Compress the string using gzip compression
    compressed_data = gzip.compress(json_str.encode('utf-8'))

    # Encode the compressed data into a Base64-encoded string
    encoded_str = base64.b64encode(compressed_data).decode('ascii')

    # Add the Monero Subscription identifier
    monero_subscription = 'monero-subscription:' + encoded_str

    return monero_subscription


def clear():
    if os.name == 'nt':  # for windows
        os.system('cls')
    else:  # for mac and linux(here, os.name is 'posix')
        os.system('clear')


# CHECK FUNCTIONS ######################################################################################################
def check_name(name):
    if len(name) <= 50:
        return True
    else:
        print(f'Subscription name "{name}" is too long. Please update it to be 50 characters or less in the {filename} file.')
        return False


def check_currency(currency):
    if currency == 'USD' or currency == 'XMR':
        return True
    else:
        print(f'Currency "{currency}" is not yet supported. Please use either "XMR" or "USD". Update it in the {filename} file.')
        return False


def check_wallet(wallet_address):
    # Check if the wallet address starts with the number 4
    if wallet_address[0] != "4":
        print(f'Wallet "{wallet_address}" is not valid. It should start with a "4" Update it in the {filename} file.')
        return False

    # Check if the wallet address is exactly 95 characters long
    if len(wallet_address) != 95:
        print(f'Wallet "{wallet_address}" is not valid. It should be exactly 95 characters long. Update it in the {filename} file.')
        return False

    # Check if the wallet address contains only valid characters
    valid_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    for char in wallet_address:
        if char not in valid_chars:
            print(f'Wallet "{wallet_address}" is not valid. It contains invalid characters. Update it in the {filename} file.')
            return False

    # If it passed all these checks
    return True


def check_start_date(start_date):
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        return True
    except ValueError:
        print(f'Subscription Start Date "{start_date}" is not valid. It needs to be in Year-Month-Day format. Examples: 2023-01-26, 2023-12-21, 2023-07-01. Update it in the {filename} file.')
        return False


def check_amount(amount):
    if type(amount) is float:
        return True
    else:
        print(f'Amount "{amount}" is not valid. It needs to be a number with a decimal point. For $20, instead of 20, use 20.00. Update it in the {filename} file.')
        return False


def check_billing_cycle_days(billing_cycle):
    if type(billing_cycle) is int:
        return True
    else:
        print(f'Days In Billing Cycle "{billing_cycle}" is not valid. It needs to be a whole number without any commas or decimal points. Update it in the {filename} file.')
        return False


# VARIABLES ############################################################################################################
filename = 'Add_Your_Subscription_Info_Here.txt'
save_file = 'ID_And_Code.txt'

website_title = 'Monero Subscription Code Generator:'
website_logo_image = '/static/monerologo.png'

# START PROGRAM ########################################################################################################
app = Flask(__name__)


# The @ makes a "decorator" which lets you wrap a function and modify its behavior
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # getting form data
        custom_label = request.form.get('custom_label')
        sellers_wallet = request.form.get('sellers_wallet')
        currency = request.form.get('currency')
        amount = float(request.form.get('amount'))
        payment_id = request.form.get('paymentid')
        start_date = request.form.get('start_date')
        billing_cycle_days = int(request.form.get('billing_cycle_days'))

        if not payment_id:
            payment_id = make_payment_id()

        #print(payment_id)

        if check_name(custom_label):
            if check_wallet(sellers_wallet):
                if check_currency(currency):
                    if check_amount(amount):
                        if check_start_date(start_date):
                            if check_billing_cycle_days(billing_cycle_days):
                                json_data = {
                                    "custom_label": custom_label,
                                    "sellers_wallet": sellers_wallet,
                                    "currency": currency,
                                    "amount": amount,
                                    "payment_id": payment_id,
                                    "start_date": start_date,
                                    "billing_cycle_days": billing_cycle_days
                                }

                                # process data to create code
                                code = make_monero_subscription_code(json_data)

                                # render template with generated code
                                return render_template('home.html', code=code, payment_id=payment_id)

    # If it's a GET request, just render the template without a code
    return render_template('home.html', code=None)


if __name__ == '__main__':
    app.run(debug=True)
