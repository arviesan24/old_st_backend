import random
import string
import time
from flask import jsonify
from components.utils import redis as rs


def create_appointment(payload):
    collection = 'appointments'
    random_str = ''.join(random.choices(string.ascii_lowercase, k=3))
    key = f'{time.time()}{random_str}'
    id = f'{collection}_{key}'
    payload['id'] = id
    data = payload
    rs.create_data(collection, key, data)
    return jsonify({'status': 'Appointment created.'})


def update_appointment(payload):
    collection = 'appointments'
    key = payload['id'].split('_')[1]
    data = payload
    base_appointment = get_appointment(payload['id'])
    for k in base_appointment.keys():
        if not data.get(k):
            data[k] = base_appointment[k]
    rs.create_data(collection, key, data)
    return jsonify({'status': 'Appointment updated.'})

def assign_appointment(appointment, doctor):
    collection = 'appointments'
    key = appointment.split('_')[1]
    data = rs.read_data(collection, key)
    data['assigned_to'] = doctor
    rs.create_data(collection, key, data)
    return jsonify({'status': f'Appointment assigned to the doctor.'})


def list_appointments():
    records = rs.get_all_from_collection('appointments')
    return records


def get_appointment(appointment_id):
    collection = 'appointments'
    key = appointment_id.split('_')[1]
    res = rs.read_data(collection, key)
    if res:
        return res
    return {}


def search_appointment(_date=None, start=None, end=None, assigned_doctor=None, accepted=None):
    appointments = list_appointments()
    if _date:
        appointments = [item for item in appointments if item['date']==_date]
    if start:
        appointments = [item for item in appointments if item['start']==start]
    if end:
        appointments = [item for item in appointments if item['end']==end]
    if assigned_doctor:
        appointments = [item for item in appointments if item['assigned_to']==assigned_doctor]
    if accepted:
        appointments = [item for item in appointments if item['accepted']==accepted]
    return jsonify({'data': appointments})


def is_appointment_accepted(appointment_id):
    collection = 'appointments'
    key = appointment_id.split('_')[1]
    res = rs.read_data(collection, key)
    accepted = res.get('accepted')
    if accepted:
        return True
    return False
