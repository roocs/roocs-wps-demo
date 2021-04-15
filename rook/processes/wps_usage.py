import logging
import os
import glob
import subprocess

from pywps import FORMATS, ComplexOutput, Format, LiteralInput, Process
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError


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
                "output",
                "GeoUsage",
                abstract="Output of GeoUsage as text.",
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
        response.update_status("GeoUsage started.", 0)
        cmd = ["GeoUsage", "log", "analyze"]
        cmd.extend(sorted(glob.glob("/var/log/nginx/access.log*")))
        cmd.extend(
            [
                "--service-type",
                "OGC:WPS",
                "--endpoint",
                "/wps",
                "--resolve-ips",
                "--top",
                "200",
            ]
        )
        if "time" in request.inputs:
            cmd.extend(["--time", request.inputs["time"][0].data])
        result = subprocess.run(cmd, capture_output=True, shell=False)
        if result.returncode != 0:
            raise ProcessError(
                f"GeoUsage failed: {result.stderr.decode('utf-8', errors='ignore')}"
            )
        with open(os.path.join(self.workdir, "geousage.txt"), "w") as fout:
            fout.write(result.stdout.decode("utf-8", errors="ignore"))
            response.outputs["output"].file = fout.name
        response.update_status("GeoUsage completed.", 100)
        return response
