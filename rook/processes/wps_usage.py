import logging

from pywps import FORMATS, ComplexOutput, Format, LiteralInput, Process
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError

from rook.usage import GeoUsage, DBUsage


LOGGER = logging.getLogger()


class Usage(Process):
    def __init__(self):
        inputs = [
            LiteralInput(
                "time",
                "Time Period",
                abstract="The time period for usage collection seperated by /"
                "Example: 2021-04-01/2021-04-30",
                data_type="string",
                min_occurs=0,
                max_occurs=1,
            ),
        ]
        outputs = [
            ComplexOutput(
                "geousage",
                "GeoUsage",
                abstract="OGC:WPS metrics collected from apache/nginx log files.",
                metadata=[
                    Metadata("GeoUsage", "https://github.com/geopython/GeoUsage"),
                ],
                as_reference=True,
                supported_formats=[FORMATS.TEXT],
            ),
            ComplexOutput(
                "dbusage",
                "DBUsage",
                abstract="OGC:WPS metrics collected from pywps database.",
                as_reference=True,
                supported_formats=[FORMATS.TEXT],
            ),
        ]

        super(Usage, self).__init__(
            self._handler,
            identifier="usage",
            title="Usage",
            abstract="Run usage collector.",
            metadata=[
                Metadata("ROOK", "https://github.com/roocs/rook"),
            ],
            version="0.1",
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True,
        )

    def _handler(self, request, response):
        response.update_status("Usage started.", 0)
        if "time" in request.inputs:
            time = request.inputs["time"][0].data
        else:
            time = None
        try:
            usage = GeoUsage()
            response.outputs["geousage"].file = usage.collect(
                time=time, outdir=self.workdir
            )
            response.update_status("GeoUsage completed.", 50)
            usage = DBUsage()
            response.outputs["dbusage"].file = usage.collect(
                time=time, outdir=self.workdir
            )
            response.update_status("DBUsage completed.", 100)
        except Exception as e:
            raise ProcessError(f"{e}")
        return response
