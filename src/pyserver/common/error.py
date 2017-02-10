# Common error code
ERROR_CODE_OK = 0
ERROR_CODE_FAIL = 1
ERROR_CODE_SYSTEM = 2
ERROR_CODE_PARAM_WRONG = 3
ERROR_CODE_NOT_LOGINED = 4
ERROR_CODE_ILLEGAL_REQUEST = 5
ERROR_CODE_NO_PERMISSION = 6
ERROR_CODE_RESOURCE_NOT_FOUND = 7
ERROR_CODE_RESOURCE_DUPLICATED = 8

# User error code
ERROR_CODE_USER_INVISIBLE = 1000
ERROR_CODE_USER_PASSWORD_WRONG = 1001

# Error message
MESSAGES = {
    ERROR_CODE_OK: "成功",
    ERROR_CODE_FAIL: "失败",
    ERROR_CODE_SYSTEM: "系统错误",
    ERROR_CODE_PARAM_WRONG: "参数错误",
    ERROR_CODE_NOT_LOGINED: "未登录",
    ERROR_CODE_ILLEGAL_REQUEST: "非法请求",
    ERROR_CODE_NO_PERMISSION: "无权操作",
    ERROR_CODE_RESOURCE_NOT_FOUND: "资源未找到",
    ERROR_CODE_RESOURCE_DUPLICATED: "资源重复",

    ERROR_CODE_USER_INVISIBLE: "用户不可见",
    ERROR_CODE_USER_PASSWORD_WRONG: "密码错误",
}


class Error(Exception):
    def __init__(self, code=ERROR_CODE_FAIL, message=""):
        super().__init__(code, message)
        self.code = code
        self.message = message

    def __str__(self):
        return "{} {}".format(self.code, self.message)


class ServiceError(Error):
    pass
