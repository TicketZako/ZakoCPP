from internal.config import configer
from internal.core.task import Task
from internal.util import CliUtils, log


class CliLaunch:
    """
    票务选购
    """

    @staticmethod
    def generate():
        """
        配置窗口
        """
        if not configer.buyer.buyer:
            log.error("请先配置购买人信息")
            return

        if not configer.product.ticketMain.id or not configer.product.ticketType.id:
            log.error("请先配置产品信息")
            return

        CliUtils.print("", end="\n")
        CliUtils.print("选票配置完成，准备启动抢票任务", color="green", size="large")
        CliUtils.print("", end="\n")

        confirm = CliUtils.inquire(
            type="Confirm",
            message="是否立即启动抢票任务？",
            default=True,
        )

        if not confirm:
            log.info("已取消启动任务")
            return

        log.info("正在启动抢票任务...")
        task = Task()
        success = task.run()

        if success:
            log.info("任务执行成功")
        else:
            log.error("任务执行失败或被中断")
