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

    appointments = list_appointments()
    same_date_appointments = [apt['id'] for apt in appointments if apt['date']==payload['date']]
    if len(same_date_appointments) >= 5:
        return jsonify({'error': 'There are already 5 appointments scheduled for the selected date.'}), 405

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

    appointments = list_appointments()
    same_date_appointments = [apt['id'] for apt in appointments if apt['date']==payload['date']]
    same_date_appointments.remove(payload['id'])
    if len(same_date_appointments) >= 5:
        return jsonify({'error': 'There are already 5 appointments scheduled for the selected date.'}), 405

    rs.create_data(collection, key, data)
    return jsonify({'status': 'Appointment updated.'})


def assign_appointment(appointment, doctor):
    collection = 'appointments'
    key = appointment.split('_')[1]
    data = rs.read_data(collection, key)
    data['assigned_to'] = doctor
    rs.create_data(collection, key, data)
    return jsonify({'status': 'Appointment assigned to the doctor.'})


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


def search_appointment(start_date, end_date):
    appointments = list_appointments()
    appointments = [
        appointment for appointment in appointments \
        if appointment['date'] >= start_date \
        and appointment['date'] <= end_date
    ]
    return jsonify({'data': appointments})


def is_appointment_accepted(appointment_id):
    collection = 'appointments'
    key = appointment_id.split('_')[1]
    res = rs.read_data(collection, key)
    accepted = res.get('accepted')
    if accepted:
        return True
    return False


def delete_appointment(appointment_id):
    appointment = get_appointment(appointment_id)
    if not appointment.get('accepted'):
        collection = 'appointments'
        key = appointment_id.split('_')[1]
        rs.delete_item(collection, key)
        return jsonify({'status': 'Appointment successfully deleted.'})
    return jsonify({'error': 'Cannot delete already accepted appointment.'}), 405


def accept_appointment(payload):
    new_payload = dict()
    new_payload['id'] = payload['id']
    new_payload['accepted'] = True
    return update_appointment(new_payload)


def doctor_appointments(doctor):
    records = rs.get_all_from_collection('appointments')
    appointments = [
        appointment for appointment in records \
        if appointment['assigned_to']==doctor
    ]
    return jsonify({'data': appointments})
