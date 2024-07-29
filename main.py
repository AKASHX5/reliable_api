from flask import Flask, request, jsonify
import httpx
import random
import time
# from utils import create_group, delete_group

from api import app
# BASE_URL = "http//<192.168.10.187>5001"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008,debug=True)
