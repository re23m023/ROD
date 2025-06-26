#!/usr/bin/env python3

import rospy
import moveit_commander
import sys

def main():
    # ROS-Node initialisieren
    rospy.init_node('test_knick_motion', anonymous=True)
    moveit_commander.roscpp_initialize(sys.argv)

    # MoveGroupCommander für Knick-Arm
    move_group = moveit_commander.MoveGroupCommander("knick_arm")

    rospy.loginfo("✅ MoveGroupCommander für 'knick_arm' erstellt.")

    # OPTIONAL: Infos zum aktuellen Zustand
    current_joints = move_group.get_current_joint_values()
    rospy.loginfo(f"🔧 Aktuelle Gelenkpositionen:\n{current_joints}")

    # ZIEL-Gelenkwinkel (bitte anpassen falls nötig – 6 oder 7 Gelenke)
    joint_goal = [-1.5, -0.7, -1.2, -1.0, 0.6, -0.4, 0.0]  # Beispielwerte für 7 DOF

    if len(joint_goal) != len(current_joints):
        rospy.logerr("❌ Anzahl der Ziel-Gelenke stimmt nicht mit dem Modell überein.")
        return

    move_group.set_joint_value_target(joint_goal)

    # Bewegung ausführen
    success = move_group.go(wait=True)
    move_group.stop()

    if success:
        rospy.loginfo("✅ Bewegung erfolgreich abgeschlossen.")
    else:
        rospy.logerr("❌ Bewegung fehlgeschlagen.")

    moveit_commander.roscpp_shutdown()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass

