from app.core.project_context import ProjectContext


class ProjectRuntime:
    """
    Runtime environment for an opened project.
    """

    def __init__(self, project):

        self.context = ProjectContext(project)

        self.modules = {}

    def register_module(self, module):

        self.modules[module.id] = module

    def get_module(self, module_id):

        return self.modules.get(module_id)

    def get_context(self):

        return self.context