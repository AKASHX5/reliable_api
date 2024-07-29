from flask import Flask

app = Flask(__name__)

# Import the routes to register them with the app
from api import api_handler