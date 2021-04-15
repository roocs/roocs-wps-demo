import os
import glob
import subprocess

from .base import Usage


class GeoUsage(Usage):
    def collect(self, time=None, outdir=None):
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
        if time:
            cmd.extend(["--time", time])
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            raise Exception(
                f"GeoUsage failed: {result.stderr.decode('utf-8', errors='ignore')}"
            )
        with open(os.path.join(outdir, "geousage.txt"), "w") as fout:
            fout.write(result.stdout.decode("utf-8", errors="ignore"))
        return fout.name
