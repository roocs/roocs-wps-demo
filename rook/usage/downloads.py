import gzip
import os
import re
import glob
import pandas as pd

from .base import Usage

LOG_PATTERN = re.compile(
    r"""(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - (?P<remoteuser>.+) \[(?P<datetime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(?P<method>.+) )(?P<request>.+)(http\/[1-2]\.[0-9]")) (?P<status>\d{3}) (?P<size>\d+) (["](?P<referer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""",  # noqa
    re.IGNORECASE,
)


class Downloads(Usage):
    def collect(self, time=None, outdir=None):
        log_files = sorted(glob.glob("/var/log/nginx/access.log*"))
        data = []
        for f in log_files:
            if f.endswith(".gz"):
                logfile = gzip.open(f)
            else:
                logfile = open(f, "rb")
            for line in logfile.readlines():
                result = re.search(LOG_PATTERN, line.decode())
                if not result:
                    continue
                result_dict = result.groupdict()
                request = result_dict["request"].strip()
                if not request.startswith("/outputs"):
                    continue
                data.append(
                    dict(
                        ip=result_dict["ip"].strip(),
                        datetime=result_dict["datetime"],
                        request=request,
                        size=int(result_dict["size"]),
                        referer=result_dict["referer"].strip(),
                        useragent=result_dict["useragent"].strip(),
                        status=int(result_dict["status"]),
                        method=result.group(6).strip(),
                    )
                )
            logfile.close()
        df = pd.DataFrame(data)
        df_downloads = df.loc[
            df["request"].str.contains(r"/outputs/rook/.*/.*\.nc", regex=True)
        ]  # noqa
        fname = os.path.join(outdir, "downloads.csv")
        df_downloads.to_csv(fname, index=False)
        return fname
