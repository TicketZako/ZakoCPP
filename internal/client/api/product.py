from internal.client.net import net_manager
from internal.data.response import QueryProductResponse
from internal.util import log


class ProductApi:
    """
    票务接口
    """

    @staticmethod
    def query_product(event_main_id: int) -> QueryProductResponse:
        """
        活动信息

        :param event_main_id: 活动 ID

        :return QueryProductResponse: 活动信息
        """
        url = ""
        params = {}
        headers = {}
        resp = net_manager.request("get", url, params=params, headers=headers)

        if resp.code != -1:
            log.error(f"获取活动信息失败: {resp.msg}")
            return QueryProductResponse(
                code=resp.code,
                msg=resp.msg,
                data=None,
            )

        if "ticketTypeList" not in resp.data:
            return ProductApi.query_product(event_main_id)

        return QueryProductResponse(
            code=0,
            msg="获取活动信息成功",
            data=resp.data,
        )
