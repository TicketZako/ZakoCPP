class PrivacyUtils:
    """
    隐私信息处理工具类
    """

    @staticmethod
    def mask_phone(phone: str) -> str:
        """
        屏蔽手机号中间4位

        :param phone: 手机号
        :return: 屏蔽后的手机号，例如：138****5678
        """
        if not phone or len(phone) != 11:
            return phone
        return f"{phone[:3]}****{phone[7:]}"

    @staticmethod
    def mask_idcard(idcard: str) -> str:
        """
        屏蔽身份证号，只显示前4位和后4位

        :param idcard: 身份证号
        :return: 屏蔽后的身份证号，例如：1101**********1234
        """
        if not idcard or len(idcard) < 8:
            return idcard
        return f"{idcard[:4]}{'*' * (len(idcard) - 8)}{idcard[-4:]}"

    @staticmethod
    def mask_token(token: str) -> str:
        """
        屏蔽Token，只显示前4位和后4位

        :param token: Token
        :return: 屏蔽后的Token，例如：abcd****efgh
        """
        if not token or len(token) < 8:
            return "****"
        return f"{token[:4]}****{token[-4:]}"
