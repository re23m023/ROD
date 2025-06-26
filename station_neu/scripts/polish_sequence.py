#!/usr/bin/env python3
import rospy
import sys
from moveit_commander import MoveGroupCommander, PlanningSceneInterface, RobotCommander, roscpp_initialize, roscpp_shutdown
from geometry_msgs.msg import PoseStamped
import time

def choose_mode():
    print("\n--- Politurmodus Auswahl ---")
    print("1: Einfache Politur (sanft, grobmaschig)")
    print("2: Intensive Politur (dicht, fein)")
    mode = input("Modusnummer eingeben: ")
    return mode

def move_to_pose(group, pose):
    group.set_pose_target(pose)
    plan = group.go(wait=True)
    group.stop()
    group.clear_pose_targets()
    return plan

def main():
    roscpp_initialize(sys.argv)
    rospy.init_node('polish_sequence')

    robot = RobotCommander()
    scene = PlanningSceneInterface()
    scara = MoveGroupCommander("scara_arm")
    knick = MoveGroupCommander("knick_arm")

    rospy.sleep(2)  # scene setup time

    # Pose: Greife Handy
    pick_pose = PoseStamped()
    pick_pose.header.frame_id = "world"
    pick_pose.pose.position.x = 0.4
    pick_pose.pose.position.y = 0.0
    pick_pose.pose.position.z = 0.3
    pick_pose.pose.orientation.w = 1.0

    # Pose: Lege auf Tisch
    place_pose = PoseStamped()
    place_pose.header.frame_id = "world"
    place_pose.pose.position.x = 0.0
    place_pose.pose.position.y = -0.4
    place_pose.pose.position.z = 0.3
    place_pose.pose.orientation.w = 1.0

    # Pose: Polierstart
    polish_start = PoseStamped()
    polish_start.header.frame_id = "world"
    polish_start.pose.position.x = 0.0
    polish_start.pose.position.y = -0.4
    polish_start.pose.position.z = 0.35
    polish_start.pose.orientation.w = 1.0

    mode = choose_mode()

    print("\n[SCARA] Hole Handy...")
    move_to_pose(scara, pick_pose)

    print("[SCARA] Lege Handy auf Tisch...")
    move_to_pose(scara, place_pose)

    print("[SCARA] Fahre in Home...")
    scara.set_named_target("scara_home")
    scara.go(wait=True)

    print("[Knick] Beginne Politur...")
    move_to_pose(knick, polish_start)

    if mode == "1":
        print("[Knick] Einfache Politur läuft...")
        for i in range(3):
            polish_start.pose.position.x += 0.02
            move_to_pose(knick, polish_start)
            polish_start.pose.position.x -= 0.02
            move_to_pose(knick, polish_start)
    elif mode == "2":
        print("[Knick] Intensive Politur läuft...")
        for i in range(6):
            polish_start.pose.position.x += 0.01
            move_to_pose(knick, polish_start)
            polish_start.pose.position.x -= 0.01
            move_to_pose(knick, polish_start)
    else:
        print("Ungültiger Modus. Abbruch.")
        return

    print("[Knick] Politur abgeschlossen. Fahre Home...")
    knick.set_named_target("knick_home")
    knick.go(wait=True)

    print("[SCARA] Hole Handy zurück...")
    move_to_pose(scara, place_pose)
    move_to_pose(scara, pick_pose)

    print("[SCARA] Lege Handy zurück...")
    move_to_pose(scara, pick_pose)
    scara.set_named_target("scara_home")
    scara.go(wait=True)

    print("\n✅ Ablauf abgeschlossen!")

    roscpp_shutdown()

if __name__ == '__main__':
    main()
