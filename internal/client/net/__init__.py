from typing import Any, Dict, Literal, Optional

from httpx import Client, HTTPStatusError, Request, RequestError, Response, StreamError

from internal.data.response import ResponseData
from internal.util import log


class NetClient:
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
            follow_redirects=True,
            http2=True,
            verify=False,
            event_hooks={
                "request": [NetClient.request_hook],
                "response": [NetClient.response_hook],
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
    ) -> ResponseData:
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
            return ResponseData(code=114514, msg="未知的请求方式")

        try:
            resp: Response = methods[method](url=url, **kwargs)  # noqa
            if resp.status_code == 200:
                if "application/json" in dict(resp.headers)["content-type"]:
                    log.debug(resp.json())
                    return ResponseData(
                        code=-1,
                        msg=resp.json().get("message", "")
                        if isinstance(resp.json(), dict)
                        else "",
                        data=resp.json(),
                    )
            elif resp.status_code == 204:
                return ResponseData(code=0, msg="请求成功")
            return ResponseData(code=114514, msg=f"请求错误: {resp.status_code}")
        except (
            RequestError,
            HTTPStatusError,
            StreamError,
        ) as e:
            return ResponseData(code=114514, msg=f"请求错误: {e}")

    @staticmethod
    def request_hook(request: Request) -> None:
        """
        请求事件钩子
        """
        log.debug(
            f"【Request请求】地址: {request.url} 方法: {request.method} 内容: {request.content} 请求参数: {request.read()}"
        )

    @staticmethod
    def response_hook(response: Response) -> None:
        """
        响应事件钩子
        """
        request = response.request
        log.debug(
            f"【Request响应】地址: {request.url} 状态码: {response.status_code} 返回: {response.read()}"
        )

        if response.status_code != 200:
            log.error(f"【Request响应】请求错误, 状态码: {response.status_code}")
