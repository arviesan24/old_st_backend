from flask import jsonify
from components.database import appointments as apt
from components.database import users as usr
from components.utils.helpers import date_validator, time_validator


def create_appointment_controller(payload):
    """
    {
        "date": str,
        "start": str,
        "end": str,
        "assigned_to": str,
        "patient_name": str,
        "comment": str,
        "accepted": bool
    }
    """
    apt_date = payload.get('date')
    apt_start = payload.get('start')
    apt_end = payload.get('end')
    doctor = payload.get('assigned_to')
    patient_name = payload.get('patient_name')
    comment = payload.get('comment')
    payload['accepted'] = False

    if not comment:
        payload['comment'] = None

    if not apt_date:
        return jsonify({"error": "Date is required."}), 400
    if not date_validator(apt_date):
        return jsonify({"error": "Date is invalid. Format('YYYY-MM-DD')"}), 400

    if not apt_start:
        return jsonify({"error": "Start time is required."}), 400
    if not time_validator(apt_start):
        return jsonify({"error": "Start time is invalid. Format('HH:MM')"}), 400

    if not apt_end:
        return jsonify({"error": "End time is required."}), 400
    if not time_validator(apt_end):
        return jsonify({"error": "End time is invalid. Format('HH:MM')"}), 400

    if not patient_name:
        return jsonify({"error": "Patient's name is required."}), 400

    if not doctor:
        payload['assigned_to'] = None
    else:
        is_doctor_available = usr.is_doctor_available(doctor)
        if not is_doctor_available:
            return jsonify({"error": "Selected doctor not available."}), 400

    if apt_start >= apt_end:
        return jsonify({"error": "End time should be later than start time."}), 400

    return apt.create_appointment(payload)


def update_appointment_controller(payload):
    apt_id = payload.get('id')
    apt_date = payload.get('date')
    apt_start = payload.get('start')
    apt_end = payload.get('end')

    if not apt_id:
        return jsonify({"error": "Appointment ID missing."}), 400
    if apt_date and not date_validator(apt_date):
        return jsonify({"error": "Date is invalid. Format('YYYY-MM-DD')"}), 400
    if apt_start and not time_validator(apt_start):
        return jsonify({"error": "Start time is invalid. Format('HH:MM')"}), 400
    if apt_end and not time_validator(apt_end):
        return jsonify({"error": "End time is invalid. Format('HH:MM')"}), 400
    if apt_start and apt_end and apt_start >= apt_end:
        return jsonify({"error": "End time should be later than start time."}), 400

    if apt.is_appointment_accepted(payload['id']):
        return jsonify({
            "error": "Changes not allowed. Appointment already accepted by physician."}), 405

    return apt.update_appointment(payload)


def search_appointment_controller(payload):
    start_date = payload.get('start_date')
    end_date = payload.get('end_date')
    if start_date and not date_validator(start_date):
        return jsonify({"error": "Start date is invalid. Format('YYYY-MM-DD')"}), 400
    if end_date and not date_validator(end_date):
        return jsonify({"error": "End date is invalid. Format('YYYY-MM-DD')"}), 400
    return apt.search_appointment(start_date, end_date)


def assign_appointment_controller(payload):
    apt_id = payload.get('id')
    assigned_doctor = payload.get('doctor')
    if not apt_id:
        return jsonify({"error": "Appointment ID missing."}), 400
    if not assigned_doctor:
        return jsonify({"error": "Select a doctor to assign."}), 400
    is_doctor_available = usr.is_doctor_available(assigned_doctor)
    if not is_doctor_available:
        return jsonify({"error": "Selected doctor not available."}), 400
    return apt.assign_appointment(apt_id, assigned_doctor)


def delete_appointment_controller(payload):
    appointment_id = payload.get('id')
    if not appointment_id:
        return jsonify({"error": "Appointment ID is required."}), 400
    return apt.delete_appointment(appointment_id)


def accept_appointment_controller(user_id, payload):
    appointment_id = payload.get('id')
    appointment = apt.get_appointment(appointment_id)
    if appointment['assigned_to'] != user_id:
        return jsonify({"error": "This appointment is not assigned to you."}), 400
    return apt.accept_appointment(payload)


def doctor_appointments_controller(doctor):
    if not doctor:
        return jsonify({"error": "No doctor selected."}), 400
    return apt.doctor_appointments(doctor)
