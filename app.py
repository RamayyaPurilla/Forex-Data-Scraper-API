from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from database import get_db_connection
from flasgger import Swagger
import sqlite3

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/api/forex-data', methods=['POST'])
def get_forex_data():
    """
    Get Forex Data
    ---
    parameters:
      - name: from
        in: query
        type: string
        required: true
        description: The source currency
      - name: to
        in: query
        type: string
        required: true
        description: The target currency
      - name: period
        in: query
        type: string
        required: true
        description: The time period (1W, 1M, 3M, 6M, 1Y)
    responses:
      200:
        description: A list of forex rates
        schema:
          type: array
          items:
            type: object
            properties:
              date:
                type: string
                description: The date of the rate
              rate:
                type: number
                description: The exchange rate
      400:
        description: Missing or invalid parameters
    """
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    period = request.args.get('period')

    if not all([from_currency, to_currency, period]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Calculate date range based on period
    end_date = datetime.now()
    if period == '1W':
        start_date = end_date - timedelta(weeks=1)
    elif period == '1M':
        start_date = end_date - timedelta(days=30)
    elif period == '3M':
        start_date = end_date - timedelta(days=90)
    elif period == '6M':
        start_date = end_date - timedelta(days=180)
    elif period == '1Y':
        start_date = end_date - timedelta(days=365)
    else:
        return jsonify({"error": "Invalid period"}), 400

    # Query the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, rate FROM forex_rates
        WHERE from_currency = ? AND to_currency = ?
        AND date BETWEEN ? AND ?
        ORDER BY date
    """, (from_currency, to_currency, start_date.date(), end_date.date()))
    
    data = [{"date": row[0], "rate": row[1]} for row in cursor.fetchall()]
    conn.close()

    return jsonify(data)

@app.route('/api/all-data', methods=['GET'])
def get_all_data():
    """
    Get All Forex Data
    ---
    responses:
      200:
        description: A list of all forex rates
        schema:
          type: array
          items:
            type: object
            properties:
              from_currency:
                type: string
                description: The source currency
              to_currency:
                type: string
                description: The target currency
              date:
                type: string
                description: The date of the rate
              rate:
                type: number
                description: The exchange rate
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT from_currency, to_currency, date, rate 
        FROM forex_rates 
        ORDER BY from_currency, to_currency, date
    """)
    
    data = [
        {
            "from_currency": row[0],
            "to_currency": row[1],
            "date": row[2],
            "rate": row[3]
        } for row in cursor.fetchall()
    ]
    conn.close()

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
