from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class QueryBuyerData(BaseModel):
    """
    购票人信息
    """

    id: int = Field(description="购票人 ID")
    realname: str = Field(description="购票人姓名")
    idcard: str = Field(description="购票人证件号码")
    mobile: str = Field(description="购票人手机号")
    validType: int = Field(description="证件类型")

    model_config = ConfigDict(extra="ignore")


class QueryBuyerResponse(BaseModel):
    """
    购票人信息 返回结果
    """

    code: int = Field(description="状态码")
    msg: Optional[str] = Field(default="", description="提示信息")
    data: Optional[List[QueryBuyerData]] = Field(default=None, description="数据")
