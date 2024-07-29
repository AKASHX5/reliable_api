from flask import request, jsonify
import httpx, random
import json
import logging, time



def get_group(group_id,url):
    response = httpx.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def create_group(url, payload):
    try:
        response = httpx.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {}


# def delete_group(url,payload):
#     try:
#         response = httpx.delete(url,params=payload)
#         return response.json()
#     except Exception as e:
#         print(f"Error in delete_group: {str(e)}")
#         return {}


def delete_group(url, params_data):
    try:
        response = httpx.delete(url, params=params_data)
        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
            return {"status": response.status_code,
                    "message": "Request failed"}

        # Check if response content is not empty
        if response.content:
            return response.json()
        else:
            print("Empty response content")
            return {"status": response.status_code,
                    "message": "Empty response"}
    except Exception as e:
        print(f"Error in delete_group: {str(e)}")
        return {"status": "error", "message": str(e)}


def retry_operation(operation, max_retries=3, *args, **kwargs):
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = operation(*args, **kwargs)
            if response.get('status') == 200:
                return response
        except Exception as e:
            logging.error(f"Error in operation: {str(e)}")
        retry_count += 1
        sleep_time = exponential_backoff(retry_count)
        time.sleep(sleep_time)
    return None

def exponential_backoff(retry_count):
    return 2 ** retry_count + random.uniform(0, 1)

