"""
utilitários e funções auxiliares para traj3d
"""

import re
import numpy as np


def parse_triplet(txt):
    # recebe "x,y,z" ou "x y z" e converte para floats
    a = re.split(r"[ ,;]+", txt.strip())
    if len(a) != 3:
        raise ValueError(f"esperado 3 valores, recebi: {txt}")
    return float(a[0]), float(a[1]), float(a[2])


def validate_video_path(video_path):
    # valida se o caminho do vídeo é válido
    import os
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"arquivo de vídeo não encontrado: {video_path}")
    return True


def validate_xml_path(xml_path):
    # valida se o caminho do xml é válido
    import os
    if not os.path.exists(xml_path):
        raise FileNotFoundError(f"arquivo XML não encontrado: {xml_path}")
    return True


def clamp(value, min_val, max_val):
    # limita um valor entre min_val e max_val
    return max(min_val, min(max_val, value))


def safe_divide(numerator, denominator, default=0.0):
    # divisão segura que retorna default quando denominador é zero
    if abs(denominator) < 1e-9:
        return default
    return numerator / denominator
