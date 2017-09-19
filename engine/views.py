import boto3

from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse

from engine.core.dataobjects.car import Car
from engine.core.dataobjects.cat import Cat
from engine.core.util.http import HttpUtil

from django.views.generic.base import TemplateView


def easyfunction(request, ):
    c = Car('Mazda')
    c.run()
    c.debug()
    current_fuel = c.get_fuel()

    print(c)
    print(c.__dict__)

    cat = Cat('Kitty')
    cat.info()

    http = HttpUtil()
    http.get_header_data(request)

    str(http.get_header_data(request))
    return HttpResponse("Current Fuel: " + str(c) + " " + c.brand + " " + str(current_fuel))


class HomePageView(TemplateView):

    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['latest_articles'] = 'hello'
        return context



# using as a cron to retrieve from queue and insert to DE
class UpdateSmppResponse(APIView):

    _SQS = boto3.resource('sqs', region_name=settings.SQS_REGION_NAME)
    _MAX_QUEUE_MESSAGES = 10

    def message_consumer(self, queue_name):
        sqs = self._SQS
        queue = sqs.get_queue_by_name(QueueName=queue_name)

        # Process messages by printing out body from test Amazon SQS Queue
        message_bodies = []
        while True:
            messages_to_delete = []
            for message in queue.receive_messages(MaxNumberOfMessages=self._MAX_QUEUE_MESSAGES):
                # process message body
                #body = json.loads(message.body)
                #message_bodies.append(body)
                # add message to delete
                messages_to_delete.append(message)

                # TODO do something from here



            # if you don't receive any notifications the
            # messages_to_delete list will be empty
            if len(messages_to_delete) == 0:
                break
            # delete messages to remove them from SQS queue
            # handle any errors
            else:
                print('' + str(messages_to_delete))

        result = dict()
        result['meta'] = {}
        result['meta']['response_desc'] = "Success"
        result['meta']['response_code'] = "22000"

        return result

    def queue_list(self):
        sqs = self._SQS
        # Retrieving a queue by its name
        # queue = sqs.get_queue_by_name(QueueName=queue_name)

        # Printing queues information
        # print("Queue url retrieved: {0}" .format(queue.url))
        # print("Retrieved queue and its attributes: {0}".format(queue.attributes.get('DelaySeconds')))

        # Printing all queues urls that exists in Amazon SQS
        print("\nPrinting all queues from Amazon SQS")
        for queue in sqs.queues.all():
            print("Queue url: {0}" . format(queue.url))

    def post(self, request):
        result = self.message_consumer('dev-smppgateway-responsemt')

        return Response(result)

    def get(self, request):
        return self.post(request)


class SendSmppMessage(APIView):

    _SQS = boto3.resource('sqs', region_name=settings.SQS_REGION_NAME)
    _MAX_QUEUE_MESSAGES = 10

    # 'dev-smppgateway-responsemt'
    def sender(self, queue_name):
        sqs = self._SQS
        queue = sqs.get_queue_by_name(QueueName=queue_name)
        response = queue.send_message(MessageBody='world')
        return response

    def post(self, request):
        # Retrieving a queue by its name
        # queue = sqs.get_queue_by_name(QueueName='test')

        # Create a new message
        # response = queue.send_message(MessageBody='world')

        # The response is not a resource, but gives you a message ID and MD5
        # print("MessageId created: {0}".format(response.get('MessageId')))
        # print("MD5 created: {0}".format(response.get('MD5OfMessageBody')))  # define Q

        # sqs = boto3.resource('sqs', region_name=settings.SQS_REGION_NAME)
        # queue = sqs.get_queue_by_name(settings.QUEUE_NAME_BATCH_SMS)

        result = {}
        result['data'] = []
        usage = []
        message_con = []
        req_sms = {}
        req_sms['data'] = []
        dep_sms = []

        asyncFlag = False
        log = API("tfg_log")

        header_app_meta = {}
        header_app_meta['log_session_id'] = 'logsess'
        header_app_meta['user_name'] = 'username'

        header_meta = request.META['HTTP_APP_META']

        app_meta = json.loads(header_meta)
        if 'log_session_id' in app_meta:
            if (app_meta['log_session_id'] != ''):
                session_id = app_meta['log_session_id']

        if 'env' in app_meta:
            header_app_meta['env'] = app_meta['env']

        header_app_meta['user_name'] = app_meta['user_name']
        header_app_meta['user_id'] = app_meta['user_id']
        header_app_meta['request_datetime'] = app_meta['request_datetime']

        queue_util_func = queue_util()
        send_noti_header = queue_util_func.Queueheader(header_app_meta)

        sms_util_func = sms_util()
        #senddataresult = sms_util_func.SMS_queue(settings.QUEUE_NAME_SMS, req_sms, dep_sms, header_app_meta['log_session_id'],
                                #send_noti_header, header_app_meta['user_name'], message_con, asyncFlag, log,
                                #header_app_meta)

        #smssend = Sms_queue_send()

        #queue = sqs.get_queue_by_name(QueueName=settings.QUEUE_NAME_BATCH_SMS)
        #queue = sqs.get_queue_by_name(QueueName='dev-smppgateway-responsemt')

        #Qresponse = queue.send_message(MessageBody='Hello', MessageAttributes=send_noti_header)
        #Qresponse = queue.send_message(MessageBody='world')
        #smssend.Sms_queue_send_func(queue, '', dep_list, 'message_content', action_by, app_meta, send_noti_header, log)

        return Response(self.sender('dev-smppgateway-responsemt'))
