#!/bin/bash

# Workspace setzen
cd ~/catkin_ws

# Terminal 1: Gazebo mit Controllern
gnome-terminal --title="Gazebo + Controller" -- bash -c "source devel/setup.bash; roslaunch station_neu gazebocontroller.launch; exec bash"

# Kurzes Warten, damit Gazebo starten kann
sleep 5

# Terminal 2: MoveIt + RViz
gnome-terminal --title="MoveIt + RViz" -- bash -c "source devel/setup.bash; roslaunch station_moveit_config demo.launch; exec bash"

# Warten, bis der MoveIt-Service wirklich verfügbar ist
echo "⏳ Warte auf /move_group Service..."
until rosservice list | grep -q /move_group; do
  sleep 1
done
echo "✅ /move_group ist verfügbar."

# Terminal 3: Python-Testskript ausführen
#gnome-terminal --title="Test Knick-Motion" -- bash -c "source devel/setup.bash; rosrun #station_neu test_knick_motion.py; exec bash"

