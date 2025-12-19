from internal.client.api.user import UserApi
from internal.config import configer
from internal.error import LoginStatusCode


class UserService:
    """
    用户信息服务
    """

    @staticmethod
    def login() -> int:
        """
        登入接口

        :return: 状态码
        """
        if not configer.account.account:
            return LoginStatusCode.MissingAccount

        if not configer.account.password:
            return LoginStatusCode.MissingPassword

        resp = UserApi.query_login(configer.account.account, configer.account.password)
        if resp.code == 0:
            configer.account.token = resp.data.token
            return LoginStatusCode.Success

        return LoginStatusCode.LoginError
