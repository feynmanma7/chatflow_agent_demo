from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route("/recommend/category", methods=["POST"])
def recommend_customer():

    req = request.json

    manager_id = req.get("manager_id")
    product_category = req.get("product_category")

    customers = []

    for i in range(10):
        customers.append({
            "customer_id": f"C{10000+i}",
            "customer_name": f"客户{i+1}",
            "score": round(random.uniform(0.7, 0.99), 4)
        })

    '''
    return jsonify({
        "code": 0,
        "msg": "success",
        "data": {
            "manager_id": manager_id,
            "product_category": product_category,
            "customer_list": customers
        }
    })
    '''

    return jsonify({
        "code": 0,
        "msg": "success",
        "data": {
            "manager_id": manager_id,
            "product_category": product_category,
            "customer_list": customers
        }
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )

    