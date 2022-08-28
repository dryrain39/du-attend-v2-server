from dataclasses import dataclass, asdict

from fluent_logger.flogger import FLogger


@dataclass()
class PromoLogger(FLogger):
    tag = "promo_2205"

    action_code: int
    client_ip: str
    std_id: str
    success: bool
    additional_data: dict


class ActionCode:
    GET_COUPON: int = 100

    PROMOTION_STATUS: int = 200

    PROMOTION_GET_URL: int = 300

    PROMOTION_ACTION: int = 400

