from game.pose import Pose


# TODO: invert dependencies between camera and drawables. It should be camera.draw(drawable), not drawable.draw(camera)
# TODO: switch to smooth_step instead of exponential smoothing
class Camera:
    def __init__(self, starting_pose: Pose):
        """ Creates a new camera.
        Width and height of the pose control the size of the camera's view.

        :param starting_pose: Starting pose for the camera
        """
        self.pose = Pose().set_to(starting_pose)
        self.target_pose = self.pose
        self.k_value = 0

    def set_tracking(self, target: Pose, k_value: float = 3):
        """ Sets the camera to track a target pose

        :param target: the pose to track
        :param k_value: the amount of time it takes to reach the target pose
        """
        self.target_pose = target
        self.k_value = k_value

    def update(self, dt: float) -> None:
        """ Updates the camera's position. To be called every frame

        :param dt: Time elapsed since last update
        """
        self.pose.set_to(self.pose - (self.pose - self.target_pose) * self.k_value * dt)


if __name__ == '__main__':
    camera = Camera(Pose(1, 1, 0, 10, 10))
    target_pose = Pose(10, 10, 0, 10, 10)
    print(camera.pose)
    print(target_pose)
    camera.set_tracking(target_pose, k_value=1)
    for t in range(100):
        print(f'{t * 0.1:.1f}', camera.pose, target_pose, target_pose - camera.pose)
        camera.update(0.1)
