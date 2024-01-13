from yoomoney import Quickpay
from loader import yoomoney_token


def create_pay_link(id_: int, coast: int) -> str:
    quickpay = Quickpay(
        receiver=yoomoney_token,
        quickpay_form="shop",
        targets=f"Оплата услуг печати или сканирования заказа {id_}",
        paymentType="SB",
        sum=coast,
        label=str(id_),
    )
    return quickpay.base_url
