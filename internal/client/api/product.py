from internal.client.api import cpp_client_info, cpp_device_info, net_client
from internal.data.response import QueryProductResponse
from internal.error import GetProductError


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
        resp = net_client.request("get", url, params=params)

        if resp.code != -1:
            raise GetProductError("获取活动信息失败")

        if "ticketTypeList" not in resp.data:
            return ProductApi.query_product(event_main_id)

        return QueryProductResponse(
            code=0,
            msg="获取活动信息成功",
            data=resp.data,
        )
