from datetime import datetime
from time import mktime

import math
import json
import traceback
import uuid


class HttpUtil(object):
    def get_request_data(self, request):
        is_chunked = request.META.get("HTTP_TRANSFER_ENCODING")
        if is_chunked == 'chunked':
            print(request.META['HTTP_APP_META'])
            input_data_tmp = request.stream.read().decode("utf-8")
            input_data = json.loads(input_data_tmp)
        else:
            input_data = request.data
        return input_data

    def get_header_data(self, request):
        header_app_meta = {}
        session_id = ""

        date = datetime.now()
        mk_datetime = mktime(date.timetuple())
        Date = math.floor(mk_datetime)
        try:
            header_meta = request.META['HTTP_APP_META']
            app_meta = json.loads(header_meta)
            if 'log_session_id' in app_meta:
                if app_meta['log_session_id'] != '':
                    session_id = app_meta['log_session_id']

            if 'env' in app_meta:
                header_app_meta['env'] = app_meta['env']

            header_app_meta['user_name'] = app_meta['user_name']
            header_app_meta['user_id'] = app_meta['user_id']
            header_app_meta['request_datetime'] = app_meta['request_datetime']
            try:
                date = app_meta['request_datetime']
                date_object = datetime.strptime(date, '%d-%m-%Y %H:%M:%S')
                mk_datetime = mktime(date_object.timetuple())
                current_timestamp = math.floor(mk_datetime) * 1000
                header_app_meta['request_datetime_long'] = current_timestamp
            except:
                header_app_meta['request_datetime_long'] = Date * 1000
            header_app_meta['response'] = "20000"

        except Exception as e:
            traceback.print_exc()
            # log.error("{}".format(e))
            header_app_meta['response'] = "22000"
            header_app_meta['detail'] = "{}".format(e)

        if session_id == "":
            session_id = str(uuid.uuid4())
            header_app_meta['log_session_id'] = session_id
            # log.set_sessionId(session_id)
            # log.put_cacheData()
        else:
            # log.set_sessionId(session_id)
            header_app_meta['log_session_id'] = session_id

        return header_app_meta
