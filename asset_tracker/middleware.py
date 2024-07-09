from datetime import datetime
import logging

class TimingMiddleware:
    '''
    Middleware to log the time taken for each request
    '''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    def process_request(self, request):
        request.start_time = datetime.now()

    def process_response(self, request, response):        
        end_time = datetime.now()
        logging.info(f"TimingMiddleware: Time taken for request: {end_time - request.start_time} from {request.path}")
        return response