from typing import List

from pydantic import BaseModel, Field

from internal.config.autosave import AutoSaveConfig


class BuyerData(BaseModel):
    """
    购票人数据
    """

    id: int = Field(description="购票人 ID")
    realname: str = Field(description="购票人姓名")
    idcard: str = Field(description="购票人证件号码")
    mobile: str = Field(description="购票人手机号")
    validType: int = Field(description="证件类型")


class BuyerConfig(AutoSaveConfig):
    """
    购票人配置
    """

    buyer: List[BuyerData] = Field(default_factory=list, description="购票人列表")
    count: int = Field(default=0, description="购票人数")
