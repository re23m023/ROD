#!/usr/bin/env python3
import rospy
import moveit_commander
import json
import sys
import os
import time

def load_waypoints(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        rospy.logerr(f"Fehler beim Laden der Waypoints: {e}")
        return []

def move_to_position(group, joints, desc, pause):
    rospy.loginfo(f"➡️ {desc}")
    group.set_joint_value_target(joints)
    success = group.go(wait=True)
    group.stop()
    if success:
        rospy.loginfo("✅ Ziel erreicht.")
    else:
        rospy.logerr("❌ Bewegung fehlgeschlagen.")
    time.sleep(pause)

def main():
    rospy.init_node("knick_waypoint_mover", anonymous=True)
    moveit_commander.roscpp_initialize(sys.argv)

    group_name = "knick_arm"
    move_group = moveit_commander.MoveGroupCommander(group_name)

    wp_path = os.path.join(os.path.dirname(__file__), "../waypoints/knick_wp.json")
    waypoints = load_waypoints(wp_path)

    for wp in waypoints:
        pos = wp["joints"]
        desc = wp.get("description", "Unnamed Step")
        pause = wp.get("pause", 1)
        move_to_position(move_group, pos, desc, pause)

    moveit_commander.roscpp_shutdown()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
