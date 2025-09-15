"""
módulo para visualização e plotagem
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa


def plot_xyz(df, out_png, cam_xyz, p0, p1):
    # plota em gráfico 3d a trajetória da bola na sala
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    x = df["x3d"].to_numpy()
    y = df["y3d"].to_numpy()
    z = df["z3d"].to_numpy()
    m = ~(np.isnan(x) | np.isnan(y) | np.isnan(z))

    # curva da trajetória
    if m.any():
        ax.plot(x[m], y[m], z[m], "b-", lw=3, label="trajetória 3d")

    # pontos de referência
    ax.scatter(*p0, c="green", s=160, marker="o", label="início", edgecolors="black", linewidth=1.5)
    ax.scatter(*p1, c="red", s=160, marker="s", label="fim", edgecolors="black", linewidth=1.5)
    ax.scatter(*cam_xyz, c="purple", s=180, marker="^", label="câmera", edgecolors="black", linewidth=1.5)

    # limites de x e y a partir de 0
    cx, cy, cz = map(float, cam_xyz)
    x_all = np.r_[x[m] if m.any() else [], [p0[0], p1[0], cx, 0.0]]
    y_all = np.r_[y[m] if m.any() else [], [p0[1], p1[1], cy, 0.0]]
    L = float(max(np.max(x_all), np.max(y_all)))
    L = 1.0 if not np.isfinite(L) or L <= 0 else L
    pad = 0.05 * L
    ax.set_xlim(0, L + pad)
    ax.set_ylim(0, L + pad)
    ax.invert_yaxis()

    # limites de z a partir de 0
    z_all = np.r_[z[m] if m.any() else [], [p0[2], p1[2], cz, 0.0]]
    Z = float(np.max(z_all))
    Z = 1.0 if not np.isfinite(Z) or Z <= 0 else Z
    ax.set_zlim(0, Z + 0.05*Z)

    # linhas de leitura de altura
    ax.plot([cx, cx], [cy, cy], [0, cz], "--", color="k", lw=1.4, alpha=0.9)  # câmera
    if m.any():
        i_peak = int(np.nanargmax(z))
        bx, by, bz = float(x[i_peak]), float(y[i_peak]), float(z[i_peak])
        ax.plot([bx, bx], [by, by], [0, bz], "--", color="gray", lw=1.4, alpha=0.9)  # pico
    if p0[2] > 0:
        ax.plot([p0[0], p0[0]], [p0[1], p0[1]], [0, p0[2]], "--", color="green", lw=1.0, alpha=0.8)  # início elevado

    # vista padrão
    ax.view_init(elev=25, azim=-45)

    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_zlabel("z [m]")
    ax.set_title("trajetória 3d")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # eixos de referência no plano z=0
    ax.scatter(0.0, 0.0, 0.0, s=60, c="k", marker="o", depthshade=False)
    ax.plot([0, L+pad], [0, 0], [0, 0], color="k", lw=1.0, alpha=0.8)
    ax.plot([0, 0], [0, L+pad], [0, 0], color="k", lw=1.0, alpha=0.8)

    fig.tight_layout()
    fig.savefig(out_png, dpi=160)
    plt.close(fig)


def plot_velocity_components(df, out_png):
    # plota componentes de velocidade ao longo do tempo
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    t = df["t"].to_numpy()
    
    # Velocidade x
    axes[0, 0].plot(t, df["vx"], "r-", lw=2)
    axes[0, 0].set_xlabel("Tempo [s]")
    axes[0, 0].set_ylabel("vx [m/s]")
    axes[0, 0].set_title("Velocidade X")
    axes[0, 0].grid(True, alpha=0.3)
    
    # Velocidade y
    axes[0, 1].plot(t, df["vy"], "g-", lw=2)
    axes[0, 1].set_xlabel("Tempo [s]")
    axes[0, 1].set_ylabel("vy [m/s]")
    axes[0, 1].set_title("Velocidade Y")
    axes[0, 1].grid(True, alpha=0.3)
    
    # Velocidade z
    axes[1, 0].plot(t, df["vz"], "b-", lw=2)
    axes[1, 0].set_xlabel("Tempo [s]")
    axes[1, 0].set_ylabel("vz [m/s]")
    axes[1, 0].set_title("Velocidade Z")
    axes[1, 0].grid(True, alpha=0.3)
    
    # Módulo da velocidade
    axes[1, 1].plot(t, df["speed"], "k-", lw=2)
    axes[1, 1].set_xlabel("Tempo [s]")
    axes[1, 1].set_ylabel("|v| [m/s]")
    axes[1, 1].set_title("Módulo da Velocidade")
    axes[1, 1].grid(True, alpha=0.3)
    
    fig.tight_layout()
    fig.savefig(out_png, dpi=160)
    plt.close(fig)


def plot_acceleration_components(df, out_png):
    # plota componentes de aceleração ao longo do tempo
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    t = df["t"].to_numpy()
    
    # Aceleração x
    axes[0, 0].plot(t, df["ax"], "r-", lw=2)
    axes[0, 0].set_xlabel("Tempo [s]")
    axes[0, 0].set_ylabel("ax [m/s²]")
    axes[0, 0].set_title("Aceleração X")
    axes[0, 0].grid(True, alpha=0.3)
    
    # Aceleração y
    axes[0, 1].plot(t, df["ay"], "g-", lw=2)
    axes[0, 1].set_xlabel("Tempo [s]")
    axes[0, 1].set_ylabel("ay [m/s²]")
    axes[0, 1].set_title("Aceleração Y")
    axes[0, 1].grid(True, alpha=0.3)
    
    # Aceleração z
    axes[1, 0].plot(t, df["az"], "b-", lw=2)
    axes[1, 0].set_xlabel("Tempo [s]")
    axes[1, 0].set_ylabel("az [m/s²]")
    axes[1, 0].set_title("Aceleração Z")
    axes[1, 0].grid(True, alpha=0.3)
    
    # Módulo da aceleração
    a_mod = np.sqrt(df["ax"]**2 + df["ay"]**2 + df["az"]**2)
    axes[1, 1].plot(t, a_mod, "k-", lw=2)
    axes[1, 1].set_xlabel("Tempo [s]")
    axes[1, 1].set_ylabel("|a| [m/s²]")
    axes[1, 1].set_title("Módulo da Aceleração")
    axes[1, 1].grid(True, alpha=0.3)
    
    fig.tight_layout()
    fig.savefig(out_png, dpi=160)
    plt.close(fig)


def plot_energy_analysis(df, out_png, mass=0.27, g=9.81):
    # plota análise de energia (cinética, potencial e total)
    from .kinematics import calculate_kinetic_energy, calculate_potential_energy, calculate_total_energy
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    t = df["t"].to_numpy()
    ke = calculate_kinetic_energy(df, mass)
    pe = calculate_potential_energy(df, mass, g)
    te = calculate_total_energy(df, mass, g)
    
    ax.plot(t, ke, "r-", lw=2, label="Energia Cinética")
    ax.plot(t, pe, "g-", lw=2, label="Energia Potencial")
    ax.plot(t, te, "k-", lw=2, label="Energia Total")
    
    ax.set_xlabel("Tempo [s]")
    ax.set_ylabel("Energia [J]")
    ax.set_title("Análise de Energia")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    fig.tight_layout()
    fig.savefig(out_png, dpi=160)
    plt.close(fig)
