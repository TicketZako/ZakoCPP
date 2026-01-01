from asyncio import (
    AbstractEventLoop,
    new_event_loop,
    run_coroutine_threadsafe,
    set_event_loop,
)
from asyncio import sleep as async_sleep
from threading import Lock, Thread
from time import sleep
from typing import Optional

from pydglab_ws import Channel, DGLabWSServer, RetCode, StrengthOperationType

from internal.core.notification.external.dglab.pulse import PULSE_DATA
from internal.util import CliUtils, IPUtils, log


class DGLabManager:
    """
    DGLab 管理器
    """

    _instance: Optional["DGLabManager"] = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._server: Optional[DGLabWSServer] = None
        self._client = None
        self._loop: Optional[AbstractEventLoop] = None
        self._thread: Optional[Thread] = None
        self._is_running = False
        self._host = "0.0.0.0"
        self._port = 5678

    def init(self) -> None:
        """
        初始化服务
        """
        if self._is_running:
            return
        self._is_running = False
        self._server = None
        self._client = None
        self._loop = None
        self._thread = None

    def start(self) -> None:
        """
        启动服务
        """
        if self._is_running:
            return

        self._is_running = True
        self._loop = new_event_loop()
        set_event_loop(self._loop)
        self._thread = Thread(target=self._run_server, daemon=True)
        self._thread.start()

    def _run_server(self) -> None:
        """
        在后台线程中运行服务器
        """
        self._loop.run_until_complete(self._server_coroutine())

    async def _server_coroutine(self) -> None:
        """
        服务器协程
        """
        try:
            async with DGLabWSServer(self._host, self._port, 60) as server:
                self._server = server
                self._client = server.new_local_client()

                local_ip = IPUtils.get_local_ip()
                log.info("DGLab WebSocket 服务器已启动")
                log.info(f"服务器地址: ws://{local_ip}:{self._port}")

                async for data in self._client.data_generator(RetCode):
                    if data == RetCode.CLIENT_DISCONNECTED:
                        log.warning("App 已断开连接，等待重新连接...")
                        await self._client.rebind()
                        log.info("重新绑定成功")
        except Exception as e:
            log.error(f"DGLab 服务器运行出错: {e}")
            self._is_running = False

    def connect(self) -> None:
        """
        等待连接
        """
        if not self._is_running:
            log.warning("DGLab 服务器未启动，无法等待连接")
            return

        max_wait = 5
        waited = 0
        while not self._client and waited < max_wait:
            sleep(0.1)
            waited += 0.1

        if not self._client:
            log.warning("DGLab 服务器启动超时，无法等待连接")
            return

        if not self._client.not_bind:
            log.info("DGLab 已连接")
            return

        local_ip = IPUtils.get_local_ip()
        url = self._client.get_qrcode(f"ws://{local_ip}:{self._port}")

        try:
            CliUtils.print("", end="\n")
            CliUtils.print("=" * 60, color="cyan")
            CliUtils.print("DGLab 连接", color="cyan", size="large")
            CliUtils.print("=" * 60, color="cyan")
            CliUtils.print("", end="\n")
            CliUtils.print("DGLab WebSocket 服务器已启动", color="green", bold=True)
            CliUtils.print(f"服务器地址: ws://{local_ip}:{self._port}", color="yellow")
            CliUtils.print("", end="\n")
            CliUtils.print(
                "请用 DG-Lab App 扫描下方二维码以连接", color="cyan", bold=True
            )
            CliUtils.print("", end="\n")
        except ImportError:
            log.info("DGLab WebSocket 服务器已启动")
            log.info(f"请用 DG-Lab App 扫描二维码以连接: {url}")

        CliUtils.print_qrcode(url)

        try:
            CliUtils.print("", end="\n")
            CliUtils.print("等待 App 连接中...", color="yellow")
        except ImportError:
            log.info("等待 App 连接中...")

        if self._loop:
            future = run_coroutine_threadsafe(self._wait_for_bind(), self._loop)
            future.result()

    async def _wait_for_bind(self) -> None:
        """
        等待客户端绑定
        """
        if not self._client:
            return

        await self._client.bind()

        try:
            CliUtils.print("", end="\n")
            CliUtils.print(
                f"✅ 已与 App 成功绑定 (ID: {self._client.target_id})",
                color="green",
                bold=True,
            )
            CliUtils.print("=" * 60, color="cyan")
            CliUtils.print("", end="\n")
        except ImportError:
            log.info(f"已与 App {self._client.target_id} 成功绑定")

    def stop(self) -> None:
        """
        停止服务
        """
        self._is_running = False
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)  # noqa
        if self._thread:
            self._thread.join(timeout=1)

    def status(self) -> bool:
        """
        服务状态

        :return bool: 状态值
        """
        return (
            self._is_running and self._client is not None and not self._client.not_bind
        )

    @property
    def client(self):
        """
        获取客户端实例
        """
        return self._client

    @property
    def loop(self) -> Optional[AbstractEventLoop]:
        """
        获取事件循环
        """
        return self._loop

    def send_notification(
        self,
        pulses: list,
        strength: int,
        channel_str: str,
        interval: float,
    ) -> None:
        """
        发送通知（波形和强度）

        :param pulses: 波形名称列表
        :param strength: 强度值
        :param channel_str: 通道字符串 ("A" 或 "B")
        :param interval: 波形之间的间隔时间（秒）
        """
        if not self._is_running or not self._client or self._client.not_bind:
            raise ValueError("DGLab 客户端未连接，无法发送通知")

        if not pulses:
            raise ValueError("波形列表为空，无法发送通知")

        channel = Channel.A if channel_str == "A" else Channel.B

        if self._loop and self._loop.is_running():
            run_coroutine_threadsafe(
                self._send_multiple_pulses(channel, pulses, strength, interval),
                self._loop,
            )
        else:
            raise ValueError("DGLab 事件循环未运行，无法发送通知")

    async def _send_multiple_pulses(
        self,
        channel: Channel,
        pulses: list,
        strength: int,
        interval: float,
    ) -> None:
        """
        按顺序发送多个波形

        :param channel: 通道
        :param pulses: 波形名称列表
        :param strength: 强度值
        :param interval: 波形之间的间隔时间（秒）
        """
        if not self._client:
            raise ValueError("DGLab 客户端未连接")

        try:
            await self._client.set_strength(
                channel, StrengthOperationType.SET_TO, strength
            )

            pulse_names = []
            for i, pulse_name in enumerate(pulses):
                pulse_data = PULSE_DATA.get(pulse_name)
                if not pulse_data:
                    log.warning(f"未知的波形类型: {pulse_name}，跳过")
                    continue

                pulse_duration = len(pulse_data) * 0.1
                copies = max(1, int(1.0 / pulse_duration) + 1)
                pulse_data_extended = pulse_data * copies

                await self._client.add_pulses(channel, *pulse_data_extended)
                pulse_names.append(pulse_name)

                if i < len(pulses) - 1:
                    await async_sleep(interval)

            if pulse_names:
                log.info(
                    f"DGLab 通知已发送: 通道={channel.name}, 波形={', '.join(pulse_names)}, 强度={strength}"
                )
            else:
                log.warning("没有有效的波形被发送")
        except Exception as e:
            log.error(f"发送 DGLab 通知失败: {e}", exc_info=True)
            raise
