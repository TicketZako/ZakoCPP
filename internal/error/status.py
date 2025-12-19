class LoginStatusCode:
    """
    登录状态码
    """

    Success: int = 0
    LoginError: int = 200000
    MissingAccount: int = 300000
    MissingPassword: int = 300001


class BuyerStatusCode:
    """
    购买人信息 状态码
    """

    Success: int = 0
    MissingBuyer: int = 300000


class ProductStatusCode:
    """
    票务信息状态码
    """

    Success: int = 0
    NoStock: int = 100000


class OrderStatusCode:
    """
    票务状态码
    """

    Success: int = 0
    NoStock: int = 100000
    RequestLimited: int = 200000
    RequestRisked: int = 200001
    RequestBlocked: int = 200002
    OrderDuplicated: int = 300000
