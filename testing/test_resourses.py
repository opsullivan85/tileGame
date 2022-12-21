from game.resources import get_resource_path
import os


def test_get_resource_path():
    """ PROJECT_DIR needs to be set to the root directory of the project for this test to work.
    This can be done in the run configuration of the test runner.
    """
    assert get_resource_path('textures/test_file.file') == \
        os.environ['PROJECT_DIR'] + '/resources/textures/test_file.file'
