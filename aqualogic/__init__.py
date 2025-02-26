"""Support for AquaLogic devices."""
from datetime import timedelta
import logging
import threading
import time

#from aqualogic.core import AquaLogic
from .core import AquaLogic
import voluptuous as vol

from homeassistant.const import (
    CONF_DEVICE,
    CONF_HOST,
    CONF_PATH,
    CONF_PORT,
    EVENT_HOMEASSISTANT_START,
    EVENT_HOMEASSISTANT_STOP,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
#from homeassistant.helpers.dispatcher import dispatcher_send
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "aqualogic"
UPDATE_TOPIC = f"{DOMAIN}_update"
CONF_UNIT = "unit"
RECONNECT_INTERVAL = timedelta(seconds=10)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_DEVICE, default="socket"): cv.string,
                vol.Optional(CONF_HOST, default="localhost"): cv.string,
                vol.Optional(CONF_PORT, default=23): cv.port,
                vol.Optional(CONF_PATH, default="/dev/ttyUSB0"): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up AquaLogic platform."""
    device = config[DOMAIN][CONF_DEVICE]
    host = config[DOMAIN][CONF_HOST]
    port = config[DOMAIN][CONF_PORT]
    path = config[DOMAIN][CONF_PATH]
    processor = AquaLogicProcessor(hass, device, host, port, path)
    hass.data[DOMAIN] = processor
    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, processor.start_listen)
    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, processor.shutdown)
    _LOGGER.debug("AquaLogicProcessor initialized")
    return True


class AquaLogicProcessor(threading.Thread):
    """AquaLogic event processor thread."""

    def __init__(self, hass, device, host, port, path):
        """Initialize the data object."""
        super().__init__(daemon=True)
        self._hass = hass
        self._device = device
        self._host = host
        self._port = port
        self._path = path
        self._shutdown = False
        self._panel = None

    def start_listen(self, event):
        """Start event-processing thread."""
        _LOGGER.debug("Event processing thread started")
        self.start()

    def shutdown(self, event):
        """Signal shutdown of processing event."""
        _LOGGER.debug("Event processing signaled exit")
        self._shutdown = True

    def data_changed(self, panel):
        """Aqualogic data changed callback."""
        self._hass.helpers.dispatcher.dispatcher_send(UPDATE_TOPIC)

    def run(self):
        """Event thread."""

        while True:
            self._panel = AquaLogic()
            try:
                if self._device == "socket":
                    _LOGGER.info("Connecting to %s:%d", self._host, self._port)
                    self._panel.connect_socket(self._host, self._port)
                else:
                    _LOGGER.info("Connecting to %s", self._path)
                    self._panel.connect_serial(self._path)

                self._panel.process(self.data_changed)

                if self._shutdown:
                    return

                if self._device == "socket":
                    _LOGGER.error("Connection to %s:%d lost", self._host, self._port)
                else:
                    _LOGGER.error("Connection to %s lost", self._path)

            except Exception as e:
                _LOGGER.error("Connection exception %s", e)

            time.sleep(RECONNECT_INTERVAL.seconds)

    @property
    def panel(self):
        """Retrieve the AquaLogic object."""
        return self._panel
