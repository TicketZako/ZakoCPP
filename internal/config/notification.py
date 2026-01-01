from typing import List, Literal, Optional, Union

from pydantic import Field

from internal.config.autosave import AutoSaveConfig


class DesktopConfig(AutoSaveConfig):
    """
    桌面通知配置
    """


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


class GotifyConfig(AutoSaveConfig):
    """
    Gotify 配置
    """

    token: str = Field(default="", description="Gotify Token")
    host: Optional[str] = Field(default=None, description="Gotify 地址")
    port: Optional[int] = Field(default=None, description="Gotify 端口")
    path: str = Field(default="/", description="Gotify 完整路径")
    use_tls: bool = Field(default=False, description="是否使用 TLS/SSL")


class DingtalkConfig(AutoSaveConfig):
    """
    钉钉配置
    """

    token: str = Field(default="", description="钉钉 Token")


class EmailConfig(AutoSaveConfig):
    """
    Email 配置
    """

    smtp_host: str = Field(default="", description="SMTP 服务器地址")
    smtp_port: int = Field(default=587, description="SMTP 服务器端口")
    smtp_user: str = Field(default="", description="SMTP 用户名")
    smtp_pass: str = Field(default="", description="SMTP 密码")
    use_tls: bool = Field(default=True, description="是否使用 TLS/SSL")
    from_addr: str = Field(default="", description="发件人邮箱地址")
    to_addr: Union[str, List[str]] = Field(
        default="", description="收件人邮箱地址（支持多个，用逗号分隔或列表）"
    )


class PushmeConfig(AutoSaveConfig):
    """
    PushMe 配置
    """

    token: str = Field(default="", description="PushMe Token")


class PushdeerConfig(AutoSaveConfig):
    """
    PushDeer 配置
    """

    push_key: str = Field(default="", description="PushDeer Push Key")
    host: Optional[str] = Field(
        default=None, description="PushDeer 服务器地址（可选，留空使用默认服务）"
    )
    port: Optional[int] = Field(default=None, description="PushDeer 服务器端口（可选）")
    use_tls: bool = Field(default=False, description="是否使用 SSL/TLS")


class ServerchanConfig(AutoSaveConfig):
    """
    ServerChan 配置
    """

    token: str = Field(default="", description="ServerChan Token")


class TelegramConfig(AutoSaveConfig):
    """
    Telegram 配置
    """

    bot_token: str = Field(default="", description="Telegram Bot Token")
    chat_id: str = Field(default="", description="Telegram Chat ID")


class SlackConfig(AutoSaveConfig):
    """
    Slack 配置
    """

    # Webhook 方式（三个 token）
    token_a: str = Field(
        default="", description="Slack Webhook Token A（Webhook 方式）"
    )
    token_b: str = Field(
        default="", description="Slack Webhook Token B（Webhook 方式）"
    )
    token_c: str = Field(
        default="", description="Slack Webhook Token C（Webhook 方式）"
    )
    # OAuth 方式（一个 token）
    oauth_token: str = Field(default="", description="Slack OAuth Token（OAuth 方式）")


class WecombotConfig(AutoSaveConfig):
    """
    WeCom Bot 配置
    """

    bot_key: str = Field(default="", description="WeCom Bot Key")


class DglabConfig(AutoSaveConfig):
    """
    DGLab 配置
    """

    pulses: List[
        Literal[
            "呼吸",
            "潮汐",
            "连击",
            "快速按捏",
            "按捏渐强",
            "心跳节奏",
            "压缩",
            "节奏步伐",
            "颗粒摩擦",
            "渐变弹跳",
            "波浪涟漪",
            "雨水冲刷",
            "变速敲击",
            "信号灯",
            "挑逗1",
            "挑逗2",
        ]
    ] = Field(
        default_factory=lambda: ["呼吸"],
        description="波形类型列表（按顺序发送）",
    )
    strength: int = Field(default=50, ge=0, le=100, description="强度（0-100）")
    channel: Literal["A", "B"] = Field(default="A", description="通道选择")
    interval: float = Field(default=0.5, ge=0, description="波形之间的间隔时间（秒）")


class NotificationConfig(AutoSaveConfig):
    """
    通知配置
    """

    isEnable: bool = Field(default=False, description="是否启用通知")
    methods: List[
        Literal[
            "desktop",
            "pushplus",
            "bark",
            "gotify",
            "dingtalk",
            "mailto",
            "pushme",
            "pushdeer",
            "schan",
            "tgram",
            "slack",
            "wecombot",
            "dglab",
        ]
    ] = Field(
        default_factory=list,
        description="通知方式 (protocol)",
    )

    desktop: DesktopConfig = Field(
        default_factory=DesktopConfig,
        description="桌面通知配置",
    )
    pushplus: PushplusConfig = Field(
        default_factory=PushplusConfig,
        description="PushPlus 配置",
    )
    bark: BarkConfig = Field(
        default_factory=BarkConfig,
        description="Bark 配置",
    )
    gotify: GotifyConfig = Field(
        default_factory=GotifyConfig,
        description="Gotify 配置",
    )
    dingtalk: DingtalkConfig = Field(
        default_factory=DingtalkConfig,
        description="钉钉配置",
    )
    email: EmailConfig = Field(
        default_factory=EmailConfig,
        description="Email 配置",
    )
    pushme: PushmeConfig = Field(
        default_factory=PushmeConfig,
        description="PushMe 配置",
    )
    pushdeer: PushdeerConfig = Field(
        default_factory=PushdeerConfig,
        description="PushDeer 配置",
    )
    serverchan: ServerchanConfig = Field(
        default_factory=ServerchanConfig,
        description="ServerChan 配置",
    )
    telegram: TelegramConfig = Field(
        default_factory=TelegramConfig,
        description="Telegram 配置",
    )
    slack: SlackConfig = Field(
        default_factory=SlackConfig,
        description="Slack 配置",
    )
    wecombot: WecombotConfig = Field(
        default_factory=WecombotConfig,
        description="WeCom Bot 配置",
    )
    dglab: DglabConfig = Field(
        default_factory=DglabConfig,
        description="DGLab 配置",
    )
