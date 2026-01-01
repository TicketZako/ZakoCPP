from internal.client.net import net_manager
from internal.data.response import QueryBuyerResponse
from internal.util import log


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
        resp = net_manager.request("get", url, params=params)

        if resp.code != -1:
            log.error(f"获取购票人信息失败: {resp.msg}")
            return QueryBuyerResponse(
                code=resp.code,
                msg=resp.msg,
                data=None,
            )

        return QueryBuyerResponse(
            code=0,
            msg="获取购票人信息成功",
            data=resp.data,
        )
