from internal.client.api import cpp_client_info, cpp_device_info, net_client
from internal.data.response import CreateOrderResponse, CreateOrderResponsePatcher
from internal.util import Sign, log


class OrderApi:
    """
    订单接口
    """

    @staticmethod
    def create_order(
        method: str,
        ticket_type_id: int,
        ticket_count: int,
        purchaser_ids: str,
    ) -> CreateOrderResponse:
        """
        创建订单

        :param method: 支付方式
        :param ticket_type_id: 票档 ID
        :param ticket_count: 票数
        :param purchaser_ids: 购票人 ID 列表

        :return CreateOrderResponse: 订单请求信息
        """

        url = ""

        nonce, timestamp, sign = Sign.generate_sign(ticket_type_id)

        params = {}
        json_data = {}
        resp = net_client.request("post", url, json=json_data, params=params)

        result = resp.data.get("isSuccess", False)
        if result:
            resp.code = 0
        else:
            resp.code = CreateOrderResponsePatcher.code(resp.msg)

        log.debug(f"订单创建: {resp.code} {resp.msg}")

        return CreateOrderResponse(
            code=resp.code,
            msg=resp.msg,
            data=resp.data.get("result", None),
        )
