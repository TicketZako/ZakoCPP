class LoginStatusCode:
    """
    登录状态码
    """

    Success: int = 0
    LoginError: int = 200000
    MissingAccount: int = 300000
    MissingPassword: int = 300001
    Error: int = 999999


class BuyerStatusCode:
    """
    购买人信息 状态码
    """

    Success: int = 0
    MissingBuyer: int = 300000
    Error: int = 999999


class ProductStatusCode:
    """
    票务信息状态码
    """

    Success: int = 0
    NoStock: int = 100000
    Inactive: int = 300000
    Error: int = 999999


class OrderStatusCode:
    """
    票务状态码
    """

    Success: int = 0
    NoStock: int = 100000
    RequestLimited1: int = 200000
    RequestLimited2: int = 200001
    RequestLimited3: int = 200002
    RequestLimited4: int = 200003
    RequestBlocked: int = 200010
    HTTPError: int = 200020
    OrderDuplicated: int = 300000
    Error: int = 999999
