from datetime import datetime
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class WebsitePageview:
    website_pageview_id: str
    created_at: datetime
    website_session_id: int
    pageview_url: str


@dataclass(unsafe_hash=True)
class WebsiteSession:
    website_session_id: str
    created_at: datetime
    user_id: int
    is_repeat_session: bool
    utm_source: str
    utm_campaign: str
    utm_content: str
    device_type: str
    http_referer: str
