import signal
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from internal.config import configer
from internal.interface.entrance import CliEntrance
from internal.util import SystemUtils, log


def signal_handler(signum, frame):
    """
    信号处理器，处理 Ctrl+C 等中断信号

    :param signum: 信号编号
    :param frame: 当前堆栈帧
    """
    log.info("收到退出信号，正在安全退出...")
    sys.exit(0)


def main():
    """
    主函数
    """
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, signal_handler)

    parser = ArgumentParser(
        description="ComicUp Ticketer - 票务抢票工具",
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--encrypt",
        type=str,
        choices=["true", "false"],
        help="配置文件加密设置（true/false），默认使用配置文件中的设置",
    )

    args = parser.parse_args()

    try:
        if args.encrypt is not None:
            encrypt_value = args.encrypt.lower() == "true"
            old_auto_save = configer._auto_save
            configer._auto_save = False
            try:
                configer.setting.isEncrypt = encrypt_value
            finally:
                configer._auto_save = old_auto_save
            log.info(
                f"配置文件加密已{'启用' if encrypt_value else '禁用'}（通过命令行参数）"
            )

        configer.load()

        CliEntrance.enter()

    except KeyboardInterrupt:
        log.info("用户中断，正在退出...")
        SystemUtils.exit(0)
    except Exception as e:
        log.error(f"程序运行出错: {e}")
        SystemUtils.exit(1)


if __name__ == "__main__":
    main()
