# Todo: success를 한 response인 경우 serializer data를 함께 response해준다.
# Todo: 이 부분은 함수를 이용하여 로직 처리를 하는 방법도 고려

# 일정 생성 완료 response
ScheduleCreateSuccess = {
    'success': True,
    'data': {
        'message': '일정 생성 완료'
    }
}

# 일정 삭제 완료 response
ScheduleDeleteSuccess = {
    'success': True,
    'data': {
        'message': '일정 삭제 완료'
    }
}

# 일정에 멤버 추가 완료 response
ScheduleInviteSuccess = {
    'success': True,
    'data': {
        'message': '일정에 유저 추가 완료'
    }
}

# 일정 나가기 완료 response
ScheduleLeaveSuccess = {
    'success': True,
    'data': {
        'message': '일정 나가기 완료'
    }
}

# 일정 참가 멤버 추방 완료 response
ScheduleExpulsionSuccess = {
    'success': True,
    'data': {
        'message': '해당 유저 일정에서 추방 완료'
    }
}

# 일정 도착 완료 response
ScheduleArrivalSuccess = {
    'success': True,
    'data': {
        'message': '일정 도착 완료'
    }
}

# 참여하고 있는 일정 리스트 불러오기 완료 response
ScheduleFilterListSuccess = {
    'success': True,
    'data': {
        'message': '참여하고 있는 일정 불러오기 완료'
    }
}

# 참여하고 있는 일정 없음 완료 response
ScheduleFilterEmptySuccess = {
    'success': True,
    'data': {
        'message': '참여 중인 일정이 없습니다.'
    }
}

# 휴일 리스트 불러오기 완료 response
HolidayListSuccess = {
    'success': True,
    'data': {
        'message': '휴일 리스트 불러오기 완료'
    }
}

# 일정 가져오기 실패 response
ScheduleNotFoundError = {
    'success': False,
    'data': {
        'message': '해당 일정을 찾을 수 없습니다.'
    }
}

# 유저 가져오기 실패 response
UserNotFoundError = {
    'success': False,
    'data': {
        'message': '해당 유저를 찾을 수 없습니다.'
    }
}

# 요청 형식 불일치 response
RequestFormatError = {
    'success': False,
    'data': {
        'message': '요청 형식에 맞지 않습니다.'
    }
}

# 이미 참여 중인 일정 response
ScheduleUserAlreadyExistsError = {
    'success': False,
    'data': {
        'message': '일정에 이미 참여 중인 유저'
    }
}

# 참여하고 있지 않은 일정 response
ScheduleNotParticipantedError = {
    'suceess': False,
    'data': {
        'message': '해당 일정에 참여하고 있지 않습니다.'
    }
}

# 일정 등록자 추방 불가 response
ScheduleExpulsionPermissionError = {
    'success': False,
    'data': {
        'message': '일정 등록자는 추방시킬 수 없습니다.'
    }
}

# 일정에 이미 도착한 유저 response
ScheduleUserAlreadyArrivalError = {
    'success': False,
    'data': {
        'message': '이미 도착한 유저입니다.'
    }
}