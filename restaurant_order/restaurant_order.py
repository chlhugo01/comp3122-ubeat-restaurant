import datetime
import flask
import json
import pymongo
import redis

##############################
# Init library / connections
#######3######################
flask_app = flask.Flask(__name__)
mongo_client = pymongo.MongoClient('mongodb://comp3122:23456@restaurant_order_db:27017')
redis_conn = redis.Redis(host='message_queue', port=6379)

################
# Redis events
################


def new_order(message):
    load = json.loads(message['data'])
    order_id = load['order_id']
    restaurant_id = load['restaurant_id']
    food_id = load['food_id']
    user_id = load['user_id']
    orderresult = mongo_client.restaurant_orders.Order.find_one({"restaurant_id": int(restaurant_id)})
    query = {"_id" : orderresult["_id"] }
    orderresult["order"].append({'order_id':order_id, 'customer_id': user_id,'food_id':food_id,'prepare':0,'deliver':0})
    mongo_client.restaurant_orders.Order.replace_one( query, orderresult )
    #orderresult = mongo_client.restaurant_orders.Order.find()

def set_prepared(message):
    load = json.loads(message['data'])
    order_id = load['order_id']
    prepare = load['prepared']
    orders = mongo_client.restaurant_orders.Order.find_one({'order.order_id': order_id})
    for order in orders["order"]:
        if order['order_id'] == order_id:
            order["prepare"] = 1
            break
    mongo_client.restaurant_orders.Order.replace_one({'_id': orders['_id']}, orders)

def set_shipped(message):
    load = json.loads(message['data'])
    order_id = load['order_id']
    delivery_id = load['delivery_id']
    orders = mongo_client.restaurant_orders.Order.find_one({'order.order_id': order_id})
    for order in orders["order"]:
        if order['order_id'] == order_id:
            order['deliver'] = delivery_id
            break
    mongo_client.restaurant_orders.Order.replace_one({'_id': orders['_id']}, orders)

###################
# Flask endpoints
###################

@flask_app.route('/restaurant/<restaurant_id>', methods=['GET'])
def get_a_restaurant(restaurant_id):
    db = mongo_client.restaurant_orders.Order
    result = list(db.find({'restaurant_id': int(restaurant_id)}, {'_id': 0}))
    return flask.jsonify(result)

@flask_app.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    orders = mongo_client.restaurant_orders.Order \
        .find_one({'order.order_id': order_id}, { '_id': 0})
    if not orders:
         return {'error': 'not found'}, 404
    restaurant_id = orders['restaurant_id']
    orders = orders['order']
    for order in orders:
        if order['order_id'] == order_id:
            o = order
            o['restaurant_id'] = restaurant_id
            return o, 200

##############################
# Main: Run flask, establish subscription
#######3######################
if __name__ == '__main__':
    redis_pubsub = redis_conn.pubsub()
    redis_pubsub.subscribe(**{'restaurantOrder_newOrder': new_order})
    redis_pubsub.subscribe(**{'restaurantOrder_setPrepared': set_prepared})
    redis_pubsub.subscribe(**{'restaurantOrder_setShipped': set_shipped})
    redis_pubsub_thread = redis_pubsub.run_in_thread(sleep_time=0.001)
    flask_app.run(host='0.0.0.0', debug=True, port=15000)
