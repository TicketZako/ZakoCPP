from typing import Any, Dict
from urllib.parse import parse_qs, unquote


class ParserUtils:
    """
    解析工具类
    """

    @staticmethod
    def unmarshal_query(string: str) -> Dict[str, Any]:
        """
        解析 query 参数字符串

        :param string: 参数字符串

        :return Dict[str, Any]: 参数字典
        """
        params = parse_qs(string, keep_blank_values=True)

        result = {}
        for key, val in params.items():
            if isinstance(val, list) and len(val) > 0:
                result[key] = unquote(val[0])
            else:
                result[key] = val

        return result
