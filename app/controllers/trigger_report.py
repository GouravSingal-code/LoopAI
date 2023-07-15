from flask import jsonify,Flask,Blueprint
import uuid
import datetime
from app.scheduler import check_scheduler_status
from app.models.report import Report
from app.dao.report_dao import get_last_report, insert_report

trigger_report_route = Blueprint('trigger_report', __name__)

@trigger_report_route.route('/trigger_report', methods=['POST'])
def trigger_report():
    report_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now()
    
    last_report = get_last_report(timestamp)
    report = Report(report_id, timestamp, 'Running', '')

    if len(last_report)>0 :
        report.status = "Completed"
        report.location = last_report[0][3]
        insert_report(report)
    else:
        insert_report(report)
        check_scheduler_status(report_id,timestamp)
    return jsonify({'message': 'Report generation  triggered','report_id':report_id})
