from flask import Flask
from app.scheduler import schedule_jobs
app = Flask(__name__)


from .controllers.trigger_report import *
from .controllers.get_report import *

# if __name__ == "__main__":
#     schedule_jobs()
