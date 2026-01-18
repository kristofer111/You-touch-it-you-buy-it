from flask import Flask
from BuyerService.endpoints.buyer_endpoints import buyer_blueprint

app = Flask(__name__)

app.register_blueprint(buyer_blueprint)


# Ignored by flask CLI
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)



