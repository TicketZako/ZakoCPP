from typing import Literal

from pydantic import BaseModel, Field

from internal.config.autosave import AutoSaveConfig


class ProductTypeData(BaseModel):
    """
    票档信息
    """

    id: int = Field(default=0, description="票档 ID")
    name: str = Field(default="", description="票档名称")
    square: str = Field(default="", description="场次名称")
    price: int = Field(default=0, description="票档价格")
    purchaseNum: int = Field(default=0, description="可购买数量")
    remainderNum: int = Field(default=0, description="剩余数量")
    lockNum: int = Field(default=0, description="已锁定数量")
    realnameAuth: bool = Field(default=False, description="实名制购票")
    sellStartTime: int = Field(default=0, description="售票开始时间")
    sellEndTime: int = Field(default=0, description="售票结束时间")


class ProductMainData(BaseModel):
    """
    活动信息
    """

    id: int = Field(default=0, description="活动 ID")
    name: str = Field(default="", description="活动名称")


class ProductConfig(AutoSaveConfig):
    """
    票档数据
    """

    ticketMain: ProductMainData = Field(
        default_factory=ProductMainData, description="活动信息"
    )
    ticketType: ProductTypeData = Field(
        default_factory=ProductTypeData, description="票档信息"
    )
    ticketMethod: Literal["wx", "ali"] = Field(default="ali", description="购票方式")
