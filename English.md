# Puzzlebot: Autonomous Navigation & Traffic Light Detection
<div align="center">
  <img src="./assets/header.svg" alt="PuzzleBot — Autonomous Navigation & Traffic Light Detection" width="100%"/>
</div>

<br>

<div align="center">

![ROS2](https://img.shields.io/badge/ROS2-Humble-F4C2C2?style=for-the-badge&logo=ros&logoColor=7A3535)
![Python](https://img.shields.io/badge/Python-3.10+-C2D4F4?style=for-the-badge&logo=python&logoColor=1A3A6B)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-C2E8D4?style=for-the-badge&logo=opencv&logoColor=1A5C3A)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-F4DCC2?style=for-the-badge&logo=ubuntu&logoColor=7A4A1A)
![License](https://img.shields.io/badge/License-MIT-EAD4F4?style=for-the-badge&logo=opensourceinitiative&logoColor=4A2A6B)

</div>

<br>

<div align="center">
  <i>⚙ &nbsp; Engineers turn dreams into reallity &nbsp; ⚙</i>
</div>

<br>

---

## 📜 &nbsp; Table of Contents

- [⚙ System Description](#-system-description)
- [🔩 Node Architecture](#-node-architecture)
- [🗝 Node Reference](#-node-reference)
- [⚗ Installation](#-installation)
- [🔧 Use](#-use)
- [🛰 Remote Development — SSH to the Jetson Orin](#-remote-development-ssh-to-the-jetson-orin)
- [📐 Documentation](#-documentation)
- [📋 Suggested reading](#-suggested-reading)

---

## ⚙ &nbsp; System Description


> **PuzzleBot** is a two-wheeled differential mobile robot originally designed by [**Manchester Robotics**](https://manchester-robotics.com/puzzlebot-jetson-edition-1) as an educational platform for autonomous robotics using ROS 2. Its compact chassis integrates DC motors with encoders, a camera, and an embedded computer on a lightweight, maneuverable base.

<div align="center">
  <a href="https://manchester-robotics.com/puzzlebot-jetson-edition-1" target="_blank">
    <img width="512" height="487" alt="PuzzleBot — Manchester Robotics"
      src="https://github.com/user-attachments/assets/5abafcda-127f-4a56-9c36-d479c151898f" />
  </a>
</div>


### 🔩 &nbsp; Hardware — Custom settings

This unit features the following **modifications over the base model**:

| 🔧 Component | 📜 Details |
|--------------|-----------|
| <img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/e896531c-cbba-486e-98ee-4c74a876cf06" /> | **NVIDIA Jetson Orin Nano** |
| <img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/06a99699-42d4-44cc-9818-a58b14a85199" /> | Litio **4 500 mAh** — greater operational autonomy |
| <img width="200" height="200" alt="Checador de voltaje" src="https://github.com/user-attachments/assets/da89b30c-942c-4e30-a631-92b31f669de5" /> | Voltage monitor for real-time load monitoring |

### 💾 &nbsp; Software — Módulos ROS 2

This repository implements four nodes on **ROS 2 (Humble)** that run directly on the Jetson Orin:

| ⚙ Module | 📜 Function |
|----------|-----------|
| 🚦 Traffic light detection | Computer vision using HSV filters to classify traffic signs in real time |
| 🧭 Differential odometry | Continuous position estimation using 100 Hz wheel encoders |
| 🎯 Closed-loop control | Point-to-point navigation with proportional angle and distance correction |
| 🗺 Trajectory Generator | Configurable sequencing of target points with arrival detection |

---

## 🔩 &nbsp; Node Architecture

**Insertar rqt graph**

## 🗝 &nbsp; Node Reference

| ⚙ Node | 📄 Archive | 📡 Suscribe | 📢 Publish |
|--------|-----------|------------|-----------|
| `traffic_supervisor` | `traffic_supervisor.py` | `/video_source/raw`, `/cmd_vel_raw` | `/cmd_vel` |
| `closeloop` | `closeloop.py` | `/odom`, `/next_point` | `/cmd_vel_raw` |
| `odometry` | `odometry.py` | `/VelocityEncR`, `/VelocityEncL` | `/odom` |
| `path_generator` | `path_generator.py` | `/odom` | `/next_point` |

### 📡 &nbsp; Tópicos completos

| Topic | Message type | Description |
|--------|----------------|-------------|
| `/video_source/raw` | `sensor_msgs/Image` | Raw camera image |
| `/VelocityEncR` | `std_msgs/Float32` | Angular velocity of the right encoder |
| `/VelocityEncL` | `std_msgs/Float32` | Angular velocity of the left encoder |
| `/odom` | `turtlesim/Pose` | Position estimated by odometry `(x, y, θ)` |
| `/next_point` | `turtlesim/Pose` | Next target |
| `/cmd_vel_raw` | `geometry_msgs/Twist` | Controller speed (unfiltered) |
| `/cmd_vel` | `geometry_msgs/Twist` | Final speed sent to the robot |

---

## ⚗ &nbsp; Installation

### Prerequisites

```bash
# ROS 2 Humble — https://docs.ros.org/en/humble/Installation.html
sudo apt install ros-humble-cv-bridge \
                 ros-humble-sensor-msgs \
                 ros-humble-turtlesim

pip install opencv-python numpy
```

### Clone and compile

```bash
# 1. Clone the repository
git clone https://github.com/<usuario>/puzzlebot-nav.git
cd puzzlebot-nav

# 2. Compile the workspace
colcon build --symlink-install

# 3. Load the environment
source install/setup.bash
```

---

## 🔧 &nbsp; Use

### Launch the entire system
> Note: Compile first 

```bash
# Terminal:
ros2 launch semaforo semaforo_launch.xml

```
> The launcher is responsible for launching all the necessary files (path_generator.py, odometry.py, closeloop.py traffic_supervisor.py)

### Monitor the system

```bash
# View traffic light status in real time
ros2 topic echo /cmd_vel

# View the robot's pose
ros2 topic echo /odom

# View the current target
ros2 topic echo /next_point
```

---

## 🛰 &nbsp; Remote Development — SSH to the Jetson Orin

> *“The vision node (color detection) needs to run directly on the Jetson Orin, because otherwise there is a significant delay in the robot's response”*

You would typically use an external monitor to upload the program directly to the Jetson; however, it is possible to program and run code **directly on the Jetson Orin from your computer**, without a USB cable, using SSH over the local network. This allows you to edit files, compile, and run nodes as if you were at the Orin’s terminal.

### 🔑 &nbsp; Set up SSH access

```bash
# 1. Make sure that the Orin and your PC are on the same Wi-Fi network

# 2. Get the IP address of the Jetson Orin (run on the Orin)
hostname -I

# 3. From your computer, connect via SSH
ssh usuario@<IP_DE_LA_ORIN>
# Example: ssh jetson@192.168.1.42
```

### 📁 &nbsp; Mount the Orin filesystem in your file browser

You can browse and edit Orin's files directly from your **PC's file explorer** (without using the terminal) by mounting its filesystem via SFTP:

<details>
<summary>🪟 &nbsp;<b>Windows</b> &nbsp;—&nbsp; WinSCP o Windows Explorer</summary>

<br>

**Option A — Windows Explorer nativo:**
1. Open File Explorer
2. In the address bar, type:  
   ```
   \\sshfs\usuario@192.168.1.42
   ```
   *(requires installation [SSHFS-Win](https://github.com/winfsp/sshfs-win))*

**Option B — WinSCP (recommended):**
1. Download [WinSCP](https://winscp.net)
2. Protocol: `SFTP` · Host: `<IP_DE_LA_ORIN>` · Port: `22`
3. Enter your username and password → log in
4. Drag and drop files between your PC and the Orin

</details>

<details>
<summary>🍎 &nbsp;<b>macOS</b> &nbsp;—&nbsp; Finder vía SFTP</summary>

<br>

1. In Finder: `Ir` → `Conectarse al servidor…` (`⌘K`)
2. Write:
   ```
   sftp://usuario@192.168.1.42
   ```
3. Enter the password → the Orin appears as a volume in Finder

</details>

<details>
<summary>🐧 &nbsp;<b>Linux</b> &nbsp;—&nbsp; Nautilus / Dolphin / sshfs</summary>

<br>

**Graphical file manager (Nautilus/Dolphin):**
- In the address bar, type:
  ```
  sftp://usuario@192.168.1.42/home/usuario/
  ```

**By the terminal with sshfs:**
```bash
# Install sshfs if it isn't already installed
sudo apt install sshfs

# Create mounting point
mkdir -p ~/orin_ws

# Set up the Orin homepage
sshfs usuario@192.168.1.42:/home/usuario ~/orin_ws

# Take it apart when you're done
fusermount -u ~/orin_ws
```

</details>

<details>
<summary>💻 &nbsp;<b>VS Code</b> &nbsp;—&nbsp; Extension Remote SSH (recomendado para desarrollo)</summary>

<br>



</details>

---

## 📐 &nbsp; Documentación 

<details>
<summary>🚦 &nbsp;<b>traffic_supervisor.py</b> &nbsp;—&nbsp; Supervisor de Semáforo</summary>

<br>

The controller monitors the traffic flow and adjusts it based on the traffic light status, which is detected through HSV analysis of each camera frame.

**State machine:**

```
🟢 GREEN  (×1.0) ──── detects yellow ────▶ 🟡 YELLOW (×0.5)
🟡 YELLOW (×0.5) ──── detects red    ────▶ 🔴 RED    (×0.0)  ← robot detenido
🔴 RED    (×0.0) ──── detects green    ────▶ 🟢 GREEN  (×1.0)
```

> We also implemented the ability to jump directly from `GREEN` to `RED`.

**HSV detection ranges:**

| Color | H min | H max | S min | V min | Area minimum |
|-------|-------|-------|-------|-------|-------------|
| 🟢 Verde   | 40  | 80  | 50  | 50  | 600 px² |
| 🟡 Amarillo | 20  | 35  | 100 | 100 | 600 px² |
| 🔴 Rojo    | 0–10 / 170–180 | — | 150 | 120 | 600 px² |

**Key metrics:**

```python
speed_multiplier = 1.0   # GREEN  — full speed
speed_multiplier = 0.5   # YELLOW — low speed
speed_multiplier = 0.0   # RED    — robot stop
```

</details>

---

<details>
<summary>🎮 &nbsp;<b>closeloop.py</b> &nbsp;—&nbsp; Controlador de Lazo Cerrado</summary>

<br>

**Two-phase** proportional controller for point-to-point navigation:

**Phase 1 — Angular Alignment** `(state1)`

```
e_θ = atan2(dy, dx) − θ_actual     standardized a (−π, π]
ω   = clamp(Kw × e_θ, −0.5, 0.5)  Kw = 1.2
```

**Phase 2 — Linear Progress** `(state2)`

```
d = √(dx² + dy²)
v = min(v_max, Kv × d)   Kv = 0.5,  v_max = 0.4 m/s
ω = Kw × e_θ             continuous angular correction
```

**Arrival tolerances:**

| Parameter | Value |
|-----------|-------|
| Distance  | `< 0.02 m` |
| Angle     | `< 0.03 rad` |


**Close loop**

The controller implements the control law using a **finite-state machine** that divides the motion into two phases, preventing the robot from turning and moving forward simultaneously to improve accuracy.

> In the first state (state1 - orientation), the controller applies a proportional gain Kω to the orientation error eθ so that the robot rotates about its own axis until its head points directly toward the target. Once eθ falls within the angular tolerance threshold, the system transitions to the second state.

> In the second state (state2 - translation), the controller uses eₚ as the primary error to generate linear velocity using the gain Kv, while maintaining active angular correction on eθ with the gain Kω to compensate for possible deviations during translation. 

Both control actions are published to /cmd_vel as a Twist message with the components linear.x and angular.z. When the robot reaches the desired point within the defined position tolerance threshold, it transitions to the stop state, halts, and releases the current target, remaining in wait for the next point published by the path generator to restart the cycle.


</details>

---

<details>
<summary>🔩 &nbsp;<b>odometry.py</b> &nbsp;—&nbsp; Nodo de Odometría</summary>

<br>

Implementation of **differential odometry** at 100 Hz using wheel encoders:

**Differential kinematics:**

```
v = r · (ωR + ωL) / 2        r = 0.052 m  (wheel radius)
ω = r · (ωR − ωL) / L        L = 0.180 m  (wheelbase)
```
<div align="center">
  <img width="535" height="472" alt="image" src="https://github.com/user-attachments/assets/870cac85-af14-4a78-bf87-bd9b547f156e" />
</div>

**Position integration:**

```
x     += v · Δt · cos(θ)
y     += v · Δt · sin(θ)
θ     += ω · Δt
θ      = atan2(sin θ, cos θ)   ← continuous normalization to (−π, π]
```

You can also simulate this by posting `(x, y, θ)` to the `/odom` topic in `turtlesim/Pose`.

</details>

---

<details>
<summary>🗺 &nbsp;<b>path_generator.py</b> &nbsp;—&nbsp; Generador de Trayectoria</summary>

<br>

Send target points to the controller in sequence. Move on to the next point when `euclidean_distance < 0.1 m`.

**Customizable paths:**

| Figure | Checkpoints |
|--------|---------------|
| ⬜ Square 2×2 m | `(2,0) → (2,2) → (0,2) → (0,0)` |
| 🔺 Equilateral triangle | `(2,0) → (1, 1.732) → (0,0)` |
|  Trapezoid | `(2,0) → (1.5, 1) → (0.5, 1) → (0,0)` |

To change the path, modify the `point_list` 
</details>

---

## 📋 &nbsp; Suggested reading

```
The following is a suggested list for reference. Sincerely, The developers of this project.
```

**Official page ROS2**
https://www.ros.org/

**Books on Mobile Robotics**

Jazar, R. N. (2010). Theory of applied robotics: Kinematics, dynamics, and control (2nd ed.). Springer.

Spong, M. W., Hutchinson, S., & Vidyasagar, M. (2020). Robot modeling and control (2nd ed.). Wiley.

Lynch, K. M., & Park, F. C. (2017). Modern robotics: Mechanics, planning, and control. Cambridge University Press. https://doi.org/10.1017/9781316661239



<br>

<div align="center">

<sub>⚙ &nbsp; Construido con engranajes, vapor y Python &nbsp; ⚙</sub>

</div>
