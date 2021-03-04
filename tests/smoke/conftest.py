import pytest

from owslib.wps import WebProcessingService, monitorExecution
from pywps import configuration as config

from tests.smoke.utils import parse_metalink
from tests.common import PYWPS_CFG


def server_url():
    config.load_configuration(cfgfiles=PYWPS_CFG)
    url = config.get_config_value("server", "url")
    return url


class RookWPS:
    def __init__(self, url):
        self.wps = WebProcessingService(url, verbose=False, skip_caps=True)

    def getcapabilities(self):
        self.wps.getcapabilities()
        return self.wps

    def describeprocess(self, identifier):
        return self.wps.describeprocess(identifier)

    def execute(self, identifier, inputs):
        outputs = [("output", False, None)]
        execution = self.wps.execute(identifier, inputs, output=outputs)
        monitorExecution(execution)
        assert execution.isSucceded() is True
        xml = execution.processOutputs[0].data[0]
        url = parse_metalink(xml)
        return url


@pytest.fixture
def wps():
    wps_ = RookWPS(server_url())
    return wps_
