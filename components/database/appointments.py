import random
import string
import time
from flask import jsonify
from components.database import users as usr
from components.utils.sendgrid_mail import send_email
from components.utils import redis as rs


def apt_for_the_date(date):
    appointments = list_appointments()
    scheduled_appointments = [
        apt['id'] for apt in appointments if apt['date']==date]
    return scheduled_appointments


def create_appointment(payload):
    collection = 'appointments'
    random_str = ''.join(random.choices(string.ascii_lowercase, k=3))
    key = f'{time.time()}{random_str}'
    id = f'{collection}_{key}'
    payload['id'] = id

    appointment_count = len(apt_for_the_date(payload['date']))
    if  appointment_count >= 5:
        return jsonify({
            'error': 'There are already 5 appointments scheduled for the selected date.'
        }), 405
    doctor = payload.get('assigned_to')
    if appointment_conflict(doctor, payload['date'], payload['start'], payload['end']):
        return jsonify({'error': 'Doctor has a conflicting schedule.'}), 405

    rs.create_data(collection, key, payload)
    if doctor:
        send_email(doctor, payload)
    return jsonify({'status': 'Appointment created.'})


def update_appointment(payload):
    collection = 'appointments'
    key = payload['id'].split('_')[1]
    data = payload
    base_appointment = get_appointment(payload['id'])
    # supply dict with the data from base appointment if missing from payload
    for k in base_appointment.keys():
        if not data.get(k):
            data[k] = base_appointment[k]

    same_date_appointments = apt_for_the_date(payload['date'])
    if payload['id'] in same_date_appointments:
        same_date_appointments.remove(payload['id'])
    if len(same_date_appointments) >= 5:
        return jsonify({
            'error': 'There are already 5 appointments scheduled for the selected date.'
        }), 405

    apt_id = data.get('id')
    doctor = data.get('assigned_to')
    if doctor and not usr.search_doctor(doctor):
        return jsonify({
            'error': 'Doctor is not on the list.'
        }), 400

    conflict_apt_list = appointment_conflict(doctor, data['date'], data['start'], data['end'])
    if apt_id in conflict_apt_list:
        conflict_apt_list.remove(apt_id)
    if conflict_apt_list:
        return jsonify({'error': 'Doctor has a conflicting schedule.'}), 405
    rs.create_data(collection, key, data)
    if doctor:
        send_email(doctor, data, True)
    return jsonify({'status': 'Appointment updated.'})


def assign_appointment(appointment, doctor):
    collection = 'appointments'
    key = appointment.split('_')[1]
    data = rs.read_data(collection, key)
    if appointment_conflict(doctor, data['date'], data['start'], data['end']):
        return jsonify({'error': 'Doctor is not available on this schedule.'}), 405
    data['assigned_to'] = doctor
    rs.create_data(collection, key, data)
    send_email(data['assigned_to'], data)
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


def accept_appointment(doctor, payload):
    records = rs.get_all_from_collection('appointments')
    selected_appointment = get_appointment(payload['id'])
    my_appointments = [
        appointment for appointment in records \
        if appointment['assigned_to']==doctor
    ]
    same_date_appointments = [
        appointment for appointment in my_appointments \
        if appointment['date']==selected_appointment['date'] \
        and appointment['accepted']==True \
        and not appointment['id']==selected_appointment['id']
    ]

    if len(same_date_appointments) >= 3:
        return jsonify({
            'error': 'You already accepted 3 other appointments for the selected date.'
        }), 405

    new_payload = dict()
    new_payload['id'] = payload['id']
    new_payload['accepted'] = True
    return update_appointment(new_payload)


def __doctor_appointments(doctor):
    records = rs.get_all_from_collection('appointments')
    appointments = [
        appointment for appointment in records \
        if appointment['assigned_to']==doctor
    ]
    return appointments


def doctor_appointments(doctor):
    appointments = __doctor_appointments(doctor)
    return jsonify({'data': appointments})


def my_appointments_search(doctor, start_date, end_date, accepted):
    my_appointments = __doctor_appointments(doctor)
    if len(my_appointments) == 0:
        return jsonify({'data': []})

    filtered_appointments = [
        appointment for appointment in my_appointments \
        if appointment['date'] >= start_date \
        and appointment['date'] <= end_date
    ]
    output_appointment = [
        appointment for appointment in filtered_appointments \
        if appointment['accepted'] == accepted
    ]
    return jsonify({'data': output_appointment})


def appointment_conflict(doctor, date, start, end):
    if doctor is None:
        return []

    appointments = __doctor_appointments(doctor)
    dated_appointments = [
        apppointment for apppointment in appointments \
        if apppointment['date'] == date
    ]

    conflict_list_id = list()
    for dated_apt in dated_appointments:
        if (
            (dated_apt['start'] < start and start < dated_apt['end']) or
            (dated_apt['start'] < end and end < dated_apt['end']) or
            (start < dated_apt['start'] and dated_apt['end'] < end) or
            (dated_apt['start'] < start and end < dated_apt['end']) or
            (dated_apt['start'] == start and end == dated_apt['end'])
        ):
            conflict_list_id.append(dated_apt['id'])
    return conflict_list_id


def all_appointments():
    return jsonify({'data': list_appointments()})
