# # pip install --upgrade stripe

import stripe

# # Set your secret key. Remember to switch to your live secret key in production.
# # See your keys here: https://dashboard.stripe.com/account/apikeys
# stripe.api_key = "sk_test_51Ic2aYBtLnY99CpgJ3aPRLX3Q4CZlbs1ynD3YiD01tsftKK9k2ePHhADz5rkLDt5RRAXHjZph5QxTsBV4dwu34r000V6Harpq6"

# intent = stripe.PaymentIntent.create(
#     amount=2,
#     currency='sgd',
#     # Verify your integration in this guide by including this parameter
#     metadata={'integration_check': 'accept_a_payment'},
# )

# from flask import Flask, jsonify
# app = Flask(__name__)

# @app.route('/checkout')
# def checkout():
#   intent = # ... Fetch or create the PaymentIntent
#   return render_template('checkout.html', client_secret=intent.client_secret)

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = "sk_test_51Ic2aYBtLnY99CpgJ3aPRLX3Q4CZlbs1ynD3YiD01tsftKK9k2ePHhADz5rkLDt5RRAXHjZph5QxTsBV4dwu34r000V6Harpq6"

stripe.PaymentIntent.create(
  amount=1000,
  currency='sgd',
  payment_method_types=['card'],
  receipt_email='jenny.rosen@example.com',
)