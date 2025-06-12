import os, requests, sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from config import app, db
# Import API routes
# from api.routes import api_bp

from stock_analysis import get_stock_info
from plots import create_candlestick_chart, create_comparison_chart
from lucerna import Lucerna
from financial_reports import FinancialReportDownloader


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
    try:
        stock_info, stock_price_df = get_stock_info(symbol)
        fig_price = create_candlestick_chart(stock_price_df,
                                             stock_info['company_name'],
                                             stock_info['currency'])
        fig_json = fig_price.to_json()
        return jsonify({**stock_info, "candlestick_json": fig_json})
    except Exception as e:
        print(f"Error fetching stock info for {symbol}: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch stock information. Please try again later.',
            'details': str(e)
        }), 500

@app.route('/api/analyze-company', methods=['POST'])
def analyze_company():
    data = request.get_json()
    company = data.get('company')
    
    # Initialize Lucerna and FinancialReportDownloader
    lucerna = Lucerna('gemini', "gemini-2.5-flash-preview-05-20")
    report_downloader = FinancialReportDownloader()
    
    try:
        # Get financial report
        pdf_path, report_text = report_downloader.get_latest_financial_report(company)
        
        # Prepare the prompt with financial report content
        prompt = f"Analyze the following company: {company}\n\n"
        if report_text:
            prompt += f"Here is the latest financial report content:\n{report_text}\n\n"
            prompt += "Please provide a detailed analysis including:\n"
            prompt += "1. Company Overview\n"
            prompt += "2. Financial Analysis\n"
            prompt += "3. Risk Assessment\n"
        else:
            prompt += "Please provide a general analysis of the company."
        
        # Get analysis from Lucerna
        analysis = lucerna.explain_company(prompt)
        
        # Split the analysis into sections
        sections = {
            'overview': '',
            'financials': '',
            'risks': ''
        }
        
        # Simple parsing of the analysis text into sections
        current_section = 'overview'
        for line in analysis.split('\n'):
            line = line.strip()
            if line.lower().startswith('financial'):
                current_section = 'financials'
            elif line.lower().startswith('risk'):
                current_section = 'risks'
            elif line:
                sections[current_section] += line + '\n'
        
        return jsonify({
            'analysis': sections,
            'has_financial_report': bool(report_text)
        })
    
    finally:
        # Clean up temporary files
        report_downloader.cleanup()

if __name__ == '__main__':
    print(f"python version : {sys.version}")
    with app.app_context():
        db.create_all()
    app.run(debug=False)