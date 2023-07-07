from rest_framework.exceptions import APIException


class HotspotNotFound(APIException):
    status_code = 404
    default_detail = "The requested hotpot does not exist"
