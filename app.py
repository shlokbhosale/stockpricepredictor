from flask import Flask, request, jsonify
import requests
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stock_db"
)
cursor = db.cursor()

@app.route("/stock/<symbol>", methods=['GET'])
def get_stock_price(symbol):
    api_key = "2TQAPE50X09Q6XI"
    api_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    response = requests.get(api_url)
    data = response.json()

    if "Global Quote" in data:
        stock_price = data["Global Quote"].get("05. price", "N/A")
        query = "INSERT INTO stocks(symbol, price) VALUES (%s, %s)"
        values = (symbol, stock_price)
        cursor.execute(query, values)
        db.commit()
        return jsonify({"symbol": symbol, "price": stock_price})
    else:
        return jsonify({"error": "Invalid stock symbol or API limit reached"}), 400

if __name__ == "__main__":
    app.run(debug=True)