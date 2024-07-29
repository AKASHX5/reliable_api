from flask import Flask, request, jsonify
import httpx
import random
import time
from utils.utils import create_group, delete_group, exponential_backoff, \
    retry_operation
# from main import BASE_URL
from api import app
import logging

# logging.basicConfig(level=logging.DEBUG)
BASE_URL = "http://localhost:5001"


@app.route('/v1/create_groups', methods=['POST'])
def create_group_api():
    # app.logger.debug("Received request at /v1/create_groups")
    try:
        data = request.json.get("groupId")
        print("data",data)
        if not isinstance(data, str):
            return jsonify({"message": "Invalid groupId"}), 400
    except Exception as e:
        return jsonify({"message": f"Error parsing request: {str(e)}"}), 400

    try:
        node_list = [
            f"{BASE_URL}/v1/group/one",
            f"{BASE_URL}/v1/group/two",
            f"{BASE_URL}/v1/group/three"
        ]

        successful_create = []
        request_data = {"groupId": data}

        for url in node_list:
            try:
                print("url",url)
                print(request_data)
                response = create_group(url, payload=request_data)
                print("dd",response)
                if response.get('status') == 200:
                    successful_create.append(url)
            except Exception as e:
                print(f"Error creating group at {url}: {str(e)}")

        if len(successful_create) == len(node_list):
            return jsonify({"message": "creation completed in all nodes"}), 200
        if len(successful_create) == 0:
            return jsonify({"message": "failed to create in all nodes"}), 400

        for url in successful_create:
            retry_count = 0
            # while retry_count < 3:
            #     try:
            #         response = delete_group(url, request_data)
            #         if response.get('status') == 200:
            #             break
            #     except Exception as e:
            #         print(f"Error deleting group at {url}: {str(e)}")
            #     retry_count += 1
            #     sleep_time = exponential_backoff(retry_count)
            #     time.sleep(sleep_time)
            response = retry_operation(delete_group, 3, url, request_data)
            if response is None or response.get('status') != 200:
                return jsonify(
                    {"message": f"max retry failed for url {url}"}), 500

            if response.get('status') != 200:
                return jsonify(
                    {"message": f"max retry failed for url {url}"}), 500

        return jsonify({"message": "rollback success"}), 500

    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/v1/delete_groups', methods=['DELETE'])
def delete_group_api():
    try:
        data = request.json
        if not isinstance(data, dict):
            return jsonify({"message": "Invalid groupId"}), 400
    except Exception as e:
        return jsonify({"message": f"Error parsing request: {str(e)}"}), 400

    try:
        delete_api = [
            f"{BASE_URL}/v1/group/one",
            f"{BASE_URL}/v1/group/two",
            f"{BASE_URL}/v1/group/three"
        ]

        successful_delete = []

        for url in delete_api:
            print("url",url)
            try:
                response = delete_group(url, data)
                print(response.values())

                if response.get('status') == 200:
                    successful_delete.append(url)
            except Exception as e:
                print(f"Error deleting group at {url}: {str(e)}")

        if len(successful_delete) == len(delete_api):
            return jsonify({"message": "deletion completed in all nodes"}), 200
        if len(successful_delete) == 0:
            return jsonify({"message": "failed to delete in all nodes"}), 400

        for url in successful_delete:
            response = retry_operation(delete_group, 3, url, data)
            if response is None or response.get('status') != 200:
                return jsonify(
                    {"message": f"max retry failed for url {url}"}), 500

            if response.get('status') != 200:
                return jsonify(
                    {"message": f"max retry failed for url {url}"}), 500

        return jsonify({"message": "rollback success"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/healthz', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200
