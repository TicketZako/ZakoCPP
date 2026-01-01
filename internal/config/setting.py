from pydantic import Field

from internal.config.autosave import AutoSaveConfig


class SettingConfig(AutoSaveConfig):
    """
    系统配置
    """

    isDebug: bool = Field(default=False, description="是否启用调试模式")
    isEncrypt: bool = Field(default=True, description="是否启用加密模式")
    maxConsecutiveRequest: int = Field(default=10, description="初始连续请求次数")
    riskedInterval: int = Field(default=60000, description="风控等待间隔 (ms)")
    refreshInterval: int = Field(default=150, description="检查余票间隔 (ms)")
