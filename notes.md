
PS C:\Users\krist\OneDrive\namskeid_hr\H25\HONN\Project_2> docker compose up [+] Running 2/2r Desktop o View Config w Enable Watch ✔ Network project_2_default Created 0.1s ✔ Container project_2-buyer-service-1 Created 0.2s Attaching to buyer-service-1 buyer-service-1 | Usage: flask [OPTIONS] COMMAND [ARGS]... buyer-service-1 | Try 'flask --help' for help. buyer-service-1 | buyer-service-1 | Error: No such option: -a buyer-service-1 exited with code 2

Solution:

# `BuyerService/Dockerfile`
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Tell Flask which app to load and bind to all interfaces
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000

EXPOSE 8000
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]

# `docker-compose.yml` (service snippet)
services:
  buyer-service:
    build: ./BuyerService
    ports:
      - "8000:8000"
    environment:
      - FLASK_APP=app
      - FLASK_RUN_HOST=0.0.0.0
      - FLASK_RUN_PORT=8000
    # override CMD if needed (avoid using `-a`)
    command: flask run --host=0.0.0.0 --port=8000






buyer-service-1  | Traceback (most recent call last):
buyer-service-1  |   File "/usr/local/lib/python3.9/site-packages/flask/cli.py", line 245, in locate_app
buyer-service-1  |     __import__(module_name)
buyer-service-1  |   File "/app/app.py", line 2, in <module>
buyer-service-1  |     from BuyerService.endpoints.buyer_endpoints import buyer_blueprint
buyer-service-1  | ModuleNotFoundError: No module named 'BuyerService'


Solution:



--------

BuyerService.repository.enums.buyer import Buyer ModuleNotFoundError: No module named 'BuyerService</module></module>


Cause: Python can't find the BuyerService package because either BuyerService is not a package (no __init__.py) or you're running app.py directly from inside the BuyerService folder (which breaks absolute imports). Also you have duplicate app.py files which can confuse which module is used.


