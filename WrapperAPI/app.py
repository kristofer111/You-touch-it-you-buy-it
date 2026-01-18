from flask import Flask
from WrapperAPI.endpoints.merchant_endpoints import merchant_blueprint
from WrapperAPI.endpoints.buyer_endpoints import buyer_blueprint
from WrapperAPI.endpoints.product_endpoints import product_blueprint
from WrapperAPI.endpoints.order_endpoints import order_blueprint

app = Flask(__name__)

app.register_blueprint(merchant_blueprint, url_prefix='/api')
app.register_blueprint(buyer_blueprint, url_prefix='/api')
app.register_blueprint(product_blueprint, url_prefix='/api')
app.register_blueprint(order_blueprint, url_prefix='/api')


# Ignored by flask CLI
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)



