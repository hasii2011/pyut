
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from copy import copy

from org.pyut.ui.IPyutProject import IPyutProject
from org.pyut.uiv2.ProjectTree import ProjectTree

PyutProjects = NewType('PyutProjects', List[IPyutProject])


class ProjectManager:
    """
    This project manages interactions to the UI project tree
    """

    def __init__(self, projectTree: ProjectTree):

        self.logger:  Logger = getLogger(__name__)

        self._projects:       PyutProjects = PyutProjects([])
        self._currentProject: IPyutProject = cast(IPyutProject, None)

    @property
    def projects(self) -> PyutProjects:
        """
        The list of currently managed projects

        Returns:  Only a copy of the projects
        """
        return copy(self._projects)

    @property
    def currentProject(self) -> IPyutProject:
        """
        Returns:  The currently managed project
        """
        return self._currentProject

    @currentProject.setter
    def currentProject(self, newProject: IPyutProject):
        """
        Set the currently managed project

        Args:
            newProject:   Must have been previously managed
        """
        assert newProject in self._projects
        self._currentProject = newProject

    def addProject(self, project: IPyutProject):
        """
        Add a new project to manage
        Args:
            project:   Should not already be managed
        """
        assert project not in self._projects
        self._projects.append(project)

    def removeProject(self, project: IPyutProject):
        """
        Remove a project from our purview

        Args:
            project:   The project to no longer manage; should have been
            previously managed
        """
        assert project in self._projects
        self._projects.remove(project)
