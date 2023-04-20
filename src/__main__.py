"""
This script starts the dash application.

Author: Jonas Schrage
Date: 16.04.2023

"""
from src.index import app

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
