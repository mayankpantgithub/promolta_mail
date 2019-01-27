from django.http import JsonResponse


class BadRequestError(JsonResponse):
    def __init__(self,message,data=None):
        if not data:
            data = {}
        data["message"] = message
        self.data = data
        self.content_type="application/json"
        self.status_code = 400
        super(BadRequestError, self).__init__(self.data, status=self.status_code, content_type=self.content_type)


class InternalError(JsonResponse):
    def __init__(self,message,data=None):
        self.data = data or {}
        self.data["message"]=message
        self.content_type = "application/json"
        self.status_code = 500
        super(InternalError, self).__init__(self.data, status=self.status_code, content_type=self.content_type)
