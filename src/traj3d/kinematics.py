"""
módulo para cálculo de cinemática (velocidade e aceleração)
"""

import numpy as np


def make_velocity_functions(params):
    # deriva x(t), y(t), z(t) exatamente via cálculo diferencial
    t0 = params["t0"]
    t1 = params["t1"]
    m_x = params["m_x"]
    m_y = params["m_y"]
    a = params["a"]
    b = params["b"]

    # helper de trecho: aplica fórmula só em [t0, t1) e zera fora
    # nota: [t0, t1) para garantir que no último frame (t1) a velocidade seja 0
    def piecewise(tt, inside_func):
        tt = np.asarray(tt, dtype=float)
        out = np.zeros_like(tt, dtype=float)
        m = (tt >= t0) & (tt < t1)  # mudança: < t1 em vez de <= t1
        if m.any():
            out[m] = inside_func(tt[m])
        return out

    # vx = dx/dt, vy = dy/dt, vz = dz/dt
    vx = lambda tt: piecewise(tt, lambda u: np.full_like(u, m_x))
    vy = lambda tt: piecewise(tt, lambda u: np.full_like(u, m_y))
    vz = lambda tt: piecewise(tt, lambda u: 2.0 * a * u + b)

    # aceleração: ax = 0, ay = 0, az = d/dt(vz) = 2a = -g no trecho, 0 fora
    ax = lambda tt: piecewise(tt, lambda u: np.zeros_like(u))
    ay = lambda tt: piecewise(tt, lambda u: np.zeros_like(u))
    az = lambda tt: piecewise(tt, lambda u: np.full_like(u, 2.0 * a))

    return vx, vy, vz, ax, ay, az


def build_kinematics(df_pos, params):
    # gera colunas de velocidade e aceleração para cada frame
    t = df_pos["t"].to_numpy()
    vx, vy, vz, ax, ay, az = make_velocity_functions(params)

    v_x = vx(t)
    v_y = vy(t)
    v_z = vz(t)
    a_x = ax(t)
    a_y = ay(t)
    a_z = az(t)

    v_mod = np.sqrt(v_x**2 + v_y**2 + v_z**2)

    out = df_pos.copy()
    out["vx"] = v_x
    out["vy"] = v_y
    out["vz"] = v_z
    out["speed"] = v_mod
    out["ax"] = a_x
    out["ay"] = a_y
    out["az"] = a_z
    return out


def calculate_kinetic_energy(df_kinematics, mass=0.27):
    # calcula energia cinética para cada frame
    speed = df_kinematics["speed"].to_numpy()
    return 0.5 * mass * speed**2


def calculate_potential_energy(df_kinematics, mass=0.27, g=9.81):
    # calcula energia potencial gravitacional para cada frame
    z = df_kinematics["z3d"].to_numpy()
    return mass * g * z


def calculate_total_energy(df_kinematics, mass=0.27, g=9.81):
    # calcula energia total (cinética + potencial) para cada frame
    ke = calculate_kinetic_energy(df_kinematics, mass)
    pe = calculate_potential_energy(df_kinematics, mass, g)
    return ke + pe
