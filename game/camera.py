from typing import Callable

from game.drawable import Drawable
from game.math import get_smooth_step_func
from game.pose import Pose
from game.callbackHandler import CallbackHandler


# TODO: invert dependencies between camera and drawables. It should be camera.draw(drawable), not drawable.draw(camera)
class Camera:
    def __init__(self, starting_pose: Pose):
        """ Creates a new camera.
        Width and height of the pose control the size of the camera's view.

        :param starting_pose: Starting pose for the camera
        """
        self.pose = Pose().set_to(starting_pose)
        print(self.pose)
        self.target_pose = self.pose
        self.position_function: Callable[[float], Pose] = lambda t: self.target_pose
        self.position_tracking_time = 0

        self.callback_handler = CallbackHandler()

    def set_tracking(self, target: Pose, time_constant: float = 5):
        """ Sets the camera to track a target pose

        :param target: the pose to track
        :param time_constant: the amount of time it takes to reach the target pose
        """
        self.target_pose = target
        # Poses implement arithmatic rules, so they can be used in place of a float for the smooth step function
        self.position_function = get_smooth_step_func(self.pose, self.target_pose, time_constant)
        self.callback_handler.clear_callbacks()
        self.callback_handler.add_callback(self.target_pose.any_updated, self.update_tracking)
        self.update_tracking()

    def update_tracking(self):
        self.position_tracking_time = 0

    def update(self, dt: float) -> None:
        """ Updates the camera's position. To be called every frame

        :param dt: Time elapsed since last update
        """
        self.callback_handler.check_callbacks()
        self.position_tracking_time += dt
        self.pose.set_to(self.position_function(self.position_tracking_time))


if __name__ == '__main__':
    camera = Camera(Pose(1, 1, 0, 10, 10))
    print(camera.pose)
    print(Pose(10, 10))
    camera.set_tracking(Pose(10, 10), 1)
    for _ in range(12):
        camera.update(0.1)
        print(camera.pose)
