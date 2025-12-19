from internal.config import configer
from internal.config.buyer import BuyerData
from internal.core.service.buyer import BuyerService
from internal.error import BuyerStatusCode
from internal.util import CliUtils, PrivacyUtils, log


class CliBuyer:
    """
    票务选购
    """

    @staticmethod
    def choose_buyer_step() -> bool:
        """
        选择购票人
        """
        CliUtils.print("", end="\n")
        CliUtils.print("选择购票人", color="cyan", size="large")
        CliUtils.print("", end="\n")

        try:
            status_code, buyer_list = BuyerService.get_buyer()

            if status_code != BuyerStatusCode.Success:
                log.error("获取购票人信息失败")
                return False

            if not buyer_list:
                log.warning("没有可用的购票人信息，请先添加购票人")
                return False

            choices = []
            buyer_map = {}

            for buyer in buyer_list:
                masked_mobile = PrivacyUtils.mask_phone(buyer.mobile)
                masked_idcard = PrivacyUtils.mask_idcard(buyer.idcard)
                display_text = f"{buyer.realname} | {masked_mobile} | {masked_idcard}"
                choices.append(display_text)
                buyer_map[display_text] = buyer

            selected_buyers = CliUtils.inquire(
                type="Checkbox",
                message="请选择购票人（可多选，空格选择/取消，回车确认）",
                choices=choices,
            )

            if not selected_buyers:
                log.warning("未选择任何购票人")
                return False

            selected_buyer_data = []
            for selected_text in selected_buyers:
                if selected_text in buyer_map:
                    buyer = buyer_map[selected_text]
                    buyer_data = BuyerData(
                        id=buyer.id,
                        realname=buyer.realname,
                        idcard=buyer.idcard,
                        mobile=buyer.mobile,
                        validType=buyer.validType,
                    )
                    selected_buyer_data.append(buyer_data)

            configer.buyer.buyer = selected_buyer_data
            configer.buyer.count = len(selected_buyer_data)

            CliUtils.print("", end="\n")
            CliUtils.print(
                f"已选择 {len(selected_buyer_data)} 位购票人",
                color="green",
            )
            for buyer_data in selected_buyer_data:
                masked_mobile = PrivacyUtils.mask_phone(buyer_data.mobile)
                CliUtils.print(
                    f"  - {buyer_data.realname} ({masked_mobile})",
                    color="green",
                )
            CliUtils.print("", end="\n")

            return True

        except Exception as e:
            log.error(f"选择购票人失败: {e}", exc_info=True)
            return False

    @staticmethod
    def generate():
        """
        配置窗口
        """
        if not CliBuyer.choose_buyer_step():
            return CliBuyer.choose_buyer_step()
