from main.workflows.factory import WorkflowFactory
from main.workflows.base import Workflow

def _test_build(cls : Workflow):
    wf : Workflow = cls()
    wf.build_steps()

def test_build_non_configurable_workflows():
    for name, meta in WorkflowFactory.WORKFLOWS.items():
        if meta.needs_config:
            continue
        print(f"testing workflow {name}")
        _test_build(meta.cls)