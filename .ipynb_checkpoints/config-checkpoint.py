import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'

    # Add other configuration settings as needed
    CACHE_TYPE = "SimpleCache"  # Flask-Caching settings
    CACHE_DEFAULT_TIMEOUT = 300


def configure_llm(llm='gemini', version="gemini-2.0-flash"):
    if llm == 'gemini':
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('gemini_api_key'))
        gemini = genai.GenerativeModel(version)
    else:
        raise NameError(f"{llm}:{version} is not supported. Please try a differnt config.")
    