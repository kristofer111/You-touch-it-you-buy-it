from flask import Flask
from MerchantService.endpoints.merchant_endpoints import merchant_blueprint

app = Flask(__name__)

app.register_blueprint(merchant_blueprint)


# Ignored by flask CLI
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)



