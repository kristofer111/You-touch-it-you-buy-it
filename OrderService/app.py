from flask import Flask
from OrderService.endpoints.order_endpoints import order_blueprint

app = Flask(__name__)

app.register_blueprint(order_blueprint)


# Ignored by flask CLI
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)



