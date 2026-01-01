from internal.config import configer
from internal.core.service import ProductService
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
        event_main_id = CliUtils.inquire(
            type="Text",
            message="请输入活动 ID",
            default="5476",
        )

        try:
            resp = ProductService.get_ticket(int(event_main_id))
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
            type_map = {}

            for ticket in ticket_types:
                display_text = (
                    f"{ticket.name} | "
                    f"{PriceUtils.format_price(ticket.price)} | "
                    f"开票: {TimeUtils.format_timestamp(ticket.sellStartTime)}"
                )
                choices.append(display_text)
                type_map[display_text] = ticket

            choices.append("返回")
            type_map["返回"] = None

            selected = CliUtils.inquire(
                type="List",
                message="请选择票务",
                choices=choices,
            )

            if selected == "返回":
                return False

            if selected not in type_map:
                log.error("选择的票务不存在")
                return False

            selected_type = type_map[selected]

            CliUtils.print("", end="\n")
            CliUtils.print("已选择票务", color="green", size="large")
            CliUtils.print(f"票务 ID: {selected_type.id}")
            CliUtils.print(f"票务名称: {selected_type.name}")
            if selected_type.square:
                CliUtils.print(f"场次名称: {selected_type.square}")
            CliUtils.print(f"票务价格: {PriceUtils.format_price(selected_type.price)}")
            CliUtils.print(f"可购买数量: {selected_type.purchaseNum}张")
            CliUtils.print(f"剩余数量: {selected_type.remainderNum}张")
            CliUtils.print(f"已锁定数量: {selected_type.lockNum}张")
            CliUtils.print(
                f"实名制购票: {'是' if selected_type.realnameAuth else '否'}"
            )
            CliUtils.print(
                f"开票时间: {TimeUtils.format_timestamp(selected_type.sellStartTime)}"
            )
            CliUtils.print(
                f"结束时间: {TimeUtils.format_timestamp(selected_type.sellEndTime)}"
            )
            CliUtils.print("", end="\n")

            configer.product.ticketMain = ticket_main
            configer.product.ticketType = selected_type

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

        payment_choices = ["支付宝", "微信支付"]
        payment_map = {
            "支付宝": "ali",
            "微信支付": "wx",
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
            return

        CliProduct.choose_pay_step()
