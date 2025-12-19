from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, PrivateAttr

from internal.config.autosave.list import AutoSaveList

if TYPE_CHECKING:
    from internal.config.manager import ConfigManager


class AutoSaveConfig(BaseModel):
    """
    自动保存配置基类
    """

    _parent_config: Optional["ConfigManager"] = PrivateAttr(default=None)

    def _should_save(self) -> bool:
        """
        判断是否应该触发保存
        """
        parent = getattr(self, "_parent_config", None)
        return (
            parent is not None
            and hasattr(parent, "_auto_save")
            and parent._auto_save
            and hasattr(parent, "_initialized")
            and parent._initialized
        )

    def _trigger_save(self):
        """
        触发父级配置保存
        """
        if self._should_save():
            try:
                self._parent_config.save()
            except Exception:
                pass

    def __setattr__(self, name: str, value) -> None:
        """
        设置属性并触发自动保存
        """
        if name.startswith("_"):
            super().__setattr__(name, value)
            return

        old_value = getattr(self, name, None)

        if isinstance(value, list):
            if not isinstance(value, AutoSaveList):
                parent = getattr(self, "_parent_config", None)
                value = AutoSaveList(value, parent=parent)

        super().__setattr__(name, value)

        parent = getattr(self, "_parent_config", None)
        if isinstance(value, BaseModel) and hasattr(value, "_parent_config"):
            if parent is not None:
                object.__setattr__(value, "_parent_config", parent)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, BaseModel) and hasattr(item, "_parent_config"):
                    if parent is not None:
                        object.__setattr__(item, "_parent_config", parent)

        if old_value != value:
            self._trigger_save()