--------

  File "C:\Users\krist\OneDrive\namskeid_hr\H25\HONN\Project_2\BuyerService\repository\buyer_repository.py", line 38, in create_buyer
    cursor.execute(
sqlite3.OperationalError: database is locked

Solution: Delete the db file


-------

depends_on in docker-compose.yml only ensures that the buyer-service-db container is started before buyer-service, but it does not wait for the database to be ready to accept connections. The database may still be initializing when your service tries to connect.

--------

Error: Could not import 'MerchantService.app'.

ath stafsetningu

---------



PS C:\Users\krist\OneDrive\namskeid_hr\H25\HONN\Project_2\PaymentService> python .\producer.py                                                
Traceback (most recent call last):
  File "C:\Users\krist\OneDrive\namskeid_hr\H25\HONN\Project_2\PaymentService\producer.py", line 5, in <module>
    connection = pika.BlockingConnection(
                 ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\krist\AppData\Local\Programs\Python\Python312\Lib\site-packages\pika\adapters\blocking_connection.py", line 360, in __init__
    self._impl = self._create_connection(parameters, _impl_class)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\krist\AppData\Local\Programs\Python\Python312\Lib\site-packages\pika\adapters\blocking_connection.py", line 451, in _create_connection
    raise self._reap_last_connection_workflow_error(error)
pika.exceptions.IncompatibleProtocolError: StreamLostError: ('Transport indicated EOF',)


Rabbit MQ's default post is 15672 and 5672, which are reserved ports on Widows. If you run MQ with default port you'll
get this error:

(HTTP code 500) server error - ports are not available: exposing port TCP 0.0.0.0:5672 -> 127.0.0.1:0: listen tcp 0.0.0.0:5672: bind: An attempt was made to access a socket in a way forbidden by its access permissions.

Workaround:

Specify which port Rabbit should try to use in the producer:
```py
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=7654))
```

```docker
    ports:
      - "8080:15672"
      - "7654:5672"
```

--------------

in Python, it matters in which order you define classes (in terms of reference)

------------

PS C:\Users\krist\OneDrive\namskeid_hr\H25\HONN\Project_2> httpx --version         
Usage: httpx [OPTIONS] URL

Error: No such option: --version (Possible options: --json, --no-verify, --verbose)

Solution:

PS C:\Users\krist\OneDrive\namskeid_hr\H25\HONN\Project_2> python -c "import httpx; print(httpx.__version__)"
0.28.1

_-----------


card_number = "1789"
        
        for i in range(len(card_number)-4):
            c = card_number[i]
            card_number.replace(c, '*', 1)


-----------------------



return jsonify(new_product), 200 inventory-service     |            ^^^^^^^^^^^^^^^^^^^^   

TypeError: '<' not supported between instances of 'Product' and 'Product'

The error indicates that the Product enum is being used in a way that involves comparison (e.g., sorting or equality checks), which is not directly supported between enum members unless explicitly defined.
To fix this, ensure that you are accessing the value of the Product enum members when using them in operations like dictionary keys or comparisons. Update the create_product method to use Product.<ENUM_MEMBER>.value consistently when constructing the new_product dictionary.

      new_product = {
          Product.MERCHANT_ID: row[Product.MERCHANT_ID.value],
          Product.PRODUCT_NAME: row[Product.PRODUCT_NAME.value],
          Product.PRICE: row[Product.PRICE.value],
          Product.QUANTITY: row[Product.QUANTITY.value]
      }


---------------

Náði ekki að tengjast buyer-db með þetta port mapping: "5432:5432"


--------------------

why does curl -v http://host.docker.internal:8002/api/buyers/1 work but not curl -v http://buyer-service:8002/api/buyers/1

Because buyer-service is a Docker Compose service name that Docker’s internal DNS resolves only inside the Compose network (between containers). From your host shell that name does not resolve, so the request fails. host.docker.internal / localhost work from the host because the service’s port is published to the host network.
```bash
docker compose ps
# or
docker ps
```

if the port is published (e.g. 0.0.0.0:8002->8002/tcp) call from host:
```bash
curl -v http://localhost:8002/api/buyers/1
# or
curl -v http://127.0.0.1:8002/api/buyers/1
```

If the port is NOT published and you want to call the service by name, run curl from another container on the same network:
```bash
docker run --rm --network $(docker compose ps -q | xargs docker inspect --format '{{index .NetworkSettings.Networks}}' 2>/dev/null | sed -n '1p' | sed -e 's/.*"Name":\s*"\([^"]*\)".*/\1/') curlimages/curl -v http://buyer-service:8002/api/buyers/1
```

(or simpler if you know the network name:)
```bash
docker run --rm --network project_2_default curlimages/curl -v http://buyer-service:8002/api/buyers/1
```

-----------------

order-service-rabbitmq  | 2025-10-31 13:07:21.838581+00:00 [error] <0.679.0> closing AMQP connection <0.679.0> (172.19.0.1:33174 -> 172.19.0.6:5672, duration: '5M, 0s'):
order-service-rabbitmq  | 2025-10-31 13:07:21.838581+00:00 [error] <0.679.0> missed heartbeats from client, timeout: 60s

python consumer.py
order-service-rabbitmq  | 2025-10-31 13:22:14.953499+00:00 [error] <0.1346.0> operation queue.declare caused a channel exception resource_locked: cannot obtain exclusive access to locked queue 'payment-service-queue' in vhost '/'. It could be originally declared on another connection or the exclusive property value does not match that of the original declaration.


------------------

order-service-rabbitmq  | 2025-10-31 13:39:06.840013+00:00 [info] <0.493.0> Resetting node maintenance status
payment-service         | Traceback (most recent call last):
payment-service         |   File "/app/PaymentService/./consumer.py", line 6, in <module>
payment-service         |     connection = pika.BlockingConnection(
payment-service         |                  ^^^^^^^^^^^^^^^^^^^^^^^^
payment-service         |   File "/usr/local/lib/python3.12/site-packages/pika/adapters/blocking_connection.py", line 360, in __init__
payment-service         |     self._impl = self._create_connection(parameters, _impl_class)
payment-service         |                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
payment-service         |   File "/usr/local/lib/python3.12/site-packages/pika/adapters/blocking_connection.py", line 451, in _create_connection
payment-service         |     raise self._reap_last_connection_workflow_error(error)
payment-service         | pika.exceptions.IncompatibleProtocolError: StreamLostError: ('Transport indicated EOF',)
order-service-rabbitmq  | 2025-10-31 13:39:08.011958+00:00 [warning] <0.515.0> Deprecated features: `management_metrics_collection`: Feature `management_metrics_collection` is deprecated.



--------------



order-service-rabbitmq  | 2025-10-31 13:40:48.736034+00:00 [warning] <0.637.0>     "deprecated_features.permit.management_metrics_collection = true"
order-service           |     return ctx.invoke(self.callback, **ctx.params)
order-service-rabbitmq  | 2025-10-31 13:40:48.736034+00:00 [warning] <0.637.0> To test RabbitMQ as if the feature was removed, set this in your configuration:




order-service           |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


order-service-rabbitmq  | 2025-10-31 13:40:48.736034+00:00 [warning] <0.637.0>     "deprecated_features.permit.management_metrics_collection = false"
order-service           |   File "/usr/local/lib/python3.12/site-packages/click/core.py", line 814, in invoke


order-service-rabbitmq  | 2025-10-31 13:40:49.025397+00:00 [info] <0.673.0> Management plugin: HTTP (non-TLS) listener started on port 15672


order-service           |     return callback(*args, **kwargs)
order-service-rabbitmq  | 2025-10-31 13:40:49.026703+00:00 [info] <0.701.0> Statistics database started.
order-service-rabbitmq  | 2025-10-31 13:40:49.027288+00:00 [info] <0.700.0> Starting worker pool 'management_worker_pool' with 3 processes in it
order-service           |   File "/usr/local/lib/python3.12/site-packages/click/decorators.py", line 93, in new_func
order-service-rabbitmq  | 2025-10-31 13:40:49.122533+00:00 [info] <0.712.0> Prometheus metrics: HTTP (non-TLS) listener started on port 15692



order-service           |     return ctx.invoke(f, obj, *args, **kwargs)
order-service-rabbitmq  | 2025-10-31 13:40:49.124204+00:00 [info] <0.615.0> Ready to start client connection listeners
order-service-rabbitmq  | 2025-10-31 13:40:49.146414+00:00 [info] <0.756.0> started TCP listener on [::]:5672
order-service           |     return callback(*args, **kwargs)
order-service           |            ^^^^^^^^^^^^^^^^^^^^^^^^^
order-service           |   File "/usr/local/lib/python3.12/site-packages/flask/cli.py", line 979, in run_command
order-service           |     raise e from None
order-service           |   File "/usr/local/lib/python3.12/site-packages/flask/cli.py", line 963, in run_command
order-service           |     app: WSGIApplication = info.load_app()  # pyright: ignore
order-service           |                            ^^^^^^^^^^^^^^^
order-service           |   File "/usr/local/lib/python3.12/site-packages/flask/cli.py", line 349, in load_app
order-service           |     app = locate_app(import_name, name)
order-service           |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
order-service           |   File "/usr/local/lib/python3.12/site-packages/flask/cli.py", line 245, in locate_app
order-service           |     __import__(module_name)
order-service           |   File "/app/OrderService/app.py", line 2, in <module>
order-service           |     from OrderService.endpoints.order_endpoints import order_blueprint
order-service           |   File "/app/OrderService/endpoints/order_endpoints.py", line 21, in <module>
order-service           |     order_service = OrderService(order_repository, InventoryClient(), Exchange())
order-service           |                                                                       ^^^^^^^^^^
order-service           |   File "/app/OrderService/messaging/exchange.py", line 7, in __init__
order-service           |     connection = pika.BlockingConnection(
order-service           |                  ^^^^^^^^^^^^^^^^^^^^^^^^
order-service           |   File "/usr/local/lib/python3.12/site-packages/pika/adapters/blocking_connection.py", line 360, in __init__
order-service           |     self._impl = self._create_connection(parameters, _impl_class)
order-service           |                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
order-service           |   File "/usr/local/lib/python3.12/site-packages/pika/adapters/blocking_connection.py", line 451, in _create_connection
order-service           |     raise self._reap_last_connection_workflow_error(error)
order-service           | pika.exceptions.IncompatibleProtocolError: StreamLostError: ('Transport indicated EOF',)
order-service exited with code 1

----------------------


payment-service         | pika.exceptions.IncompatibleProtocolError: StreamLostError: ('Transport indicated EOF',)
line 6 in consumer.py

So the mq servic is not ready before they try to connect i think


----------

order-service-rabbitmq  | 2025-10-31 14:27:50.139173+00:00 [info] <0.764.0> accepting AMQP connection 172.19.0.1:42818 -> 172.19.0.6:5672
order-service-rabbitmq  | 2025-10-31 14:27:50.139668+00:00 [error] <0.764.0> closing AMQP connection 172.19.0.1:42818 -> 172.19.0.6:5672 (duration: '3ms'):
order-service-rabbitmq  | 2025-10-31 14:27:50.139668+00:00 [error] <0.764.0> HTTP GET request detected on AMQP port. Ensure the client is connecting to the correct port.
order-service-rabbitmq  | 2025-10-31 14:27:59.425576+00:00 [info] <0.775.0> accepting AMQP connection 172.19.0.1:59432 -> 172.19.0.6:5672
order-service-rabbitmq  | 2025-10-31 14:27:59.426034+00:00 [error] <0.775.0> closing AMQP connection 172.19.0.1:59432 -> 172.19.0.6:5672 (duration: '4ms'):
order-service-rabbitmq  | 2025-10-31 14:27:59.426034+00:00 [error] <0.775.0> HTTP GET request detected on AMQP port. Ensure the client is connecting to the correct port.
order-service-rabbitmq  | 2025-10-31 14:28:03.779124+00:00 [info] <0.783.0> accepting AMQP connection 172.19.0.1:59436 -> 172.19.0.6:5672
order-service-rabbitmq  | 2025-10-31 14:28:03.779933+00:00 [error] <0.783.0> closing AMQP connection 172.19.0.1:59436 -> 172.19.0.6:5672 (duration: '2ms'):
order-service-rabbitmq  | 2025-10-31 14:28:03.779933+00:00 [error] <0.783.0> HTTP GET request detected on AMQP port. Ensure the client is connecting to the correct port.


The issue is that the health check is using curl to send an HTTP GET request to the RabbitMQ AMQP port (5672). However, the AMQP port is not designed to handle HTTP requests, which is why RabbitMQ logs the error: "HTTP GET request detected on AMQP port".
To fix this, you should use a proper AMQP health check instead of curl. Replace the health check command with one that uses rabbitmq-diagnostics or another tool that can properly interact with the AMQP protocol.

test: ["CMD-SHELL", "rabbitmq-diagnostics -q ping && curl -s host.docker.internal:7654 > /dev/null || exit 1"]


-------------


test: ["CMD-SHELL", "rabbitmq-diagnostics -q ping && rabbitmq-diagnostics -q check_port_listener 5672 || exit 1"]


order-service-rabbitmq | 2025-10-31 16:15:05.163720+00:00 [info] <0.10.0> Time to start RabbitMQ: 25414 ms dependency failed to start: container order-service-rabbitmq is unhealthy


docker exec -it order-service-rabbitmq rabbitmq-diagnostics -q ping
docker exec -it order-service-rabbitmq rabbitmq-diagnostics -q check_port_listener 5672
echo $?


Both diagnostics succeed manually, so RabbitMQ itself is healthy. The issue is the healthcheck shell syntax inside Docker Compose.
When Docker runs the CMD-SHELL array, it doesn’t execute it as a full interactive shell with parentheses grouping; exit codes can be lost. Simplify and harden the healthcheck:


healthcheck:
  test: ["CMD", "bash", "-c", "rabbitmq-diagnostics -q ping && rabbitmq-diagnostics -q check_port_listener 5672"]
  interval: 5s
  timeout: 5s
  retries: 20
  start_period: 30s

or, if you want to stay with CMD-SHELL:

healthcheck:
  test: ["CMD-SHELL", "rabbitmq-diagnostics -q ping && rabbitmq-diagnostics -q check_port_listener 5672"]
  interval: 5s
  timeout: 5s
  retries: 20
  start_period: 30s


---------

after a while i get:

order-service-rabbitmq  | 2025-10-31 16:24:38.287738+00:00 [error] <0.684.0> closing AMQP connection <0.684.0> (172.18.0.1:38254 -> 172.18.0.5:5672, duration: '3M, 4s'):
order-service-rabbitmq  | 2025-10-31 16:24:38.287738+00:00 [error] <0.684.0> missed heartbeats from client, timeout: 60s

Solution pika.ConnectionParameters(host='host.docker.internal', port=7654, heartbeat=30))


---------------

# python InventoryService/messaging/consumer.py
Traceback (most recent call last):
  File "/app/InventoryService/messaging/consumer.py", line 4, in <module>
    from InventoryService.repositories.product_repository import ProductRepository
ModuleNotFoundError: No module named 'InventoryService'
# python -m InventoryService.messaging.consumer
 [*] Waiting for logs. To exit press CTRL+C

```bash
```







docker builder prune --all -f
docker volume prune -f
docker system prune -a
docker-compose up --build


Delete all entries from buyer-db:

```bash
docker exec -it merchant-service-db psql -U postgres -d Merchants -c "TRUNCATE TABLE Merchants RESTART IDENTITY CASCADE;"
docker exec -it buyer-service-db psql -U postgres -d Buyers -c "TRUNCATE TABLE buyers RESTART IDENTITY CASCADE;"
docker exec -it inventory-service-db psql -U postgres -d Inventory -c "TRUNCATE TABLE products RESTART IDENTITY CASCADE;"
docker exec -it payment-service-db psql -U postgres -d Payments -c "TRUNCATE TABLE payments RESTART IDENTITY CASCADE;"
```
Drop table
```bash
docker exec -it buyer-services-db psql -U postgres -d Buyers -c "DROP TABLE buyers;"
docker exec -it merchant-services-db psql -U postgres -d Merchants -c "DROP TABLE merchants;"
docker exec -it inventory-services-db psql -U postgres -d Inventory -c "DROP TABLE products;"
docker exec -it order-services-db psql -U postgres -d Orders -c "DROP TABLE orders;"
```

```bash
curl -v http://127.0.0.1:8002/api/buyers/1 # does not work
curl -v http://0.0.0.0:8002/api/buyers/1 # does not work
curl -v http://buyer-service:8002/api/buyers/1 # does not work
curl -v http://host.docker.internal:8002/api/buyers/1 # works
curl -v http://host.docker.internal:8001/api/merchants/1 # works

curl -v http://host.docker.internal:7654 > /dev/null || exit 1
curl -v host.docker.internal:7654 > /dev/null || exit 1
curl -v http://host.docker.internal:76542 > /dev/null || exit 1
curl -s http://host.docker.internal:7654 > /dev/null || exit 1

nc -z host.docker.internal 7654 || exit 1
nc host.docker.internal 7654 || exit 1
rabbitmq-diagnostics -q check_port_listener 5672 || exit 1

python3 -c "import pika; pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672)).close()" || exit 1


docker exec -it email-service env | grep SENDGRID_API_KEY

```




EmailService
The Email body should say "Order {order id} has been successfully purchased" (exchange {order
id} for the actual order id)



{
    "productId": 123,
    "merchantId": 123,
    "buyerId": 123,
    "creditCard": {
        "cardNumber": "12341234123412341234",
        "expirationMonth": 8,
        "expirationYear": 2025,
        "cvc": 123
    },
    "discount": 0.2 
}


["CMD-SHELL", "rabbitmq-diagnostics -q ping || exit 1"]

test: ["CMD-SHELL", "rabbitmq-diagnostics -q ping && nc -z localhost 5672 || exit 1"]

test: ["CMD-SHELL", "rabbitmq-diagnostics -q ping && curl -s host.docker.internal:7654 > /dev/null || exit 1"]

test: ["CMD-SHELL", "rabbitmq-diagnostics -q ping && rabbitmq-diagnostics -q check_port_listener 5672 || exit 1"]

RUN apt-get update && apt install -y netcat

apt-get update && apt install -y netcat-openbsd

apt-get update && apt-get install -y python3 python3-pip && pip3 install pika --break-system-packages
apt install -y python3 python3-pip && pip3 install pika

pip install pika --break-system-packages

        html_content=f"""
            <strong>Order Details:</strong><br>
            Order ID: {order['id']}<br>
            Product Name: {order['product_name']}<br>
            Price: {order['total_price']} V-Bucks<br>
            """


    card_number = "1234567"
    new_card_number = card_number
    for i in range(len(card_number) - 4):
        c = card_number[i]
        new_card_number.replace(c, '*', 1)
    print(new_card_number)

class BuyerClient:
    # def __init__(self, base_url='http://host.docker.internal:8002', timeout=5.0):