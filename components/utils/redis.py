import redis
import json
from flask import jsonify


r = redis.Redis(host='localhost', port=6379, db=0)


def read_data(collection, key):
    data = r.get(f'{collection}_{key}')
    try:
        return json.loads(data)
    except TypeError as ex:
        return data


def create_data(collection, key, data):
    if isinstance(data, dict):
        data = json.dumps(data)
    r.set(f'{collection}_{key}', data)
    return jsonify({
        'status': 'Record saved.'
    }), 200


def get_all_from_collection(collection):
    cursor, keys = r.scan(match=f'{collection}_*')
    init_records = [item.decode('utf_8') for item in r.mget(keys)]
    records = [json.loads(item) for item in init_records]
    return records
