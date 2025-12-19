from internal.config import configer
from internal.config.product import ProductTypeData
from internal.core.service.product import ProductService
from internal.error import ProductStatusCode
from internal.util import CliUtils, PriceUtils, TimeUtils, log


class CliProduct:
    """
    票务选购
    """

    @staticmethod
    def choose_event_step() -> bool:
        """
        选择票务信息
        """
        event_id = CliUtils.inquire(
            type="Text",
            message="请输入活动 ID",
            default="",
        )

        try:
            resp = ProductService.get_ticket(int(event_id))
            status_code, ticket_main, ticket_types = resp

            if status_code != ProductStatusCode.Success:
                log.error("获取票务信息失败")
                return False

            if not ticket_types:
                log.warning("该活动没有可用票务")
                return False

            CliUtils.print("", end="\n")
            CliUtils.print("可用票务列表", color="cyan", size="large")
            CliUtils.print("", end="\n")

            choices = []
            ticket_map = {}

            for ticket in ticket_types:
                display_text = (
                    f"{ticket.ticketName} | "
                    f"{PriceUtils.format_price(ticket.ticketPrice)} | "
                    f"开票: {TimeUtils.format_timestamp(ticket.sellStartTime)}"
                )
                choices.append(display_text)
                ticket_map[display_text] = ticket

            choices.append("返回")
            ticket_map["返回"] = None

            selected = CliUtils.inquire(
                type="List",
                message="请选择票务",
                choices=choices,
            )

            if selected == "返回" or selected not in ticket_map:
                return False

            selected_ticket = ticket_map[selected]

            CliUtils.print("", end="\n")
            CliUtils.print("已选择票务", color="green", size="large")
            CliUtils.print(f"票务 ID: {selected_ticket.id}")
            CliUtils.print(f"票务名称: {selected_ticket.ticketName}")
            if selected_ticket.square:
                CliUtils.print(f"场次名称: {selected_ticket.square}")
            CliUtils.print(
                f"票务价格: {PriceUtils.format_price(selected_ticket.ticketPrice)}"
            )
            CliUtils.print(f"可购买数量: {selected_ticket.purchaseNum}张")
            CliUtils.print(f"剩余数量: {selected_ticket.remainderNum}张")
            CliUtils.print(f"已锁定数量: {selected_ticket.lockNum}张")
            CliUtils.print(
                f"实名制购票: {'是' if selected_ticket.realnameAuth else '否'}"
            )
            CliUtils.print(
                f"开票时间: {TimeUtils.format_timestamp(selected_ticket.sellStartTime)}"
            )
            CliUtils.print(
                f"结束时间: {TimeUtils.format_timestamp(selected_ticket.sellEndTime)}"
            )
            CliUtils.print("", end="\n")

            configer.product.ticketType = ProductTypeData(
                id=selected_ticket.id,
                name=selected_ticket.ticketName,
                square=selected_ticket.square,
                ticketPrice=selected_ticket.ticketPrice,
                purchaseNum=selected_ticket.purchaseNum,
                remainderNum=selected_ticket.remainderNum,
                lockNum=selected_ticket.lockNum,
                realnameAuth=selected_ticket.realnameAuth,
                sellStartTime=selected_ticket.sellStartTime,
                sellEndTime=selected_ticket.sellEndTime,
            )
            configer.product.ticketMain.id = ticket_main.eventMainId
            configer.product.ticketMain.name = ticket_main.eventName

            return True
        except ValueError:
            log.error("活动 ID 格式错误，请输入数字")
            return False
        except Exception as e:
            log.error(f"获取活动信息失败: {e}")
            return False

    @staticmethod
    def choose_pay_step():
        """
        选择支付方式
        """
        CliUtils.print("", end="\n")
        CliUtils.print("选择支付方式", color="cyan", size="large")
        CliUtils.print("", end="\n")

        payment_choices = ["微信支付", "支付宝"]
        payment_map = {
            "微信支付": "wx",
            "支付宝": "ali",
        }

        selected_payment = CliUtils.inquire(
            type="List",
            message="请选择支付方式",
            choices=payment_choices,
        )

        if selected_payment in payment_map:
            configer.product.ticketMethod = payment_map[selected_payment]
            CliUtils.print("", end="\n")
            CliUtils.print(
                f"已选择支付方式: {selected_payment}",
                color="green",
            )
            CliUtils.print("", end="\n")
        else:
            log.warning("未选择支付方式，使用默认值: 微信支付")
            configer.product.ticketMethod = "wx"

    @staticmethod
    def generate():
        """
        配置窗口
        """
        if not CliProduct.choose_event_step():
            return CliProduct.choose_event_step()

        CliProduct.choose_pay_step()
