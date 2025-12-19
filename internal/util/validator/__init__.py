import re
from typing import Optional


class ValidatorUtils:
    """
    验证工具类
    """

    @staticmethod
    def validate_phone(phone: Optional[str]) -> bool:
        """
        验证手机号格式

        :param phone: 手机号
        :return: 是否有效
        """
        if not phone:
            return False
        # 中国手机号验证：11位数字，以1开头，第二位为3-9
        pattern = r"^1[3-9]\d{9}$"
        return bool(re.match(pattern, phone))

    @staticmethod
    def validate_email(email: Optional[str]) -> bool:
        """
        验证邮箱格式

        :param email: 邮箱地址
        :return: 是否有效
        """
        if not email:
            return False
        # 简单的邮箱格式验证
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_password(password: Optional[str], min_length: int = 6) -> bool:
        """
        验证密码格式

        :param password: 密码
        :param min_length: 最小长度
        :return: 是否有效
        """
        if not password:
            return False
        return len(password) >= min_length

    @staticmethod
    def validate_not_empty(
        value: Optional[str], field_name: str = "字段"
    ) -> tuple[bool, Optional[str]]:
        """
        验证字段非空

        :param value: 要验证的值
        :param field_name: 字段名称，用于错误提示
        :return: (是否有效, 错误信息)
        """
        if not value or not value.strip():
            return False, f"{field_name}不能为空"
        return True, None
