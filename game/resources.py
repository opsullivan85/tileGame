from pathlib import Path
import game


def get_resource_path(relative_path: str) -> str:
    """ Gets the absolute path of a resource file

    :param relative_path: Relative path to the resource
    :return: Absolute path to the resource
    """
    # Resources are in the same directory as the game package in the resources folder
    return Path(game.__file__).parent.parent.joinpath('resources').joinpath(relative_path).as_posix()
