from internal.config import configer
from internal.core.service import UserService
from internal.error import LoginStatusCode
from internal.util import CliUtils, PrivacyUtils, SystemUtils, ValidatorUtils, log


class CliLogin:
    """
    登录交互界面
    """

    @staticmethod
    def account_step():
        """
        用户账号输入
        """
        while True:
            default_account = None
            if configer.account.account:
                masked_account = PrivacyUtils.mask_phone(configer.account.account)
                default_account = masked_account

            account = CliUtils.inquire(
                type="Text",
                message="请输入手机号",
                default=default_account,
            )

            if not account:
                CliUtils.print("手机号不能为空", color="red")
                continue

            if not ValidatorUtils.validate_phone(account):
                CliUtils.print("手机号格式不正确，请输入11位有效手机号", color="yellow")
                continue

            configer.account.account = account
            break

    @staticmethod
    def password_step():
        """
        密码输入
        """
        while True:
            password = CliUtils.inquire(
                type="Password",
                message="请输入密码",
            )

            if not password:
                CliUtils.print("密码不能为空", color="red")
                continue

            configer.account.password = password
            break

    @staticmethod
    def _get_error_message(status_code: int) -> str:
        """
        获取错误信息

        :param status_code: 状态码
        :return: 错误信息
        """
        error_messages = {
            LoginStatusCode.MissingAccount: "账号不能为空",
            LoginStatusCode.MissingPassword: "密码不能为空",
            LoginStatusCode.LoginError: "登录失败，请检查账号或密码是否正确",
        }
        return error_messages.get(status_code, "未知错误")

    @staticmethod
    def generate():
        """
        配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("账户登录", color="blue", size="large", style="underline")
        CliUtils.print("", end="\n")

        # 输入账号和密码
        CliLogin.account_step()
        CliLogin.password_step()

        # 尝试登录
        CliUtils.print("", end="\n")
        CliUtils.print("正在登录...", color="cyan")

        status_code = UserService.login()

        if status_code != LoginStatusCode.Success:
            CliUtils.print("", end="\n")
            error_msg = CliLogin._get_error_message(status_code)
            CliUtils.print(f"❌ {error_msg}", color="red", bold=True)
            log.error(f"登录失败: {error_msg} (状态码: {status_code})")
            CliUtils.print("", end="\n")

            # 询问是否重试
            retry = CliUtils.inquire(
                type="Confirm",
                message="是否重新尝试登录？",
                default=False,
            )

            if retry:
                CliLogin.generate()
            else:
                SystemUtils.exit(1)
        else:
            CliUtils.print("", end="\n")
            CliUtils.print("✅ 登录成功！", color="green", bold=True)
            log.info("登录成功")
            CliUtils.print("", end="\n")
