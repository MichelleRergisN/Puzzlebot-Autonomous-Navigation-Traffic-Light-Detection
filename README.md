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

## 📜 &nbsp; Tabla de Contenidos

- [⚙ Descripción del Sistema](#-descripción-del-sistema)
- [🔩 Arquitectura de Nodos](#-arquitectura-de-nodos)
- [🗝 Referencia de Nodos](#-referencia-de-nodos)
- [⚗ Instalación](#-instalación)
- [🔧 Uso](#-uso)
- [🛰 Desarrollo Remoto — SSH hacia la Jetson Orin](#-desarrollo-remoto--ssh-hacia-la-jetson-orin)
- [📐 Documentación Detallada](#-documentación)
- [📋 Documentación sugerida](#-documentación-sugerida)

---

## ⚙ &nbsp; Descripción del Sistema

> **PuzzleBot** es un robot móvil diferencial de **dos ruedas** diseñado originalmente por [**Manchester Robotics**](https://manchester-robotics.com/puzzlebot-jetson-edition-1) como plataforma educativa para robótica autónoma con ROS 2. Su chasis compacto integra motores DC con encoders, cámara y computadora embebida sobre una base ligera y maniobrable.

<div align="center">
  <a href="https://manchester-robotics.com/puzzlebot-jetson-edition-1" target="_blank">
    <img width="512" height="487" alt="PuzzleBot — Manchester Robotics"
      src="https://github.com/user-attachments/assets/5abafcda-127f-4a56-9c36-d479c151898f" />
  </a>
</div>


### 🔩 &nbsp; Hardware — Configuración personalizada

Esta unidad cuenta con las siguientes **modificaciones sobre el modelo base**:

| 🔧 Componente | 📜 Detalle |
|--------------|-----------|
| <img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/e896531c-cbba-486e-98ee-4c74a876cf06" /> | **NVIDIA Jetson Orin Nano** |
| <img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/06a99699-42d4-44cc-9818-a58b14a85199" /> | Litio **4 500 mAh** — mayor autonomía de operación |
| <img width="200" height="200" alt="Checador de voltaje" src="https://github.com/user-attachments/assets/da89b30c-942c-4e30-a631-92b31f669de5" /> | Checador de voltaje en línea para supervisión de carga en tiempo real |

### 💾 &nbsp; Software — Módulos ROS 2

Este repositorio implementa cuatro nodos sobre **ROS 2 (Humble)** que se ejecutan directamente en la Jetson Orin:

| ⚙ Módulo | 📜 Función |
|----------|-----------|
| 🚦 Detección de semáforos | Visión por computadora con filtros HSV para clasificar señales de tráfico en tiempo real |
| 🧭 Odometría diferencial | Estimación de posición continua a partir de encoders de rueda a 100 Hz |
| 🎯 Control de lazo cerrado | Navegación punto a punto con corrección proporcional de ángulo y distancia |
| 🗺 Generador de trayectorias | Secuenciación configurable de puntos objetivo con detección de llegada |

---

## 🔩 &nbsp; Arquitectura de Nodos

**Insertar rqt graph**

## 🗝 &nbsp; Referencia de Nodos

| ⚙ Nodo | 📄 Archivo | 📡 Suscribe | 📢 Publica |
|--------|-----------|------------|-----------|
| `traffic_supervisor` | `traffic_supervisor.py` | `/video_source/raw`, `/cmd_vel_raw` | `/cmd_vel` |
| `closeloop` | `closeloop.py` | `/odom`, `/next_point` | `/cmd_vel_raw` |
| `odometry` | `odometry.py` | `/VelocityEncR`, `/VelocityEncL` | `/odom` |
| `path_generator` | `path_generator.py` | `/odom` | `/next_point` |

### 📡 &nbsp; Tópicos completos

| Tópico | Tipo de mensaje | Descripción |
|--------|----------------|-------------|
| `/video_source/raw` | `sensor_msgs/Image` | Imagen cruda de la cámara |
| `/VelocityEncR` | `std_msgs/Float32` | Velocidad angular encoder derecho |
| `/VelocityEncL` | `std_msgs/Float32` | Velocidad angular encoder izquierdo |
| `/odom` | `turtlesim/Pose` | Pose estimada por odometría `(x, y, θ)` |
| `/next_point` | `turtlesim/Pose` | Siguiente punto objetivo |
| `/cmd_vel_raw` | `geometry_msgs/Twist` | Velocidad sin filtrar del controlador |
| `/cmd_vel` | `geometry_msgs/Twist` | Velocidad final publicada al robot |

---

## ⚗ &nbsp; Instalación

### Requisitos previos

```bash
# ROS 2 Humble — https://docs.ros.org/en/humble/Installation.html
sudo apt install ros-humble-cv-bridge \
                 ros-humble-sensor-msgs \
                 ros-humble-turtlesim

pip install opencv-python numpy
```

### Clonar y compilar

```bash
# 1. Clonar el repositorio
git clone https://github.com/<usuario>/puzzlebot-nav.git
cd puzzlebot-nav

# 2. Compilar el workspace
colcon build --symlink-install

# 3. Cargar el entorno
source install/setup.bash
```

---

## 🔧 &nbsp; Uso

### Lanzar el sistema completo
> Nota: primero compilar 

```bash
# Terminal:
ros2 launch semaforo semaforo_launch.xml

```
> El launch se encarga de lanzar todos los archivos necesarios (path_generator.py, odometry.py, closeloop.py traffic_supervisor.py)

### Monitorear el sistema

```bash
# Ver el estado del semáforo en tiempo real
ros2 topic echo /cmd_vel

# Visualizar la pose del robot
ros2 topic echo /odom

# Ver el punto objetivo actual
ros2 topic echo /next_point
```

---

## 🛰 &nbsp; Desarrollo Remoto — SSH hacia la Jetson Orin

> *"El nodo de visión (detección de colores) necesita correr directamente en la Jetson Orin, debido a que sino se genera un retraso significativo en la respuesta del robot"*

Usualmente se utilizaría un monitor externo para subir el programa directamente a la Jetson, sin embargo, es posible programar y ejecutar código **directamente en la Jetson Orin desde tu computadora**, sin cable USB, usando SSH sobre la red local. Esto permite editar archivos, compilar y lanzar nodos como si estuvieras en la terminal de la Orin.

### 🔑 &nbsp; Configurar acceso SSH

```bash
# 1. Asegúrate de que la Orin y tu PC estén en la misma red Wi-Fi

# 2. Obtén la IP de la Jetson Orin (ejecutar en la Orin)
hostname -I

# 3. Desde tu computadora, conecta por SSH
ssh usuario@<IP_DE_LA_ORIN>
# Ejemplo: ssh jetson@192.168.1.42
```

### 📁 &nbsp; Montar el filesystem de la Orin en tu explorador de archivos

Puedes navegar y editar los archivos de la Orin directamente desde el **explorador de archivos de tu PC** (sin terminal), montando su filesystem por SFTP:

<details>
<summary>🪟 &nbsp;<b>Windows</b> &nbsp;—&nbsp; WinSCP o Windows Explorer</summary>

<br>

**Opción A — Windows Explorer nativo:**
1. Abre el Explorador de archivos
2. En la barra de dirección escribe:  
   ```
   \\sshfs\usuario@192.168.1.42
   ```
   *(requiere tener instalado [SSHFS-Win](https://github.com/winfsp/sshfs-win))*

**Opción B — WinSCP (recomendado):**
1. Descarga [WinSCP](https://winscp.net)
2. Protocolo: `SFTP` · Host: `<IP_DE_LA_ORIN>` · Puerto: `22`
3. Ingresa usuario y contraseña → conecta
4. Arrastra y suelta archivos entre tu PC y la Orin

</details>

<details>
<summary>🍎 &nbsp;<b>macOS</b> &nbsp;—&nbsp; Finder vía SFTP</summary>

<br>

1. En Finder: `Ir` → `Conectarse al servidor…` (`⌘K`)
2. Escribe:
   ```
   sftp://usuario@192.168.1.42
   ```
3. Ingresa la contraseña → la Orin aparece como unidad en Finder

</details>

<details>
<summary>🐧 &nbsp;<b>Linux</b> &nbsp;—&nbsp; Nautilus / Dolphin / sshfs</summary>

<br>

**Gestor de archivos gráfico (Nautilus/Dolphin):**
- En la barra de dirección escribe:
  ```
  sftp://usuario@192.168.1.42/home/usuario/
  ```

**Por terminal con sshfs:**
```bash
# Instalar sshfs si no está
sudo apt install sshfs

# Crear punto de montaje
mkdir -p ~/orin_ws

# Montar el home de la Orin
sshfs usuario@192.168.1.42:/home/usuario ~/orin_ws

# Desmontar cuando termines
fusermount -u ~/orin_ws
```

</details>

<details>
<summary>💻 &nbsp;<b>VS Code</b> &nbsp;—&nbsp; Extensión Remote SSH (recomendado para desarrollo)</summary>

<br>



</details>

---

## 📐 &nbsp; Documentación 

<details>
<summary>🚦 &nbsp;<b>traffic_supervisor.py</b> &nbsp;—&nbsp; Supervisor de Semáforo</summary>

<br>

El supervisor intercepta el flujo de velocidad y lo modula según el estado del semáforo detectado mediante análisis HSV de cada frame de cámara.

**Máquina de estados:**

```
🟢 GREEN  (×1.0) ──── detecta amarillo ────▶ 🟡 YELLOW (×0.5)
🟡 YELLOW (×0.5) ──── detecta rojo     ────▶ 🔴 RED    (×0.0)  ← robot detenido
🔴 RED    (×0.0) ──── detecta verde    ────▶ 🟢 GREEN  (×1.0)
```

> También se implementó que pudiera saltar de `GREEN` a `RED` directamente.

**Rangos de detección HSV:**

| Color | H min | H max | S min | V min | Área mínima |
|-------|-------|-------|-------|-------|-------------|
| 🟢 Verde   | 40  | 80  | 50  | 50  | 600 px² |
| 🟡 Amarillo | 20  | 35  | 100 | 100 | 600 px² |
| 🔴 Rojo    | 0–10 / 170–180 | — | 150 | 120 | 600 px² |

**Parámetros clave:**

```python
speed_multiplier = 1.0   # GREEN  — velocidad completa
speed_multiplier = 0.5   # YELLOW — velocidad reducida
speed_multiplier = 0.0   # RED    — robot detenido
```

</details>

---

<details>
<summary>🎮 &nbsp;<b>closeloop.py</b> &nbsp;—&nbsp; Controlador de Lazo Cerrado</summary>

<br>

Controlador proporcional de **dos fases** para navegación punto a punto:

**Fase 1 — Alineación angular** `(state1)`

```
e_θ = atan2(dy, dx) − θ_actual     normalizado a (−π, π]
ω   = clamp(Kw × e_θ, −0.5, 0.5)  Kw = 1.2
```

**Fase 2 — Avance lineal** `(state2)`

```
d = √(dx² + dy²)
v = min(v_max, Kv × d)   Kv = 0.5,  v_max = 0.4 m/s
ω = Kw × e_θ             corrección angular continua
```

**Tolerancias de llegada:**

| Parámetro | Valor |
|-----------|-------|
| Distancia | `< 0.02 m` |
| Ángulo    | `< 0.03 rad` |


**Close loop**

El controlador aplica la ley de control mediante una **máquina de estados finitos** que separa el movimiento en dos fases, evitando que el robot gire y avance simultáneamente para mejorar la precisión.

> En el primer estado (state1 - orientación), el controlador aplica una ganancia proporcional Kω sobre el error de orientación eθ para que el robot gire sobre su propio eje hasta que su encabezado apunte directamente hacia el objetivo. Una vez que eθ cae dentro del umbral de tolerancia angular, el sistema transiciona al segundo estado.

> En el segundo estado (state2 - traslación), el controlador utiliza eₚ como error principal para generar la velocidad lineal mediante la ganancia Kv, mientras mantiene una corrección angular activa sobre eθ con la ganancia Kω para compensar posibles desviaciones durante el avance. 

Ambas acciones de control se publican en /cmd_vel como un mensaje Twist con las componentes linear.x y angular.z. Cuando el robot alcanza el punto deseado dentro del umbral de tolerancia de posición definido, transiciona al estado stop, se detiene y libera el objetivo actual, quedando en espera del siguiente punto publicado por el path generator para reiniciar el ciclo.


</details>

---

<details>
<summary>🔩 &nbsp;<b>odometry.py</b> &nbsp;—&nbsp; Nodo de Odometría</summary>

<br>

Integración de **odometría diferencial** a 100 Hz usando encoders de rueda:

**Cinemática diferencial:**

```
v = r · (ωR + ωL) / 2        r = 0.052 m  (radio de rueda)
ω = r · (ωR − ωL) / L        L = 0.180 m  (distancia entre ruedas)
```
<div align="center">
  <img width="535" height="472" alt="image" src="https://github.com/user-attachments/assets/870cac85-af14-4a78-bf87-bd9b547f156e" />
</div>

**Integración de posición:**

```
x     += v · Δt · cos(θ)
y     += v · Δt · sin(θ)
θ     += ω · Δt
θ      = atan2(sin θ, cos θ)   ← normalización continua a (−π, π]
```

Tambien se puede simular publicando en `turtlesim/Pose` con `(x, y, θ)` en el tópico `/odom`.

</details>

---

<details>
<summary>🗺 &nbsp;<b>path_generator.py</b> &nbsp;—&nbsp; Generador de Trayectoria</summary>

<br>

Publica secuencialmente puntos objetivo al controlador. Avanza al siguiente punto cuando `distancia_euclidiana < 0.1 m`.

**Trayectorias configurables:**

| Figura | Puntos de paso |
|--------|---------------|
| ⬜ Cuadrado 2×2 m | `(2,0) → (2,2) → (0,2) → (0,0)` |
| 🔺 Triángulo equilátero | `(2,0) → (1, 1.732) → (0,0)` |
|  Trapecio | `(2,0) → (1.5, 1) → (0.5, 1) → (0,0)` |

Para cambiar la trayectoria, modifica la lista `point_list` en `__init__`.

</details>

---

## 📋 &nbsp; Documentación sugerida

```
Las siguientes son una lista sugerida de consulta. Att. Los desarrolladores de este proyecto.
```

**Página oficial ROS2**
https://www.ros.org/

**Libros de robótica móvil**

Jazar, R. N. (2010). Theory of applied robotics: Kinematics, dynamics, and control (2nd ed.). Springer.

Spong, M. W., Hutchinson, S., & Vidyasagar, M. (2020). Robot modeling and control (2nd ed.). Wiley.

Lynch, K. M., & Park, F. C. (2017). Modern robotics: Mechanics, planning, and control. Cambridge University Press. https://doi.org/10.1017/9781316661239



<br>

<div align="center">

<sub>⚙ &nbsp; Construido con engranajes, vapor y Python &nbsp; ⚙</sub>

</div>
