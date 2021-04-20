import os
import pandas as pd

from pywps import configuration as config

from .base import Usage


class WPSUsage(Usage):
    def collect(self, time=None, outdir=None):
        db_conn = config.get_config_value("logging", "database")
        df = pd.read_sql(sql="pywps_requests", con=db_conn)
        df = df.loc[df["operation"] == "execute"]
        fname = os.path.join(outdir, "wps_requests.csv")
        df.to_csv(fname, index=False)
        return fname
