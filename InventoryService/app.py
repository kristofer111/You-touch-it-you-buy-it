from flask import Flask
from InventoryService.endpoints.product_endpoints import product_blueprint

app = Flask(__name__)

app.register_blueprint(product_blueprint)


# Ignored by flask CLI
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)



