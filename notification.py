import requests
import json

from homeassistant.components.notify import (
    ATTR_TITLE,
    ATTR_MESSAGE,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required("url"): cv.string,
        vol.Required("gateway"): cv.string,
    }
)


def get_service(hass, config, discovery_info=None):
    return CustomApiNotificationService(hass, config)


class CustomApiNotificationService(BaseNotificationService):
    def __init__(self, hass, config):
        self.hass = hass
        self.url = config.get("url")
        self.gateway = config.get("gateway")

    def send_message(self, message="", **kwargs):
        data = {
            "text": message,
            "username": kwargs.get("username"),
            "gateway": self.gateway,
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.url, json=data, headers=headers)
        if response.status_code != 200:
            _LOGGER.error("Error sending notification: %s", response.text)