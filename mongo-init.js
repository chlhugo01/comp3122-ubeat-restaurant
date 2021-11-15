db.auth('comp3122', '23456')
db = db.getSiblingDB('restaurant_orders')

db.createCollection('Order')
db.Order.insertOne({
    'restaurant_id':1,
    'name': 'Hong Kong Happy Dim Sum',
    'order':[
        {'order_id':'r1o1', 'customer_id':1, 'food_id':1, 'prepare':1,'deliver':1},
        {'order_id':'r1o2', 'customer_id':3, 'food_id':1, 'prepare':1,'deliver':3},
        {'order_id':'r1o3', 'customer_id':2, 'food_id':2, 'prepare':0,'deliver':0}
    ]
})
db.Order.insertOne({
    'restaurant_id':2,
    'name': 'Hong Kong Happy Meal',
    'order':[
        {'order_id':'r2o1', 'customer_id':1, 'food_id':3, 'prepare':1, 'deliver':3},
        {'order_id':'r2o2', 'customer_id':2, 'food_id':2, 'prepare':1, 'deliver':1},
        {'order_id':'r2o3', 'customer_id':1, 'food_id':3, 'prepare':0, 'deliver':0}
    ]
})
db.Order.insertOne({
    'restaurant_id':3,
    'name': 'Hong Kong Happy Restaurant',
    'order':[
        {'order_id':'r3o1', 'customer_id':2, 'food_id':3, 'prepare':1,'deliver':2},
        {'order_id':'r3o2', 'customer_id':3, 'food_id':2, 'prepare':1,'deliver':2},
        {'order_id':'r3o3', 'customer_id':3, 'food_id':3, 'prepare':0,'deliver':0}
    ]
})