from asyncio import protocols
from fastapi import HTTPException, status

class AppException(Exception):
    """Base application exception"""
class UserAlreadyExistsException(AppException):
    """Exception raised when a user already exists"""
    pass
class UserNotFoundException(AppException):
    status_code = 404
    detail = "User not found"

class InvalidCredentialsException(AppException):
    """Exception raised when credentials are invalid"""
    pass

class AlarmAlreadyArmedException(AppException):
    """Exception raised when alarm is already armed"""
    pass

class AlarmAlreadyDisarmedException(AppException):
    """Exception raised when alarm is already disarmed"""
    pass

class SensorNotFoundException(AppException):
    status_code = 404
    detail = "Sensor not found"
class SensorReadingNotFoundException(AppException):
    status_code = 404
    detail = "Sensor reading not found"
class AlarmEventNotFoundException(AppException):
    status_code = 404
    detail = "Alarm event not found"
class NotificationNotFoundException(AppException):
    status_code = 404
    detail = "Notification not found"
class SettingNotFoundException(AppException):
    status_code = 404
    detail = "Setting not found"

class SettingAlreadyExistsException(AppException):
    status_code = 404
    detail = "Setting already exists"
    
class InvalidAlarmStateException(HTTPException):
    def __init__(self, current_state: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot perform this operation while alarm is in '{current_state}' state."
        )
class DeviceNotFoundException(AppException):
    status_code = 404
    detail = "Device not found"
class DeviceAlreadyExistsException(AppException):
    status_code = 404
    detail = "Device already exists"

class InvalidPinException(AppException):
    status_code = 403
    detail = "Invalid pin"

class CarPlateNotFoundException(AppException):
    status_code = 404
    detail = "Car plate not found"

class InvalidDeviceTypeException(AppException):
    status_code = 400
    detail = "Invalid device type"

class CarNotAuthorizedException(AppException):
    status_code = 403
    detail = "Car not authorized"

class AlarmNotFoundException(AppException):
    status_code = 404
    detail = "Alarm not found"

class AlarmAlreadyExistsException(AppException):
    status_code = 404
    detail = "Alarm already exists"
    
class AlarmAccessDeniedException(AppException):
    status_code = 403
    detail = "Alarm access denied"

class UserAlreadyAddedToAlarm(AppException):
    status_code = 403
    detail = "User already is added to alarm"

class UserNotAddedToAlarm(AppException):
    status_code = 403
    detail = "User already is added to alarm"
