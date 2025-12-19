from pydantic import BaseModel, ConfigDict, Field

from internal.util.crypto import String


class CppClientInfo(BaseModel):
    """
    CPP 客户端信息
    """


class CppDeviceInfo(BaseModel):
    """
    CPP 设备信息
    """


class CppHeaders(BaseModel):
    """
    CPP 请求头
    """

    model_config = ConfigDict(populate_by_name=True)


class CppCookies(BaseModel):
    """
    CPP 响应 Cookie
    """

    token: str = Field(default="")
