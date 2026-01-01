from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class QueryPruductMainData(BaseModel):
    """
    活动信息
    """

    eventMainId: int = Field(description="活动 ID")
    eventName: str = Field(description="活动名称")

    model_config = ConfigDict(extra="ignore")


class QueryProductTypeData(BaseModel):
    """
    票档信息
    """

    id: int = Field(description="票档 ID")
    ticketName: str = Field(description="票档名称")
    square: str = Field(description="场次名称")
    ticketPrice: int = Field(description="票档价格")
    purchaseNum: int = Field(description="可购买数量")
    remainderNum: int = Field(description="剩余数量")
    lockNum: int = Field(description="已锁定数量")
    realnameAuth: bool = Field(description="实名制购票")
    sellStartTime: int = Field(description="售票开始时间")
    sellEndTime: int = Field(description="售票结束时间")

    model_config = ConfigDict(extra="ignore")


class QueryProductData(BaseModel):
    """
    活动信息 数据
    """

    ticketMain: QueryPruductMainData = Field(description="活动信息")
    ticketTypeList: List[QueryProductTypeData] = Field(description="票档信息")


class QueryProductResponse(BaseModel):
    """
    活动信息 返回结果
    """

    code: int = Field(description="状态码")
    msg: Optional[str] = Field(default="", description="提示信息")
    data: Optional[QueryProductData] = Field(default=None, description="数据")
