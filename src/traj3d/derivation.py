"""
módulo para derivação algébrica e textual
"""


def build_derivation_text(params):
    # monta texto que primeiro lista variáveis, depois mostra fórmulas simbólicas,
    # e por fim apresenta as expansões calculadas, as derivadas e uma checagem por integral
    t0 = params["t0"]
    t1 = params["t1"]
    T = params["T"]
    x0 = params["x0"]
    y0 = params["y0"]
    z0 = params["z0"]
    x1 = params["x1"]
    y1 = params["y1"]
    z1 = params["z1"]
    g = params["g"]

    m_x = params["m_x"]
    q_x = params["q_x"]
    m_y = params["m_y"]
    q_y = params["q_y"]
    a = params["a"]
    b = params["b"]
    c = params["c"]

    lines = []

    # bloco 1: variáveis com valores
    lines.append("variaveis e valores")
    lines.append("--------------------------------")
    lines.append(f"f0 = {params['f0']}  f1 = {params['f1']}  fps = {params['fps']:.6f}")
    lines.append(f"t0 = {t0:.6f}  t1 = {t1:.6f}  T = {T:.6f}")
    lines.append(f"x0 = {x0:.6f}  y0 = {y0:.6f}  z0 = {z0:.6f}")
    lines.append(f"x1 = {x1:.6f}  y1 = {y1:.6f}  z1 = {z1:.6f}")
    lines.append(f"g  = {g:.6f}")
    lines.append("")

    # bloco 2: fórmulas simbólicas com variáveis
    lines.append("formulas simbolicas")
    lines.append("--------------------------------")
    lines.append("para t em [t0, t1]:")
    lines.append("x(t) = x0 + (x1 - x0) * (t - t0) / T")
    lines.append("y(t) = y0 + (y1 - y0) * (t - t0) / T")
    lines.append("z(t) = z0 + (z1 - z0) * (t - t0) / T + 0.5 * g * T * (t - t0) - 0.5 * g * (t - t0)^2")
    lines.append("equivalente no trecho: z(t) = a * t^2 + b * t + c")
    lines.append("fora do voo: t <= t0 usa (x0, y0, z0) e t >= t1 usa (x1, y1, z1)")
    lines.append("")

    # bloco 3: contas feitas pelo computador - expansões e coeficientes
    lines.append("expansoes e coeficientes calculados")
    lines.append("--------------------------------")
    # x e y
    lines.append("x(t):")
    lines.append("  x(t) = x0 + (x1 - x0)/T * (t - t0)")
    lines.append("       = [(x1 - x0)/T] * t + [x0 - (x1 - x0)/T * t0]")
    lines.append(f"  onde m_x = (x1 - x0)/T = {m_x:.6f}  e  q_x = x0 - m_x * t0 = {q_x:.6f}")
    lines.append(f"  portanto, x(t) = {m_x:.6f} * t + {q_x:.6f}")
    lines.append("")
    lines.append("y(t):")
    lines.append("  y(t) = y0 + (y1 - y0)/T * (t - t0)")
    lines.append("       = [(y1 - y0)/T] * t + [y0 - (y1 - y0)/T * t0]")
    lines.append(f"  onde m_y = (y1 - y0)/T = {m_y:.6f}  e  q_y = y0 - m_y * t0 = {q_y:.6f}")
    lines.append(f"  portanto, y(t) = {m_y:.6f} * t + {q_y:.6f}")
    lines.append("")
    # z
    lines.append("z(t):")
    lines.append("  partimos de z = z0 + (z1 - z0)/T * (t - t0) + 0.5*g*T*(t - t0) - 0.5*g*(t - t0)^2")
    lines.append("  expandindo (t - t0)^2 = t^2 - 2*t0*t + t0^2")
    lines.append("  agrupando em z(t) = a*t^2 + b*t + c, obtemos:")
    lines.append("    a = -0.5*g")
    lines.append("    b = (z1 - z0)/T + 0.5*g*T + g*t0")
    lines.append("    c = z0 - [(z1 - z0)/T + 0.5*g*T]*t0 - 0.5*g*t0^2")
    lines.append(f"  valores: a = {a:.6f}  b = {b:.6f}  c = {c:.6f}")
    lines.append(f"  portanto, z(t) = {a:.6f} * t^2 + {b:.6f} * t + {c:.6f}")
    lines.append("")

    # bloco 4: derivação por cálculo diferencial - velocidade e aceleração
    lines.append("derivacao por calculo diferencial - velocidade e aceleracao")
    lines.append("--------------------------------")
    lines.append("no trecho t em [t0, t1]:")
    lines.append(f"  vx(t) = dx/dt = m_x = {m_x:.6f}")
    lines.append(f"  vy(t) = dy/dt = m_y = {m_y:.6f}")
    lines.append(f"  vz(t) = dz/dt = 2*a*t + b = {2*a:.6f}*t + {b:.6f}")
    lines.append("fora do trecho, as funções foram clampadas, então v(t) = 0")
    lines.append("")
    lines.append("modulo da velocidade:")
    lines.append("  |v(t)| = sqrt( vx(t)^2 + vy(t)^2 + vz(t)^2 )")
    lines.append(f"         = sqrt( {m_x:.6f}^2 + {m_y:.6f}^2 + ( {2*a:.6f}*t + {b:.6f} )^2 )")
    lines.append("")
    lines.append("aceleracao:")
    lines.append("  ax(t) = 0")
    lines.append("  ay(t) = 0")
    lines.append(f"  az(t) = d/dt[vz(t)] = 2*a = {2*a:.6f}  que equivale a -g")
    lines.append("")

    # bloco 5: checagem por integral - voltando de v(t) para z(t)
    lines.append("checagem por integral")
    lines.append("--------------------------------")
    lines.append("  integrando vz(t) = 2*a*t + b:  ∫vz dt = a*t^2 + b*t + C")
    lines.append("  impondo z(t0) = z0, obtemos C = c, logo z(t) = a*t^2 + b*t + c")
    lines.append("  idem para x e y:  ∫vx dt = m_x*t + Cx, com Cx = q_x  -  ok")
    lines.append("")

    return "\n".join(lines)


