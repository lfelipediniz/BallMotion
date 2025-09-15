#!/usr/bin/env python3
"""
Script principal para análise de trajetória 3D de bola com anotações CVAT.

Análise de trajetória com movimento parabólico em z e linear em x,y entre pontos de referência.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from traj3d.cli import main

if __name__ == "__main__":
    main()