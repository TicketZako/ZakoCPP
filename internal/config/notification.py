from typing import List, Literal

from pydantic import Field

from internal.config.autosave import AutoSaveConfig


class PushplusConfig(AutoSaveConfig):
    """
    PushPlus 配置
    """

    token: str = Field(default="", description="PushPlus Token")


class BarkConfig(AutoSaveConfig):
    """
    Bark 配置
    """

    token: str = Field(default="", description="Bark Token")
    level: Literal["passive", "timeSensitive", "active", "critical"] = Field(
        default="passive", description="Bark 通知等级"
    )


class NotificationConfig(AutoSaveConfig):
    """
    通知配置
    """

    isEnable: bool = Field(default=False, description="是否启用通知")
    notifyMethod: List[
        Literal[
            "pushplus",
            "bark",
        ]
    ] = Field(
        default_factory=list,
        description="通知方式",
    )

    pushplus: PushplusConfig = Field(
        default_factory=PushplusConfig,
        description="PushPlus 配置",
    )
    bark: BarkConfig = Field(
        default_factory=BarkConfig,
        description="Bark 配置",
    )
