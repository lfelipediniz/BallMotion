# BallMotion

A system designed to analyze the 3D trajectory of a ball in video, combining physics and computer vision to extract position, velocity, and acceleration with visual outputs and annotated results.

## Table of Contents
- [BallMotion](#ballmotion)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
  - [How to Use (Super Easy!)](#how-to-use-super-easy)
    - [Automatic Execution](#automatic-execution)
    - [Required Files](#required-files)
    - [Manual Execution (Advanced)](#manual-execution-advanced)
    - [Programmatic Usage (For Developers)](#programmatic-usage-for-developers)
  - [Project Structure](#project-structure)
  - [Generated Outputs](#generated-outputs)
  - [Advanced Examples](#advanced-examples)
    - [Custom Analysis](#custom-analysis)
    - [Batch Processing](#batch-processing)

## Introduction

**BallMotion** is a framework for analyzing the 3D motion of a ball captured in video. It uses physics-based modeling combined with CVAT annotations to reconstruct trajectories, compute kinematics, and generate detailed visualizations and annotated videos.

## Requirements
- [**Python 3.9+**](https://www.python.org/downloads/)

## How to Use (Super Easy!)

### Automatic Execution 

```bash
# 1. Make the script executable (only the first time)
chmod +x run_example.sh

# 2. Run the project (does everything automatically!)
./run_example.sh
```

**That's it!** The script automatically:

* Checks if Python is installed
* Verifies required files (`bola.mp4` and `annotations.xml`)
* Creates a Python virtual environment
* Installs all dependencies
* Runs the analysis with default parameters
* Generates all files in the `out/` folder

### Required Files
Make sure you have in the project folder:
- `bola.mp4` - your ball video
- `annotations.xml` - CVAT annotations
- `requirements.txt` - dependencies list (already included)

### Manual Execution (Advanced)

If you want to run manually or customize parameters:

```bash
# First, set up the environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Then execute
python -m traj3d.cli --video bola.mp4 --xml annotations.xml --out out
```

### Programmatic Usage (For Developers)

```python
from traj3d import run_analysis

results = run_analysis(
    video_path="bola.mp4",
    xml_path="annotations.xml", 
    output_dir="out",
    camera_pos="7,4,1",
    ball_start="0,7,2.0",
    ball_end="6,6,0",
    g=9.81
)

print("Generated files:")
for key, path in results.items():
    print(f"  {key}: {path}")
```

## Project Structure

```
src/traj3d/
├── cli.py         # main orchestration
├── io_cvat.py     # CVAT XML reading
├── detection.py   # launch/landing detection
├── trajectory.py  # trajectory building
├── kinematics.py  # velocity/acceleration functions
├── derivation.py  # derivation text generation
├── plotting.py    # 3D and components plotting
├── video_annot.py # video annotation utilities
└── utils.py       # helpers and parsing
```

## Generated Outputs

* `series.csv`: numerical trajectory data (position, velocity, acceleration)
* `derivacao_posicao.txt`: full mathematical derivation
* `trajetoria_3d.png`: 3D trajectory plot
* `velocidade_componentes.png`: velocity components
* `aceleracao_componentes.png`: acceleration components
* `bola_annotado.mp4`: annotated video
* `primeiro_frame.png`, `frame_meio.png`, `ultimo_frame.png`: annotated frames

## Advanced Examples

### Custom Analysis

```python
from traj3d import load_cvat_xy, detect_launch_frame, build_trajectory
from traj3d.kinematics import calculate_kinetic_energy
from traj3d.plotting import plot_energy_analysis

df_cvat = load_cvat_xy("annotations.xml")
launch_frame = detect_launch_frame(df_cvat[["frame", "y2d"]])
df_pos = build_trajectory(total_frames, f0, f1, fps, p0, p1, g=9.81)
ke = calculate_kinetic_energy(df_pos, mass=0.27)
plot_energy_analysis(df_pos, "energia.png", mass=0.27)
```

### Batch Processing

```python
import glob
from traj3d import run_analysis
from pathlib import Path

video_files = glob.glob("videos/*.mp4")
xml_files = glob.glob("annotations/*.xml")

for video, xml in zip(video_files, xml_files):
    results = run_analysis(
        video_path=video,
        xml_path=xml,
        output_dir=f"out_{Path(video).stem}"
    )
    print(f"Processed: {video} -> {results['trajectory_png']}")
```

---

**Enjoy the motion! 🏀📈**
