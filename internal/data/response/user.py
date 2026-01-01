from typing import Optional

from pydantic import BaseModel, Field


class QueryLoginToken(BaseModel):
    """
    登录 Token
    """

    token: Optional[str] = Field(default=None, description="Token")


class QueryLoginResponse(BaseModel):
    """
    登录 返回结果
    """

    code: int = Field(description="状态码")
    msg: Optional[str] = Field(default="", description="提示信息")
    data: Optional[QueryLoginToken] = Field(default=None, description="数据")
