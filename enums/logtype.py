from enum import Enum


class LogType(Enum):
    VISIT = "visit"
    REDIRECT = "redirect"
    CLICK = "click"
    CAMPAIGN_CLICK = "campaign_click"
    MENU_CLICK = "menu_click"
    ATTEND = "attend"
    SEARCH = "search"
    BARO_ATTEND = "baro_attend"