def print_derivation(params, out_path=None):
    # imprime no terminal e salva em arquivo se out_path for dado
    header = "derivacao da posicao, velocidade e aceleracao\n--------------------------------"
    txt = header + "\n" + build_derivation_text(params)
    print(txt)
    if out_path is not None:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(txt + "\n")


def format_derivation_summary(params):
    # cria um resumo mais conciso da derivação
    t0 = params["t0"]
    t1 = params["t1"]
    T = params["T"]
    m_x = params["m_x"]
    m_y = params["m_y"]
    a = params["a"]
    b = params["b"]
    
    lines = []
    lines.append("RESUMO DA DERIVACAO")
    lines.append("=" * 50)
    lines.append(f"Janela de voo: t ∈ [{t0:.3f}, {t1:.3f}] s (duração: {T:.3f} s)")
    lines.append("")
    lines.append("POSIÇÃO:")
    lines.append(f"  x(t) = {m_x:.6f} * t + {params['q_x']:.6f}")
    lines.append(f"  y(t) = {m_y:.6f} * t + {params['q_y']:.6f}")
    lines.append(f"  z(t) = {a:.6f} * t² + {b:.6f} * t + {params['c']:.6f}")
    lines.append("")
    lines.append("VELOCIDADE:")
    lines.append(f"  vx(t) = {m_x:.6f} m/s")
    lines.append(f"  vy(t) = {m_y:.6f} m/s")
    lines.append(f"  vz(t) = {2*a:.6f} * t + {b:.6f} m/s")
    lines.append("")
    lines.append("ACELERAÇÃO:")
    lines.append("  ax(t) = 0 m/s²")
    lines.append("  ay(t) = 0 m/s²")
    lines.append(f"  az(t) = {2*a:.6f} m/s² (constante = -g)")
    
    return "\n".join(lines)
