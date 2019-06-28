# Todo: success를 한 response인 경우 serializer data를 함께 response해준다.
# Todo: 이 부분은 함수를 이용하여 로직 처리를 하는 방법도 고려

from rest_framework.response import Response
from rest_framework import status


# 일정 가져오기 실패 response
ScheduleNotFoundError = Response({
    'success': False,
    'data': {
        'message': '해당 일정을 찾을 수 없습니다.'
    }
}, status=status.HTTP_404_NOT_FOUND)

# 유저 가져오기 실패 response
UserNotFoundError = Response({
    'success': False,
    'data': {
        'message': '해당 유저를 찾을 수 없습니다.'
    }
}, status=status.HTTP_404_NOT_FOUND)

# 요청 형식 불일치 response
RequestFormatError = Response({
    'success': False,
    'data': {
        'message': '요청 형식에 맞지 않습니다.'
    }
}, status=status.HTTP_400_BAD_REQUEST)

# 이미 참여 중인 일정 response
ScheduleUserAlreadyExistsError = Response({
    'success': False,
    'data': {
        'message': '일정에 이미 참여 중인 유저'
    }
}, status=status.HTTP_400_BAD_REQUEST)

# 참여하고 있지 않은 일정 response
ScheduleNotParticipantedError = Response({
    'suceess': False,
    'data': {
        'message': '해당 일정에 참여하고 있지 않습니다.'
    }
}, status=status.HTTP_400_BAD_REQUEST)

# 일정 등록자 추방 불가 response
ScheduleExpulsionPermissionError = Response({
    'success': False,
    'data': {
        'message': '일정 등록자는 추방시킬 수 없습니다.'
    }
}, status=status.HTTP_400_BAD_REQUEST)

# 일정에 이미 도착한 유저 response
ScheduleUserAlreadyArrivalError = Response({
    'success': False,
    'data': {
        'message': '이미 도착한 유저입니다.'
    }
}, status=status.HTTP_400_BAD_REQUEST)