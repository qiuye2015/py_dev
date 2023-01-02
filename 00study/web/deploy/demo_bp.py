import time

from flask import Blueprint, request, jsonify

from tools.tool_log.Best_Practices.log import get_logger

bp = Blueprint('rawdata_backup', __name__, url_prefix='/api/v1')

logger = get_logger()


@bp.route('/demo', methods=['POST'])
def demo():
    logger.info("start")
    time.sleep(15)
    logger.info("end")
    return jsonify(code=0, message='ok')
