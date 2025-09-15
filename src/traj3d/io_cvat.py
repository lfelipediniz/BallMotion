"""
módulo para leitura de anotações do cvat
"""

import pandas as pd
from lxml import etree


def load_cvat_xy(xml_path):
    # lê o xml do cvat e extrai o centro do bbox em cada frame como (x2d, y2d)
    root = etree.parse(xml_path).getroot()
    track = root.find(".//track")
    if track is None:
        raise RuntimeError("não achei track no annotations.xml")
    
    rows = []
    for sh in track:
        # consideramos shapes tipo box e pegamos o centro como média dos cantos
        if sh.tag.lower().endswith("box") and sh.get("frame"):
            f = int(sh.get("frame"))
            xtl = float(sh.get("xtl", 0))
            ytl = float(sh.get("ytl", 0))
            xbr = float(sh.get("xbr", 0))
            ybr = float(sh.get("ybr", 0))
            rows.append({
                "frame": f, 
                "x2d": 0.5 * (xtl + xbr), 
                "y2d": 0.5 * (ytl + ybr)
            })
    
    if not rows:
        raise RuntimeError("não encontrei shapes com box")
    
    return pd.DataFrame(rows).sort_values("frame").reset_index(drop=True)
