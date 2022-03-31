import redis
import json
from flask import jsonify


r = redis.Redis(host='localhost', port=6379, db=0)


def read_data(collection, key):
    data = r.get(f'{collection}_{key}')
    # print('result', data)
    try:
        return json.loads(data)
    except json.decoder.JSONDecodeError:
        return data


def create_data(collection, key, data):
    if isinstance(data, dict):
        data = json.dumps(data)
    r.set(f'{collection}_{key}', data)
    return jsonify({
        'status': 'Record saved.'
    }), 200
