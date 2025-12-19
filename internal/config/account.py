from typing import Optional

from pydantic import Field

from internal.config.autosave import AutoSaveConfig


class AccountConfig(AutoSaveConfig):
    """
    账号配置
    """

    account: str = Field(default="", description="账号")
    password: str = Field(default="", description="密码")
    token: Optional[str] = Field(default=None, description="token")
