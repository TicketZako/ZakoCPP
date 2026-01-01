from typing import Any, Dict, Literal, Optional

from httpx import Client, Request, Response

from internal.data.response import RawResponse
from internal.util import log


class NetManager:
    """
    网络管理器
    """

    def __init__(
        self,
        timeout: int | float = 5.0,
        headers: Optional[Dict[Any, Any]] = None,
        cookies: Optional[Dict[Any, Any]] = None,
        proxy: Optional[str] = None,
    ) -> None:
        self.client = Client(
            timeout=timeout,
            headers=headers,
            cookies=cookies,
            proxy=proxy,
            follow_redirects=False,
            http2=True,
            verify=False,
            event_hooks={
                "request": [NetManager.request_hook],
                "response": [NetManager.response_hook],
            },
        )

        self.token: str = ""

    def get(
        self,
        key: Literal["header", "cookie"] = "header",
    ) -> Dict[Any, Any]:
        """
        刷新 Cookie 或者 Header

        :param key: 刷新键
        :return Dict[Any, Any]: 数据
        """
        if key == "header":
            header = {
                key.decode("utf-8"): value.decode("utf-8")
                for key, value in self.client.headers.raw
            }
            return header
        elif key == "cookie":
            return dict(self.client.cookies)
        else:
            return dict()

    def refresh(
        self,
        key: Literal["header", "cookie"] = "header",
        value: Optional[Dict[Any, Any]] = None,
    ) -> None:
        """
        刷新 Cookie 或者 Header

        :param key: 刷新键
        :param value: 刷新值
        """

        if key == "header":
            self.client.headers.clear()
            self.client.headers.update(value)
        elif key == "cookie":
            self.client.cookies.clear()
            for key, value in value.items():
                self.client.cookies.set(key, value, domain=".allcpp.cn")

    def request(
        self,
        method: Literal["get", "post", "patch"] = "get",
        url: Optional[str] = None,
        /,
        **kwargs,
    ) -> RawResponse:
        """
        请求器
        """
        methods = {
            "get": self.client.get,
            "post": self.client.post,
            "patch": self.client.patch,
        }

        if method not in methods:
            log.warning("这是什么方式喵？")
            return RawResponse(code=114514, msg="未知的请求方式")

        try:
            resp: Response = methods[method](url=url, **kwargs)  # noqa
            if resp.status_code == 200:
                if "application/json" in dict(resp.headers)["content-type"]:
                    resp = resp.json()
                    return RawResponse(
                        code=-1,
                        msg=resp.get("message", "") if isinstance(resp, dict) else "",
                        data=resp,
                    )
            elif resp.status_code == 302:
                return RawResponse(code=-1, msg=f"请求错误: {resp.status_code}")
            return RawResponse(code=114514, msg=f"请求错误: {resp.status_code}")
        except Exception as e:
            return RawResponse(code=114514, msg=f"请求错误: {e}")

    @staticmethod
    def request_hook(request: Request) -> None:
        """
        请求事件钩子
        """
        log.debug(
            "【Request请求】"
            f" 地址: {request.url.copy_with(params=None)}"
            f" 方法: {request.method}"
            f" 参数: {request.url.params}"
            f" 内容: {request.content.decode('utf-8')}"
        )

    @staticmethod
    def response_hook(response: Response) -> None:
        """
        响应事件钩子
        """
        log.debug(
            "【Request响应】"
            f" 地址: {response.request.url.copy_with(params=None)}"
            f" 状态码: {response.status_code}"
            f" 内容: {response.read().decode('utf-8')}"
        )

        if response.status_code != 200:
            log.error(f"【Request响应】请求错误, 状态码: {response.status_code}")
