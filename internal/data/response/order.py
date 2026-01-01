from typing import Any, ClassVar, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CreateOrderData(BaseModel):
    """
    创建订单 数据
    """

    outTradeNo: str = Field(default="Unknown", description="订单号")
    orderInfo: str = Field(default="", description="订单信息")

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def handle_order_id_aliases(cls, data: Any) -> Any:
        """
        处理订单号的多个字段名：outTradeNo 和 orderid
        如果数据内有任意一个满足就写入 outTradeNo
        """
        if isinstance(data, dict):
            if "orderid" in data and "outTradeNo" not in data:
                data["outTradeNo"] = data["orderid"]
            elif "orderid" in data and "outTradeNo" in data:
                if not data.get("outTradeNo"):
                    data["outTradeNo"] = data["orderid"]
        return data


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

    map: ClassVar[Dict[str, int]] = {
        "订单创建成功": 0,
        "抱歉，余票不足，请稍后再试！": 100000,
        "相同证件限购一张！": 300000,
        "系统繁忙，请稍后再试": 200000,
        "请求过于频繁，请稍后再试": 200001,
        "抢票通道拥挤，请稍后再试": 200002,
        "抢票通道拥挤，请您稍后再试": 200003,
        "请求错误: 302": 200010,  # redirect to 403
        "请求错误: 429": 200020,
        "请求错误: 502": 200020,
        "请求错误: 503": 200020,
        "请求错误: 504": 200020,
        "请求错误: 522": 200020,
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
