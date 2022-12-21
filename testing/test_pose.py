from game.pose import Pose


def test_pose_equality():
    pose1 = Pose(1, 2, 3, 4, 5)
    pose2 = Pose(1, 2, 3, 4, 5)
    assert pose1 == pose2


def test_pose_inequality():
    pose1 = Pose(1, 1, 1, 1, 1)
    assert pose1 != Pose(1, 1, 1, 1, 0) and \
           pose1 != Pose(1, 1, 1, 0, 1) and \
           pose1 != Pose(1, 1, 0, 1, 1) and \
           pose1 != Pose(1, 0, 1, 1, 1) and \
           pose1 != Pose(0, 1, 1, 1, 1)


def test_pose_addition():
    """ Poses should not change size when added to each other
    """
    pose1 = Pose(1, 1, 1, 1, 1)
    pose2 = Pose(1, 1, 1, 1, 1)
    assert pose1 + pose2 == Pose(2, 2, 2, 1, 1)


def test_pose_subtraction():
    """ Poses should not change size when subtracted from each other
    """
    pose1 = Pose(1, 1, 1, 1, 1)
    pose2 = Pose(1, 1, 1, 1, 1)
    assert pose1 - pose2 == Pose(0, 0, 0, 1, 1)


def test_pose_multiplication():
    pose1 = Pose(2, 2, 2, 2, 2)
    pose2 = Pose(3, 3, 3, 3, 3)
    assert pose1 * pose2 == Pose(6, 6, 6, 6, 6)


def test_pose_division():
    pose1 = Pose(2, 2, 2, 2, 2)
    pose2 = Pose(3, 3, 3, 3, 3)
    assert pose1 / pose2 == Pose(2 / 3, 2 / 3, 2 / 3, 2 / 3, 2 / 3)


def test_pose_division_floor():
    pose1 = Pose(2, 2, 2, 2, 2)
    pose2 = Pose(3, 3, 3, 3, 3)
    assert pose1 // pose2 == Pose(0, 0, 0, 0, 0)


def test_default_pose_flags():
    pose = Pose(1, 1, 1, 1, 1)
    assert pose.x_updated and \
           pose.y_updated and \
           pose.theta_updated and \
           pose.w_updated and \
           pose.h_updated


def test_pose_reset_updates():
    pose = Pose(1, 1, 1, 1, 1)
    pose.reset_updates()
    assert not pose.x_updated and \
           not pose.y_updated and \
           not pose.theta_updated and \
           not pose.w_updated and \
           not pose.h_updated


def test_pose_update():
    pose1 = Pose(1, 1, 1, 1, 1)
    pose1.reset_updates()
    pose1.x += 1
    assert pose1.x_updated


def test_pose_set_to():
    pose1 = Pose(1, 1, 1, 1, 1)
    pose2 = Pose(2, 2, 2, 2, 2)
    pose1.set_to(pose2)
    assert pose1 == pose2


def test_pose_set_to_updates():
    pose1 = Pose(1, 1, 1, 1, 1)
    pose1.reset_updates()
    pose1.set_to(Pose(2, 1, 2, 1, 2))
    assert pose1.x_updated and \
           not pose1.y_updated and \
           pose1.theta_updated and \
           not pose1.w_updated and \
           pose1.h_updated
