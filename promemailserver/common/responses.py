from django.http import JsonResponse


class Response(JsonResponse):
    def __init__(self,data,message=None):
        self.data = data
        self.data["message"]=message
        self.status_code = 200
        self.content_type = "application/json"
        super(Response, self).__init__(self.data, status=self.status_code, content_type=self.content_type)
