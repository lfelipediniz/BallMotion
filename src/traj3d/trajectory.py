"""
módulo para construção de trajetórias 3d
"""

import numpy as np
import pandas as pd
from .utils import safe_divide


def build_trajectory(total_frames, f0, f1, fps, p0, p1, g=9.81):
    """
    trajetória só em termos de posição

    raciocínio:
    - t0=f0/fps, t1=f1/fps e T=t1-t0
    - criamos s em [0,1] a partir do tempo: s = clamp((t - t0)/T, 0, 1)
    - x(s) e y(s) avançam linearmente de p0 para p1
    - z(s) é parabólico: z(s) = z0 + (z1 - z0)*s + 0.5*g*T*T*s*(1 - s)
    """
    frames = np.arange(total_frames, dtype=int)
    t = frames / float(fps)

    t0 = f0 / float(fps)
    t1 = f1 / float(fps)
    T = max(t1 - t0, 1e-9)  # evita divisão por zero

    x0, y0, z0 = p0
    x1, y1, z1 = p1

    # parâmetro de progresso s ao longo do voo
    s = (t - t0) / T
    s = np.where(t <= t0, 0.0, np.where(t >= t1, 1.0, s))

    # posições finais
    x = x0 + s * (x1 - x0)
    y = y0 + s * (y1 - y0)
    z = z0 + (z1 - z0) * s + 0.5 * g * (T*T) * s * (1.0 - s)

    return pd.DataFrame({"frame": frames, "t": t, "x3d": x, "y3d": y, "z3d": z})


def make_position_functions(f0, f1, fps, p0, p1, g=9.81):
    """
    Calcula coeficientes para derivação algébrica das funções de posição.
    
    Args:
        f0: Frame de início do voo
        f1: Frame de fim do voo
        fps: Frames por segundo
        p0: Posição inicial (x0, y0, z0)
        p1: Posição final (x1, y1, z1)
        g: Aceleração da gravidade
        
    Returns:
        dict: Parâmetros das funções de posição para derivação
    """
    t0 = f0 / float(fps)
    t1 = f1 / float(fps)
    T = max(t1 - t0, 1e-9)

    x0, y0, z0 = map(float, p0)
    x1, y1, z1 = map(float, p1)

    # coeficientes equivalentes de x(t) = m_x t + q_x e y(t) = m_y t + q_y no trecho
    m_x = (x1 - x0) / T
    q_x = x0 - m_x * t0
    m_y = (y1 - y0) / T
    q_y = y0 - m_y * t0

    # coeficientes de z(t) = a t^2 + b t + c no trecho
    # partimos de z = z0 + (z1 - z0)/T * (t - t0) + 0.5*g*T*(t - t0) - 0.5*g*(t - t0)^2
    a = -0.5 * g
    A = (z1 - z0) / T + 0.5 * g * T
    b = A + g * t0
    c = z0 - A * t0 - 0.5 * g * t0 * t0

    params = dict(
        f0=f0, f1=f1, fps=float(fps),
        t0=t0, t1=t1, T=T,
        x0=x0, y0=y0, z0=z0,
        x1=x1, y1=y1, z1=z1,
        g=g,
        m_x=m_x, q_x=q_x, m_y=m_y, q_y=q_y,
        a=a, b=b, c=c
    )
    return params


def interpolate_position(t, params):
    """
    Interpola posição 3D em um tempo específico usando os parâmetros calculados.
    
    Args:
        t: Tempo para interpolação
        params: Parâmetros das funções de posição
        
    Returns:
        tuple: (x, y, z) interpolados
    """
    t0 = params["t0"]
    t1 = params["t1"]
    
    if t <= t0:
        return params["x0"], params["y0"], params["z0"]
    elif t >= t1:
        return params["x1"], params["y1"], params["z1"]
    else:
        # Dentro do intervalo de voo
        m_x, q_x = params["m_x"], params["q_x"]
        m_y, q_y = params["m_y"], params["q_y"]
        a, b, c = params["a"], params["b"], params["c"]
        
        x = m_x * t + q_x
        y = m_y * t + q_y
        z = a * t * t + b * t + c
        
        return x, y, z
