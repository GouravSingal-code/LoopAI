from flask import jsonify,Flask
import uuid
import datetime
from app.scheduler import check_scheduler_status
from app.models.report import Report
from app.dao.report_dao import get_last_report, insert_report

app = Flask(__name__)


@app.route('/trigger_report', methods=['POST'])
def trigger_report():
    report_id = str(uuid.uuid4())
    timeStamp = datetime.datetime.now()
    
    last_report = get_last_report(timeStamp)
    report = Report(report_id, timeStamp, 'Running', '')

    if len(last_report)>0 :
        report.status = "Completed"
        report.location = last_report[0][3]
        insert_report(report)
    else:
        insert_report(report)
        check_scheduler_status(report_id)
    return jsonify({'message': 'Report generation  triggered','report_id':report_id})


if __name__ == "__main__":
    app.run()