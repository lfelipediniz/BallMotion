"""
módulo para detecção de janela de voo e heurísticas
"""

import numpy as np


def detect_launch_frame(df_xy, threshold=-0.5):
    # procura o primeiro frame com queda mais intensa em y2d
    # observação: em coordenadas de imagem, y cresce para baixo; quando a bola sobe, y diminui
    d = df_xy.copy()
    d["dy"] = d["y2d"].diff()
    m = d["dy"] < threshold
    
    if m.any():
        return int(d.loc[m, "frame"].iloc[0])
    
    # se nada ficar muito evidente, usamos o primeiro frame anotado
    return int(d["frame"].iloc[0])


def detect_landing_frame(df_xy, threshold=0.5):
    # detecta o frame de pouso da bola baseado na subida mais intensa em y2d
    d = df_xy.copy()
    d["dy"] = d["y2d"].diff()
    m = d["dy"] > threshold
    
    if m.any():
        return int(d.loc[m, "frame"].iloc[-1])  # último frame com subida
    
    # se nada ficar muito evidente, usamos o último frame anotado
    return int(d["frame"].iloc[-1])


def find_peak_height_frame(df_xy):
    # encontra o frame onde a bola atinge a altura máxima (menor y2d)
    min_y_idx = df_xy["y2d"].idxmin()
    return int(df_xy.loc[min_y_idx, "frame"])


def calculate_flight_duration(df_xy, fps):
    # calcula a duração estimada do voo baseado nos frames de lançamento e pouso
    launch_frame = detect_launch_frame(df_xy)
    landing_frame = detect_landing_frame(df_xy)
    duration_frames = landing_frame - launch_frame
    return duration_frames / fps
