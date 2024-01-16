
from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW


class ProjectTestBase(UnitTestBaseW):

    RESOURCES_TEST_CLASSES_PACKAGE_NAME:      str = 'tests.resources.testclass'
    RESOURCES_TEST_JAVA_CLASSES_PACKAGE_NAME: str = 'tests.resources.testclass.ozzee'
    RESOURCES_TEST_DATA_PACKAGE_NAME:         str = 'tests.resources.testdata'
    RESOURCES_TEST_IMAGES_PACKAGE_NAME:       str = 'tests.resources.testimages'

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
