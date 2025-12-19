from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field, PrivateAttr, model_validator
from yaml import dump, safe_load

from internal.config.account import AccountConfig
from internal.config.autosave import AutoSaveList
from internal.config.buyer import BuyerConfig
from internal.config.notification import NotificationConfig
from internal.config.product import ProductConfig
from internal.config.setting import SettingConfig
from internal.util.crypto import AES
from internal.util.system import SystemUtils


class ConfigManager(BaseModel):
    """
    配置管理器
    """

    setting: SettingConfig = Field(default_factory=SettingConfig)
    account: AccountConfig = Field(default_factory=AccountConfig)
    buyer: BuyerConfig = Field(default_factory=BuyerConfig)
    notification: NotificationConfig = Field(default_factory=NotificationConfig)
    product: ProductConfig = Field(default_factory=ProductConfig)

    _config_path: Optional[Path] = PrivateAttr(default=None)
    _machine_id: Optional[str] = PrivateAttr(default=None)
    _auto_save: bool = PrivateAttr(default=True)
    _initialized: bool = PrivateAttr(default=False)

    def __init__(
        self, config_path: Optional[Path] = None, auto_save: bool = True, **data
    ):
        """
        初始化配置管理器

        :param config_path: 配置文件路径，如果不提供则使用默认路径
        :param auto_save: 是否自动保存（更新时自动写入）
        """
        super().__init__(**data)
        self._config_path = config_path or SystemUtils.get_config_path() / "config.yaml"
        self._machine_id = SystemUtils.get_machine_id()
        self._auto_save = auto_save
        self._initialized = True
        self._setup_parent_refs()

    @model_validator(mode="after")
    def _mark_initialized(self):
        """
        标记为已初始化并应用配置
        """
        if not self._initialized:
            self._initialized = True
            self._apply_config()
        return self

    def init_config(self, force: bool = False) -> "ConfigManager":
        """
        初始化配置文件

        :param force: 是否强制初始化（覆盖已存在的文件）
        :return: 自身实例（支持链式调用）
        """
        self._config_path.parent.mkdir(parents=True, exist_ok=True)

        if self._config_path.exists() and not force:
            return self

        old_auto_save = self._auto_save
        self._auto_save = False
        try:
            self.save()
        finally:
            self._auto_save = old_auto_save

        return self

    def load(self) -> "ConfigManager":
        """
        从文件加载配置

        :return: 自身实例（支持链式调用）
        """
        old_auto_save = self._auto_save
        self._auto_save = False

        try:
            if not self._config_path.exists():
                self.init_config()
                self._apply_config()
                return self

            try:
                with open(self._config_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()

                if self.setting.isEncrypt:
                    try:
                        decrypted_content = AES.decrypt(content, self._machine_id)
                        config_data = safe_load(decrypted_content)
                    except Exception:
                        config_data = safe_load(content)
                else:
                    config_data = safe_load(content)

                if config_data is None:
                    config_data = {}

                for key, value in config_data.items():
                    if not hasattr(self, key):
                        continue

                    if isinstance(value, dict):
                        config_obj = getattr(self, key)
                        if isinstance(config_obj, BaseModel) and hasattr(
                            config_obj, "model_validate"
                        ):
                            updated_obj = config_obj.model_validate(value)
                            setattr(self, key, updated_obj)
                        else:
                            setattr(self, key, value)
                    else:
                        setattr(self, key, value)

                self._setup_parent_refs()
                self._apply_config()

            except Exception as e:
                raise ValueError(f"配置文件加载失败: {e}")
        finally:
            self._auto_save = old_auto_save

        return self

    def save(self) -> "ConfigManager":
        """
        保存配置到文件

        :return: 自身实例（支持链式调用）
        """
        self._config_path.parent.mkdir(parents=True, exist_ok=True)

        config_dict = self.model_dump(exclude_none=False)

        yaml_content = dump(
            config_dict, default_flow_style=False, allow_unicode=True, sort_keys=False
        )

        if self.setting.isEncrypt:
            file_content = AES.encrypt(yaml_content, self._machine_id)
        else:
            file_content = yaml_content

        temp_path = self._config_path.with_suffix(self._config_path.suffix + ".tmp")
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(file_content)

            temp_path.replace(self._config_path)
        except Exception as e:
            if temp_path.exists():
                temp_path.unlink()
            raise RuntimeError(f"配置文件保存失败: {e}")

        return self

    def update(self, **kwargs):
        """
        更新配置并自动保存

        :param kwargs: 要更新的配置项
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        if self._auto_save:
            self.save()

    def _apply_config(self):
        """
        应用配置项到系统
        """
        try:
            from internal.util.logger import log_settings, log

            log_settings.DEBUG = self.setting.isDebug
            log.update_loggers()
        except Exception:
            pass

    def _setup_parent_refs(self):
        """
        为所有嵌套配置对象设置父级引用
        """
        if not self._initialized:
            return

        for attr_name in ["setting", "account", "buyer", "notification", "product"]:
            if hasattr(self, attr_name):
                config_obj = getattr(self, attr_name)
                self._setup_refs_recursive(config_obj, self)

    def _setup_refs_recursive(self, obj: Any, parent: "ConfigManager"):
        """
        递归设置父级引用
        """
        if isinstance(obj, BaseModel) and hasattr(obj, "_parent_config"):
            object.__setattr__(obj, "_parent_config", parent)
            for field_name in obj.model_fields.keys():
                field_value = getattr(obj, field_name, None)
                if isinstance(field_value, list) and not isinstance(
                    field_value, AutoSaveList
                ):
                    auto_save_list = AutoSaveList(field_value, parent=parent)
                    object.__setattr__(obj, field_name, auto_save_list)
                    field_value = auto_save_list
                self._setup_refs_recursive(field_value, parent)

        elif isinstance(obj, list):
            if isinstance(obj, AutoSaveList):
                object.__setattr__(obj, "_parent_config", parent)
            for item in obj:
                self._setup_refs_recursive(item, parent)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        设置属性并处理自动保存
        """
        old_value = (
            getattr(self, name, None)
            if hasattr(self, "_initialized") and self._initialized
            else None
        )

        if self._initialized and isinstance(value, list):
            if not isinstance(value, AutoSaveList):
                value = AutoSaveList(value, parent=self)

        super().__setattr__(name, value)

        if self._initialized:
            if isinstance(value, BaseModel) and hasattr(value, "_parent_config"):
                object.__setattr__(value, "_parent_config", self)
                self._setup_refs_recursive(value, self)
            elif isinstance(value, AutoSaveList):
                object.__setattr__(value, "_parent_config", self)

        if (
            self._initialized
            and name == "setting"
            and isinstance(value, SettingConfig)
            and old_value != value
        ):
            self._apply_config()

        if (
            self._auto_save
            and self._initialized
            and name
            not in ("_config_path", "_machine_id", "_auto_save", "_initialized")
            and old_value != value
        ):
            try:
                self.save()
            except Exception:
                pass
