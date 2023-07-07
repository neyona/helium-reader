from rest_framework.exceptions import APIException


class RewardNotFound(APIException):
    status_code = 404
    default_detail = "The requested reward date does not exist"
