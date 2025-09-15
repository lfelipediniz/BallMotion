"""
módulo para anotação de vídeo e utilidades de desenho
"""

import cv2
import numpy as np


def annotate_video(video_path, df, out_path, fps, df_cvat=None):
    # anota no vídeo o frame, tempo, posição 3d, módulo da velocidade, módulo da aceleração e o ponto 2d do cvat
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"não consegui abrir o vídeo: {video_path}")

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    writer = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    if not writer.isOpened():
        raise RuntimeError("falha ao abrir VideoWriter")

    x = df["x3d"].to_numpy()
    y = df["y3d"].to_numpy()
    z = df["z3d"].to_numpy()
    spd = df["speed"].to_numpy() if "speed" in df.columns else None
    ax = df["ax"].to_numpy() if "ax" in df.columns else None
    ay = df["ay"].to_numpy() if "ay" in df.columns else None
    az = df["az"].to_numpy() if "az" in df.columns else None
    by_frame_cvat = {int(r.frame): r for r in df_cvat.itertuples(index=False)} if df_cvat is not None else {}

    for idx in range(total):
        ok, frame = cap.read()
        if not ok:
            break

        if idx < len(x) and not (np.isnan(x[idx]) or np.isnan(y[idx]) or np.isnan(z[idx])):
            # Desenhar informações de posição e tempo
            draw_position_info(frame, idx, fps, x[idx], y[idx], z[idx])
            
            # Desenhar velocidade se disponível
            if spd is not None and idx < len(spd) and np.isfinite(spd[idx]):
                draw_velocity_info(frame, spd[idx])
            
            # Desenhar aceleração se disponível
            if (ax is not None and ay is not None and az is not None and 
                idx < len(ax) and np.isfinite(ax[idx]) and np.isfinite(ay[idx]) and np.isfinite(az[idx])):
                a_mod = np.sqrt(ax[idx]**2 + ay[idx]**2 + az[idx]**2)
                draw_acceleration_info(frame, a_mod)

        # Desenhar ponto 2D do CVAT
        r2 = by_frame_cvat.get(idx)
        if r2 is not None and not (np.isnan(r2.x2d) or np.isnan(r2.y2d)):
            draw_cvat_point(frame, r2.x2d, r2.y2d)

        writer.write(frame)

    cap.release()
    writer.release()


