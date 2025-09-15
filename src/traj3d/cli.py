"""
módulo cli para orquestração do fluxo principal
"""

import argparse
from pathlib import Path
import cv2
import numpy as np

from .io_cvat import load_cvat_xy
from .detection import detect_launch_frame
from .trajectory import build_trajectory, make_position_functions
from .kinematics import build_kinematics
from .derivation import print_derivation
from .plotting import plot_xyz, plot_velocity_components, plot_acceleration_components
from .video_annot import annotate_video, extract_key_frames
from .utils import parse_triplet


def parse_args():
    # parse dos argumentos da linha de comando
    p = argparse.ArgumentParser(description="trajetória com xy retilíneo e z parabólico entre pontos de referência")
    p.add_argument("--video", required=True, help="caminho do vídeo")
    p.add_argument("--xml", required=True, help="annotations.xml do cvat")
    p.add_argument("--out", default="out", help="pasta de saída")
    p.add_argument("--fps-override", type=float, default=None, help="força fps do vídeo se necessário")
    p.add_argument("--camera", "--anchor-camera", dest="camera", default="7,4,1",
                   help="posição da câmera x,y,z")
    p.add_argument("--bola-inicio", "--anchor-ball-start", dest="ball_start", default="0,7,2.0",
                   help="posição inicial da bola x,y,z")
    p.add_argument("--bola-fim", "--anchor-ball-end", dest="ball_end", default="6,6,0",
                   help="posição final da bola x,y,z")
    p.add_argument("--g", type=float, default=9.81, help="gravidade para z")
    return p.parse_args()


def main():
    # fluxo: ler args -> ler vídeo -> ler cvat -> janela do voo -> série -> derivação -> plotar -> anotar
    args = parse_args()
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    # pontos de referência em 3d
    cam_xyz = np.array(parse_triplet(args.camera), dtype=float)
    p0 = np.array(parse_triplet(args.ball_start), dtype=float)
    p1 = np.array(parse_triplet(args.ball_end), dtype=float)

    # info do vídeo
    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        raise RuntimeError(f"não consegui abrir o vídeo: {args.video}")
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = args.fps_override if args.fps_override else cap.get(cv2.CAP_PROP_FPS)
    fps = 30.0 if not fps or fps <= 0 else fps
    cap.release()

    # pontos 2d anotados
    df_cvat = load_cvat_xy(args.xml)
    mask = ~(df_cvat["x2d"].isna() | df_cvat["y2d"].isna())
    if not mask.any():
        raise RuntimeError("cvat sem pontos válidos")

    # janela do voo: começo e fim
    f0 = max(int(df_cvat.loc[mask, "frame"].iloc[0]),
             detect_launch_frame(df_cvat.loc[mask, ["frame", "y2d"]]))
    f1 = max(f0 + 1, int(df_cvat.loc[mask, "frame"].iloc[-1]))

    # série temporal só com posição
    df_pos = build_trajectory(total, f0, f1, fps, p0, p1, g=args.g)

    # derivação calculada e funções de velocidade
    params = make_position_functions(f0, f1, fps, p0, p1, g=args.g)

    # série com velocidade e aceleração via cálculo diferencial
    df = build_kinematics(df_pos, params)
    df.to_csv(outdir / "series.csv", index=False)

    # derivação textual completa
    print_derivation(params, out_path=outdir / "derivacao_posicao.txt")

    # saídas visuais
    plot_xyz(df, str(outdir / "trajetoria_3d.png"), tuple(cam_xyz), tuple(p0), tuple(p1))
    plot_velocity_components(df, str(outdir / "velocidade_componentes.png"))
    plot_acceleration_components(df, str(outdir / "aceleracao_componentes.png"))
    annotate_video(args.video, df, str(outdir / "bola_annotado.mp4"), fps, df_cvat)
    
    # extrair frames específicos
    frame_files = extract_key_frames(args.video, df, outdir, df_cvat)

    print("ok. saídas principais:")
    print(outdir / "series.csv")
    print(outdir / "derivacao_posicao.txt")
    print(outdir / "trajetoria_3d.png")
    print(outdir / "velocidade_componentes.png")
    print(outdir / "aceleracao_componentes.png")
    print(outdir / "bola_annotado.mp4")
    for frame_file in frame_files:
        print(frame_file)


def run_analysis(video_path, xml_path, output_dir="out", camera_pos="7,4,1", 
                ball_start="0,7,2.0", ball_end="6,6,0", g=9.81, fps_override=None):
    # executa a análise de trajetória programaticamente
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    # pontos de referência em 3d
    cam_xyz = np.array(parse_triplet(camera_pos), dtype=float)
    p0 = np.array(parse_triplet(ball_start), dtype=float)
    p1 = np.array(parse_triplet(ball_end), dtype=float)

    # info do vídeo
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"não consegui abrir o vídeo: {video_path}")
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = fps_override if fps_override else cap.get(cv2.CAP_PROP_FPS)
    fps = 30.0 if not fps or fps <= 0 else fps
    cap.release()

    # pontos 2d anotados
    df_cvat = load_cvat_xy(xml_path)
    mask = ~(df_cvat["x2d"].isna() | df_cvat["y2d"].isna())
    if not mask.any():
        raise RuntimeError("cvat sem pontos válidos")

    # janela do voo: começo e fim
    f0 = max(int(df_cvat.loc[mask, "frame"].iloc[0]),
             detect_launch_frame(df_cvat.loc[mask, ["frame", "y2d"]]))
    f1 = max(f0 + 1, int(df_cvat.loc[mask, "frame"].iloc[-1]))

    # série temporal só com posição
    df_pos = build_trajectory(total, f0, f1, fps, p0, p1, g=g)

    # derivação calculada e funções de velocidade
    params = make_position_functions(f0, f1, fps, p0, p1, g=g)

    # série com velocidade e aceleração via cálculo diferencial
    df = build_kinematics(df_pos, params)
    df.to_csv(outdir / "series.csv", index=False)

    # derivação textual completa
    print_derivation(params, out_path=outdir / "derivacao_posicao.txt")

    # saídas visuais
    plot_xyz(df, str(outdir / "trajetoria_3d.png"), tuple(cam_xyz), tuple(p0), tuple(p1))
    plot_velocity_components(df, str(outdir / "velocidade_componentes.png"))
    plot_acceleration_components(df, str(outdir / "aceleracao_componentes.png"))
    annotate_video(video_path, df, str(outdir / "bola_annotado.mp4"), fps, df_cvat)
    
    # extrair frames específicos
    frame_files = extract_key_frames(video_path, df, outdir, df_cvat)

    return {
        "series_csv": outdir / "series.csv",
        "derivation_txt": outdir / "derivacao_posicao.txt",
        "trajectory_png": outdir / "trajetoria_3d.png",
        "velocity_png": outdir / "velocidade_componentes.png",
        "acceleration_png": outdir / "aceleracao_componentes.png",
        "annotated_video": outdir / "bola_annotado.mp4",
        "key_frames": frame_files,
        "dataframe": df,
        "parameters": params
    }
