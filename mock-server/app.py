from flask import Flask,jsonify,request
import json

app = Flask(__name__)

with open('data/customers.json') as f:
    customers=json.load(f)

@app.route('/api/customers')
def get_customers():
    page= int(request.args.get('page',1))
    limit= int(request.args.get('limit',10))
    
    start=(page-1)*limit
    end=start+limit

    return jsonify({
        "data":customers[start:end],
        "total":len(customers),
        "page":page,
        "limit":limit
    })

@app.route('/api/customers/<id>')
def get_customer(id):
    for c in customers:
        if c["customer_id"]==id:
            return jsonify(c)
    return jsonify({"error": "Not found"}),404

@app.route('/api/health')
def health():
    return {"status": "ok"}
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)