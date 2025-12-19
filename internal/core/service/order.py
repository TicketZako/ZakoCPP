from internal.client.api.order import OrderApi
from internal.config import configer
from internal.util import log


class OrderService:
    """
    订单服务
    """

    @staticmethod
    def create_order() -> int:
        """
        创建订单

        :return: 状态码
        """
        resp = OrderApi().create_order(
            method=configer.product.ticketMethod,
            ticket_type_id=configer.product.ticketType.id,
            ticket_count=configer.buyer.count,
            purchaser_ids=",".join([str(b.id) for b in configer.buyer.buyer]),
        )
        log.debug(f"订单创建: {resp.code} {resp.msg} {resp.data}")
        return resp.code
