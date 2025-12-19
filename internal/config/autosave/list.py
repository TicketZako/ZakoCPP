from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from internal.config.manager import ConfigManager

T = TypeVar("T")


class AutoSaveList(list, Generic[T]):
    """
    自动保存列表
    """

    def __init__(
        self, items: list[T] | None = None, parent: "ConfigManager | None" = None
    ):
        super().__init__(items or [])
        self._parent_config: ConfigManager | None = parent

    def _save(self):
        """
        触发父级配置保存
        """
        parent = self._parent_config
        if (
            parent is not None
            and hasattr(parent, "_auto_save")
            and parent._auto_save
            and hasattr(parent, "_initialized")
            and parent._initialized
        ):
            try:
                parent.save()
            except Exception:
                pass

    def append(self, item: T) -> None:
        super().append(item)
        self._save()

    def extend(self, iterable: list[T]) -> None:
        super().extend(iterable)
        self._save()

    def insert(self, index: int, item: T) -> None:
        super().insert(index, item)
        self._save()

    def remove(self, item: T) -> None:
        super().remove(item)
        self._save()

    def pop(self, index: int = -1) -> T:
        result = super().pop(index)
        self._save()
        return result

    def clear(self) -> None:
        super().clear()
        self._save()

    def __setitem__(self, index: int | slice, value: T | list[T]) -> None:
        super().__setitem__(index, value)
        self._save()

    def __delitem__(self, index: int | slice) -> None:
        super().__delitem__(index)
        self._save()

    def __iadd__(self, other: list[T]) -> "AutoSaveList[T]":
        result = super().__iadd__(other)
        self._save()
        return result

    def __imul__(self, n: int) -> "AutoSaveList[T]":
        result = super().__imul__(n)
        self._save()
        return result
