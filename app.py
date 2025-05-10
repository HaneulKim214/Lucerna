import os, sys
from flask import Flask, render_template
from flask_cors import CORS
from dotenv import load_dotenv

from config import app, db
# Import API routes
# from api.routes import api_bp

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

@app.route('/portfolio')
def portfolio():
    """Render the portfolio management page."""
    print("Hello world")
    return render_template('index_2.html',
                           active_tab='portfolio')



if __name__ == '__main__':
    print(f"python version : {sys.version}")
    with app.app_context():
        db.create_all()
    app.run(debug=True)