from flask import jsonify
from components.database import appointments as apt
from components.utils.helpers import datetime_validator


def create_appointment_controller(payload):
    apt_start = payload.get('start')
    apt_end = payload.get('end')
    payload['assigned_to'] = None
    payload['accepted'] = False
    if not apt_start:
        return jsonify({'error': 'Start time and date is required.'}), 400
    if not apt_end:
        return jsonify({'error': 'End time and date is required.'}), 400
    if not datetime_validator(apt_start):
        return jsonify({'error': 'Start time and date is invalid.'}), 400
    if not datetime_validator(apt_end):
        return jsonify({'error': 'End time and date is invalid.'}), 400
    if apt_start >= apt_end:
        return jsonify({'error': 'End date and time should be later than start.'}), 400

    return apt.create_appointment(payload)


def update_appointment_controller(payload):
    if apt.is_appointment_accepted(payload['id']):
        return jsonify({
            'error': 'Changes not allowed. Appointment already accepted by physician.'}), 405

    apt_start = payload.get('start')
    apt_end = payload.get('end')

    if apt_start and not datetime_validator(apt_start):
        return jsonify({'error': 'Start time and date is invalid.'}), 400
    if apt_end and not datetime_validator(apt_end):
        return jsonify({'error': 'End time and date is invalid.'}), 400
    if apt_start and apt_end and apt_start >= apt_end:
        return jsonify({'error': 'End date and time should be later than start.'}), 400

    return apt.update_appointment(payload)


def search_appointment_controller(payload):
    apt_start = payload.get('start')
    apt_end = payload.get('end')
    assigned_to = payload.get('assigned_to')
    accepted = payload.get('accepted')
    print(payload)
    if apt_start and not datetime_validator(apt_start):
        return jsonify({'error': 'Start time and date is invalid.'}), 400
    if apt_end and not datetime_validator(apt_end):
        return jsonify({'error': 'End time and date is invalid.'}), 400
    return apt.search_appointment(
                    start=apt_start,
                    end=apt_end,
                    assigned_doctor=assigned_to,
                    accepted=accepted)
