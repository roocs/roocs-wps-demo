from pywps import Process, LiteralInput, ComplexOutput
from pywps import FORMATS
from pywps.app.exceptions import ProcessError

import daops


class Average(Process):
    def __init__(self):
        inputs = [
            LiteralInput('data_ref', 'Data references',
                         data_type='string',
                         default='cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas',
                         min_occurs=1,
                         max_occurs=10,),
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
            ComplexOutput('output', 'Output',
                          as_reference=True,
                          supported_formats=[FORMATS.TEXT]),
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

    @staticmethod
    def _handler(request, response):
        data_refs = [dref.data for dref in request.inputs['data_ref']]
        if request.inputs['pre_checked'][0].data and not daops.is_characterised(data_refs, require_all=True):
            raise ProcessError('Data has not been pre-checked')
        response.outputs['output'].data = 'not working yet'
        return response
