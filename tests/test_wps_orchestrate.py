from pywps import Service
from pywps.tests import assert_response_success, client_for

from rook.processes.wps_orchestrate import Orchestrate

from .common import PYWPS_CFG, get_output, resource_file


def test_wps_orchestrate():
    client = client_for(Service(processes=[Orchestrate()], cfgfiles=[PYWPS_CFG]))
    datainputs = "workflow=@xlink:href=file://{}".format(
        resource_file("wf_cmip6_subset_average.json")
    )
    resp = client.get(
        "?service=WPS&request=Execute&version=1.0.0&identifier=orchestrate&datainputs={}".format(
            datainputs
        )
    )
    assert_response_success(resp)
    assert "meta4" in get_output(resp.xml)["output"]


def test_wps_orchestrate_subset_collection_only():
    client = client_for(Service(processes=[Orchestrate()], cfgfiles=[PYWPS_CFG]))
    datainputs = "workflow=@xlink:href=file://{0}".format(
        resource_file("subset_wf_collection_only.json")
    )
    resp = client.get(
        "?service=WPS&request=Execute&version=1.0.0&identifier=orchestrate&datainputs={}".format(
            datainputs
        )
    )

    assert_response_success(resp)
    assert "meta4" in get_output(resp.xml)["output"]
