from rest_framework.exceptions import APIException
from rest_framework import status


class EmailInvalid(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이메일이 형식에 맞지 않습니다."
    default_code = "email_invalid"


class EmailBlank(APIException):
    status_code = status.HTTP_202_ACCEPTED
    default_detail = "이메일 값이 비어있습니다."
    default_code = "email_blank"


class EmailUnique(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "이미 사용 중인 이메일입니다."
    default_code = "email_unique"


class EmailUseful(APIException):
    status_code = status.HTTP_200_OK
    default_detail = "사용 가능한 이메일입니다."
    default_code = "email_useful"


class NicknameBlank(APIException):
    status_code = status.HTTP_202_ACCEPTED
    default_detail = "닉네임 값이 비어있습니다."
    default_code = "nickname_blank"


class NicknameMaxLength(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "닉네임의 최대 길이는 30자입니다."
    default_code = "nickname_max_length"


class NicknameUnique(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "이미 사용 중인 닉네임입니다."
    default_code = "nickname_unique"


class NicknameUseful(APIException):
    status_code = status.HTTP_200_OK
    default_detail = "사용 가능한 닉네임입니다."
    default_code = "nickname_useful"