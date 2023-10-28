import os
import gzip
import json
import base64
import random
from datetime import datetime
import monerorequest
from flask import Flask, request, render_template


# VARIABLES ############################################################################################################
website_title = 'Monero Payment Request Generator'
website_logo_image = '/static/monerologo.png'

# START PROGRAM ########################################################################################################
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # getting form data
        custom_label = request.form.get('custom_label')
        sellers_wallet = request.form.get('sellers_wallet')
        currency = request.form.get('currency')
        amount = request.form.get('amount')
        payment_id = request.form.get('paymentid')

        start_date = request.form.get('start_date')
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        start_date = monerorequest.convert_datetime_object_to_truncated_RFC3339_timestamp_format(datetime_object=start_date)

        days_per_billing_cycle = int(request.form.get('days_per_billing_cycle'))
        number_of_payments = int(request.form.get('number_of_payments'))
        change_indicator_url = request.form.get('change_indicator_url')

        if not payment_id:
            payment_id = monerorequest.make_random_payment_id()

        # process data to create code
        code = monerorequest.make_monero_payment_request(
            custom_label=custom_label,
            sellers_wallet=sellers_wallet,
            currency=currency,
            amount=amount,
            payment_id=payment_id,
            start_date=start_date,
            days_per_billing_cycle=days_per_billing_cycle,
            number_of_payments=number_of_payments,
            change_indicator_url=change_indicator_url)

        # render template with generated code
        return render_template('home.html', website_title=website_title, website_logo_image=website_logo_image, code=code, payment_id=payment_id)

    # If it's a GET request, just render the template without a code
    return render_template('home.html', website_title=website_title, website_logo_image=website_logo_image, code=None)


if __name__ == '__main__':
    app.run(debug=True)
