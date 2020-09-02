from pywps import Process, ComplexInput, ComplexOutput
from pywps import FORMATS

from rook import workflow


class Orchestrate(Process):
    def __init__(self):
        inputs = [
            ComplexInput('workflow', 'Workflow',
                         min_occurs=1,
                         max_occurs=1,
                         supported_formats=[FORMATS.JSON]),
        ]
        outputs = [
            ComplexOutput('output', 'Output',
                          as_reference=True,
                          supported_formats=[FORMATS.NETCDF]),
        ]

        super(Orchestrate, self).__init__(
            self._handler,
            identifier='orchestrate',
            title='Orchestrate',
            abstract='Run a workflow',
            version='1.0',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        wf = workflow.WorkflowRunner(
            output_dir=self.workdir)
        output = wf.run(request.inputs['workflow'][0].file)
        response.outputs['output'].file = output[0]
        return response
