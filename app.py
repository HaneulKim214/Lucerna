import os, requests, sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from config import app, db
# Import API routes
# from api.routes import api_bp

from stock_analysis import get_stock_info
from plots import create_candlestick_chart, create_comparison_chart


@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    """Render the portfolio management page."""
    print("Hello world")
    return render_template('index_2.html',
                           active_tab='portfolio')

@app.route('/api/analyze-company', methods=['POST'])
def analyze_company():
    data = request.get_json()
    company = data.get('company')
    lucerna = Lucerna('openai', "o4-mini")
    analysis = lucerna.explain_company(company)
    return jsonify({'analysis': analysis})

@app.route('/api/stock-search')
def stock_search():
    query = request.args.get('q')
    if not query:
        return jsonify({'quotes': []})
    # Sets a fake browser User-Agent string.
    # Some public APIs (like Yahoo's) block or limit access from non-browser clients 
    # (like Python scripts).
    url = f'https://query2.finance.yahoo.com/v1/finance/search?q={query}'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": query, "quotes_count": 1, "country": "United States"}
    
    resp = requests.get(url=url, params=params, headers={'User-Agent': user_agent})
    return resp.json()

@app.route('/api/stock-info')
def stock_info():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({'error': 'No symbol provided'}), 400
    stock_info = get_stock_info(symbol)
    fig_price = create_candlestick_chart(stock_info['stock_price_df'],
                                         stock_info['company_name'],
                                         stock_info['currency'])
    fig_json = fig_price.to_json()
    return jsonify({**stock_info, "candlestick_json": fig_json})


if __name__ == '__main__':
    print(f"python version : {sys.version}")
    with app.app_context():
        db.create_all()
    app.run(debug=True)