from internal.client.api import cpp_client_info, cpp_device_info, net_client
from internal.data.response import QueryBuyerResponse
from internal.error import GetBuyerError


class BuyerApi:
    """
    购买人信息 接口
    """

    @staticmethod
    def query_buyer() -> QueryBuyerResponse:
        """
        购票人信息

        :return QueryBuyerResponse: 购票人信息
        """
        url = ""
        params = {}
        resp = net_client.request("get", url, params=params)

        if resp.code != -1:
            raise GetBuyerError("获取购票人信息失败")

        return QueryBuyerResponse(
            code=0,
            msg="获取购票人信息成功",
            data=resp.data,
        )