def draw_position_info(frame, frame_idx, fps, x, y, z):
    # desenha informações de posição e tempo no frame
    txt1 = f"frame {frame_idx}  t {frame_idx/fps:0.3f}s"
    txt2 = f"x {x:0.3f}  y {y:0.3f}  z {z:0.3f}"
    
    # Desenhar com contorno preto e texto branco para melhor legibilidade
    cv2.putText(frame, txt1, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3)
    cv2.putText(frame, txt1, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, txt2, (15, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3)
    cv2.putText(frame, txt2, (15, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


def draw_velocity_info(frame, speed):
    # desenha informações de velocidade no frame
    txt3 = f"|v| {speed:0.3f} m/s"
    cv2.putText(frame, txt3, (15, 74), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3)
    cv2.putText(frame, txt3, (15, 74), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


def draw_acceleration_info(frame, a_mod):
    # desenha informações de aceleração no frame
    txt4 = f"|a| {a_mod:0.3f} m/s^2"
    cv2.putText(frame, txt4, (15, 96), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3)
    cv2.putText(frame, txt4, (15, 96), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


def draw_cvat_point(frame, x2d, y2d):
    # desenha o ponto 2d do cvat no frame
    p = (int(x2d), int(y2d))
    cv2.circle(frame, p, 8, (0, 255, 0), 2)
    cv2.putText(frame, "Bola", (p[0] + 12, p[1] - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


def draw_trajectory_trail(frame, trajectory_points, color=(255, 0, 0), thickness=2):
    # desenha uma trilha da trajetória no frame
    if len(trajectory_points) < 2:
        return
    
    for i in range(1, len(trajectory_points)):
        pt1 = (int(trajectory_points[i-1][0]), int(trajectory_points[i-1][1]))
        pt2 = (int(trajectory_points[i][0]), int(trajectory_points[i][1]))
        cv2.line(frame, pt1, pt2, color, thickness)


def draw_velocity_vector(frame, x2d, y2d, vx, vy, scale=10, color=(0, 255, 255)):
    # desenha um vetor de velocidade no frame
    start_point = (int(x2d), int(y2d))
    end_point = (int(x2d + vx * scale), int(y2d + vy * scale))
    
    cv2.arrowedLine(frame, start_point, end_point, color, 2, tipLength=0.3)


def create_info_panel(frame, info_dict, position=(10, 10)):
    # cria um painel de informações no frame
    x, y = position
    line_height = 25
    
    for i, (key, value) in enumerate(info_dict.items()):
        text = f"{key}: {value}"
        cv2.putText(frame, text, (x, y + i * line_height), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


def extract_key_frames(video_path, df, output_dir, df_cvat=None):
    # extrai 3 frames específicos: primeiro, meio e último frame do vídeo anotado
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"não consegui abrir o vídeo: {video_path}")

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Calcular frames específicos
    first_frame = 0
    middle_frame = total // 2
    last_frame = total - 1
    
    frames_to_extract = [
        (first_frame, "primeiro_frame.png"),
        (middle_frame, "frame_meio.png"), 
        (last_frame, "ultimo_frame.png")
    ]
    
    # Preparar dados para anotação
    x = df["x3d"].to_numpy()
    y = df["y3d"].to_numpy()
    z = df["z3d"].to_numpy()
    spd = df["speed"].to_numpy() if "speed" in df.columns else None
    ax = df["ax"].to_numpy() if "ax" in df.columns else None
    ay = df["ay"].to_numpy() if "ay" in df.columns else None
    az = df["az"].to_numpy() if "az" in df.columns else None
    by_frame_cvat = {int(r.frame): r for r in df_cvat.itertuples(index=False)} if df_cvat is not None else {}
    
    extracted_files = []
    
    for frame_idx, filename in frames_to_extract:
        # Ir para o frame específico
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ok, frame = cap.read()
        
        if not ok:
            print(f"Aviso: não foi possível ler o frame {frame_idx}")
            continue
            
        # Anotar o frame se houver dados válidos
        if frame_idx < len(x) and not (np.isnan(x[frame_idx]) or np.isnan(y[frame_idx]) or np.isnan(z[frame_idx])):
            # Desenhar informações de posição e tempo
            draw_position_info(frame, frame_idx, fps, x[frame_idx], y[frame_idx], z[frame_idx])
            
            # Desenhar velocidade se disponível
            if spd is not None and frame_idx < len(spd) and np.isfinite(spd[frame_idx]):
                draw_velocity_info(frame, spd[frame_idx])
            
            # Desenhar aceleração se disponível
            if (ax is not None and ay is not None and az is not None and 
                frame_idx < len(ax) and np.isfinite(ax[frame_idx]) and np.isfinite(ay[frame_idx]) and np.isfinite(az[frame_idx])):
                a_mod = np.sqrt(ax[frame_idx]**2 + ay[frame_idx]**2 + az[frame_idx]**2)
                draw_acceleration_info(frame, a_mod)

        # Desenhar ponto 2D do CVAT
        r2 = by_frame_cvat.get(frame_idx)
        if r2 is not None and not (np.isnan(r2.x2d) or np.isnan(r2.y2d)):
            draw_cvat_point(frame, r2.x2d, r2.y2d)
        
        # Salvar o frame
        output_path = output_dir / filename
        cv2.imwrite(str(output_path), frame)
        extracted_files.append(output_path)
        print(f"Frame {frame_idx} salvo como: {output_path}")
    
    cap.release()
    return extracted_files
