"""
traj3d - análise de trajetória 3d de bola com anotações cvat

este pacote fornece funcionalidades para:
- carregar anotações do cvat
- detectar janela de voo da bola
- construir trajetória 3d com movimento parabólico
- calcular cinemática (velocidade e aceleração)
- visualizar resultados e anotar vídeos
"""

from .cli import main, parse_args, run_analysis
from .io_cvat import load_cvat_xy
from .detection import detect_launch_frame
from .trajectory import build_trajectory, make_position_functions
from .kinematics import make_velocity_functions, build_kinematics
from .derivation import build_derivation_text, print_derivation
from .plotting import plot_xyz, plot_velocity_components, plot_acceleration_components
from .video_annot import annotate_video, extract_key_frames
from .utils import parse_triplet

__version__ = "1.0.0"
__all__ = [
    "main",
    "parse_args",
    "run_analysis",
    "load_cvat_xy",
    "detect_launch_frame",
    "build_trajectory",
    "make_position_functions",
    "make_velocity_functions",
    "build_kinematics",
    "build_derivation_text",
    "print_derivation",
    "plot_xyz",
    "plot_velocity_components",
    "plot_acceleration_components",
    "annotate_video",
    "extract_key_frames",
    "parse_triplet",
]
