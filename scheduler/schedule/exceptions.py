from rest_framework.exceptions import APIException


# 일정 가져오기 실패 response
class ScheduleNotFoundException(APIException):
    status_code = 404
    default_detail = {
        'success': False,
        'data': {
            'message': '해당 일정을 찾을 수 없습니다.'
        }
    }
    default_code = 'schedule_not_found'


# 유저 가져오기 실패 response
class UserNotFoundException(APIException):
    status_code = 404
    default_detail = {
        'success': False,
        'data': {
            'message': '해당 유저를 찾을 수 없습니다.'
        }
    }
    default_code = 'user_not_found'


# 요청 형식 불일치 response
class RequestFormatException(APIException):
    status_code = 400
    default_detail = {
        'success': False,
        'data': {
            'message': '요청 형식에 맞지 않습니다.'
        }
    }
    default_code = 'request_format_error'


# 이미 참여 중인 일정 response
class ScheduleUserAlreadyExistsException(APIException):
    status_code = 400
    default_detail = {
        'success': False,
        'data': {
            'message': '일정에 이미 참여 중인 유저'
        }
    }
    default_code = 'schedule_user_already_exists'


# 참여하고 있지 않은 일정 response
class ScheduleNotParticipantException(APIException):
    status_code = 400
    default_detail = {
        'success': False,
        'data': {
            'message': '해당 일정에 참여하고 있지 않습니다.'
        }
    }
    default_code = 'schedule_not_participant'


# 일정 등록자 추방 불가 response
class ScheduleExpulsionPermissionException(APIException):
    status_code = 400
    default_detail = {
        'success': False,
        'data': {
            'message': '일정 등록자는 추방시킬 수 없습니다.'
        }
    }
    default_code = 'schedule_expulsion_permission'


# 일정에 이미 도착한 유저 response
class ScheduleUserAlreadyArrivalException(APIException):
    status_code = 400
    default_detail = {
        'success': False,
        'data': {
            'message': '이미 도착한 유저입니다.'
        }
    }
    default_code = 'schedule_user_already_arrival'
