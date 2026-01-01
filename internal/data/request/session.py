from pydantic import BaseModel


class CppHeaders(BaseModel):
    """
    CPP 请求头
    """


class CppCookies(BaseModel):
    """
    CPP 响应 Cookie
    """
