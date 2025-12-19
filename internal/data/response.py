from typing import Any, ClassVar, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ResponseData(BaseModel):
    """
    请求响应 返回结果
    """

    code: int = Field(description="状态码")
    msg: Optional[str] = Field(default="", description="提示信息")
    data: Optional[Dict[Any, Any] | List] = Field(default=None, description="数据")


class LoginToken(BaseModel):
    """
    登录 Token
    """

    token: Optional[str] = Field(default=None, description="Token")


class LoginResponse(BaseModel):
    """
    登录 返回结果
    """

    code: int = Field(description="状态码")
    msg: Optional[str] = Field(default="", description="提示信息")
    data: Optional[LoginToken] = Field(default=None, description="数据")


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


class CreateOrderData(BaseModel):
    """
    创建订单 数据
    """

    outTradeNo: str = Field(description="订单号")
    orderInfo: str = Field(description="订单信息")

    model_config = ConfigDict(extra="ignore")


class CreateOrderResponse(BaseModel):
    """
    创建订单 返回结果
    """

    code: int = Field(description="状态码")
    msg: Optional[str] = Field(default="", description="提示信息")
    data: Optional[CreateOrderData] = Field(default=None, description="数据")


class CreateOrderResponsePatcher(BaseModel):
    """
    创建订单 状态码 映射
    """

    map: ClassVar[dict[str, int]] = {
        "订单创建成功": 0,
        "相同证件限购一张！": 300000,
        "请求过于频繁，请稍后再试": 200000,
        "系统繁忙，请稍后再试": 200001,
        "请求错误: 302": 200002,
        "抱歉，余票不足，请稍后再试！": 100000,
    }

    @staticmethod
    def code(msg: str) -> int:
        """
        依据 msg 返回 code

        :param msg: 提示信息

        :return int: code 值
        """
        if msg in CreateOrderResponsePatcher.map:
            return CreateOrderResponsePatcher.map[msg]
        return 114514
