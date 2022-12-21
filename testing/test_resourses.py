from game.resources import get_resource_path
import os


def test_get_resource_path():
    assert get_resource_path('images/test_file.png') == \
        os.environ['PROJECT_DIR'] + '/resources/images/test_file.png'
