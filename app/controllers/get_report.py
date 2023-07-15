from flask import Blueprint, send_file, request, jsonify, Flask
from app.dao.report_dao import get_report_status_location

get_report_route = Blueprint('get_report', __name__)

@get_report_route.route('/get_report', methods=['GET'])
def get_report():
    report_id = request.args.get('report_id')

    report_status_location = get_report_status_location(report_id)

    if report_status_location is not None:
        report_status = report_status_location[0][0]
        if report_status == 'Running':
            return jsonify({'status': 'Running'})
        elif report_status == 'Completed':
            csv_location = report_status_location[0][1]
            return send_file(csv_location, mimetype='text/csv', as_attachment=True)


    return jsonify({'error': 'Invalid report_id'})

