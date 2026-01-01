from internal.config import configer
from internal.core.service import ProductService
from internal.core.task import OrderTask
from internal.error import ProductStatusCode
from internal.util import CliUtils, log


class CliLaunch:
    """
    票务选购
    """

    @staticmethod
    def validate_config() -> bool:
        """
        检查配置
        """
        if not configer.buyer.buyer:
            log.error("请先配置购买人信息")
            return False

        if not configer.product.ticketMain.id or not configer.product.ticketType.id:
            log.error("请先配置票务信息")
            return False

        status_code = ProductService.check_inactive()
        if status_code != ProductStatusCode.Success:
            log.error("票务已下架，请重新选择")
            return False

    @staticmethod
    def update_product() -> bool:
        """
        更新票务信息
        """
        resp = ProductService.get_ticket(configer.product.ticketMain.id)
        status_code, _ticket_main, ticket_types = resp

        if status_code != ProductStatusCode.Success:
            log.error("获取票务信息失败")
            return False

        if not ticket_types:
            log.warning("该活动没有可用票务")
            return False

        for ticket in ticket_types:
            if ticket.id == configer.product.ticketType.id:
                configer.product.ticketType.sellStartTime = ticket.sellStartTime
                configer.product.ticketType.sellEndTime = ticket.sellEndTime
                configer.product.ticketType.realnameAuth = ticket.realnameAuth

        return True

    @staticmethod
    def generate():
        """
        配置窗口
        """
        result = CliLaunch.validate_config()
        if not result:
            return

        result = CliLaunch.update_product()
        if not result:
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
        task = OrderTask()
        success = task.run()

        if success:
            log.info("任务执行成功")
        else:
            log.error("任务执行失败或被中断")
