from pywps import Process, LiteralInput, ComplexOutput
from pywps import FORMATS
from pywps.app.exceptions import ProcessError
from pywps.inout.outputs import MetaLink4, MetaFile


class Average(Process):
    def __init__(self):
        inputs = [
            LiteralInput('collection', 'Collection',
                         data_type='string',
                         default='c3s-cmip5.output1.ICHEC.EC-EARTH.historical.day.atmos.day.r1i1p1.tas.latest',
                         min_occurs=1,
                         max_occurs=1,),
            LiteralInput('axes', 'Axes',
                         abstract='Please choose an axes for averaging.',
                         data_type='string',
                         min_occurs=1,
                         max_occurs=1,
                         default='time',
                         allowed_values=['time', 'latitude', 'longitude']),
            LiteralInput('pre_checked', 'Pre-Checked', data_type='boolean',
                         abstract='Use checked data only.',
                         default='0',
                         min_occurs=1,
                         max_occurs=1),
        ]
        outputs = [
            ComplexOutput('output', 'METALINK v4 output',
                          abstract='Metalink v4 document with references to NetCDF files.',
                          as_reference=True,
                          supported_formats=[FORMATS.META4]),
        ]

        super(Average, self).__init__(
            self._handler,
            identifier='average',
            title='Average',
            abstract='Run averaging on climate data.',
            version='1.0',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        # TODO: handle lazy load of daops
        from daops.utils import is_characterised
        collection = [dset.data for dset in request.inputs['collection']]
        if request.inputs['pre_checked'][0].data and not is_characterised(collection, require_all=True):
            raise ProcessError('Data has not been pre-checked')
        # metalink document with collection of netcdf files
        ml4 = MetaLink4('average-result', 'Averaging result as NetCDF files.', workdir=self.workdir)
        mf = MetaFile('Text file', 'Dummy text file', fmt=FORMATS.TEXT)
        mf.data = 'not working yet'
        ml4.append(mf)
        response.outputs['output'].data = ml4.xml
        return response
