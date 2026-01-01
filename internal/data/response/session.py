from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RawResponse(BaseModel):
    """
    请求响应 返回结果
    """

    code: int = Field(description="状态码")
    msg: Optional[str] = Field(default="", description="提示信息")
    data: Optional[Dict[Any, Any] | List] = Field(default=None, description="数据")
