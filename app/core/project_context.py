class ProjectContext:
    """
    Shared project context passed to every module.
    """

    def __init__(self, project):

        self.project = project

    @property
    def name(self):
        return self.project["name"]

    @property
    def engine(self):
        return self.project["engine"]

    @property
    def path(self):
        return self.project["path"]

    @property
    def data(self):
        return self.project