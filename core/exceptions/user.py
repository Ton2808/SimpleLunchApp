from core.exceptions import base

class DuplicateEmailOrNicknameException(base.CustomHTTPException):
    code = 400
    message = "duplicate email or nickname"
