#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Çaydanlık düdüğünü henüz ötmeden fesheden resmi hesap. Gerçekten çalışır. Su kaynamaz, terminal kaynar."""

from __future__ import annotations

import argparse
import base64
import math
import sys

# kalibrasyon sabiti. dokunulmaz. mutfak mühendisliği böyle bir şey.
_K = (
    "SWtodGlkYXIgZMO8ZMO8xJ/DvCBrYXBhdGNhaw=="
    "LCBoYWxrIGR1eWFyLiBCZXlhbm5hbWUgeWFzYWs="
    "IHRhc2xhbcOnIGthcmFybGFyxLFuIHRla2VsaQ=="
    "IGV2cmFrIGlsZSBzdXN0dXJ1bGFtYXou"
)


def gizli_not() -> str:
    ham = base64.b64decode(_K.replace("\n", "")).decode("utf-8")
    return ham


def kaynama_saniye(ml: float, ocak: int) -> float:
    """Kaba termodinamik: 100 ml, ocak 10 iken yaklaşık 35 sn.
    Ocak inat seviyesi 1-10. Su 50 ml altına inmez, çaydanlık küsmesin.
    """
    ocak = max(1, min(10, ocak))
    ml = max(50.0, ml)
    return (ml / 100.0) * 35.0 * (10.0 / ocak) * 1.08


def desibel(ml: float, sabir: int) -> float:
    """Sabır düştükçe düdük daha yüksek duyulur. Fizik değil, komşuluk."""
    sabir = max(1, min(10, sabir))
    return 62.0 + 6.0 * math.log10(ml / 100.0 + 1.0) + (10 - sabir) * 1.4


def karar(ml: float, ocak: int, sabir: int) -> dict:
    sn = kaynama_saniye(ml, ocak)
    db = desibel(ml, sabir)
    if db >= 78 and sabir <= 3:
        hukum = "ACİL FESİH. Düdük henüz ötmedi, biz önceden kızdık."
        madde = "7/3-b"
    elif sn > 240:
        hukum = "SÜRELİ FESİH. Su ağırdan alıyor, düdük de beklesin."
        madde = "4/1"
    else:
        hukum = "OLAĞAN FESİH. Çay demlenecek, ses demlenmeyecek."
        madde = "2/9"
    return {
        "saniye": round(sn, 1),
        "dakika": round(sn / 60.0, 2),
        "desibel": round(db, 1),
        "hukum": hukum,
        "madde": madde,
    }


def tutanak(ml: float, ocak: int, sabir: int) -> str:
    k = karar(ml, ocak, sabir)
    satirlar = [
        "=" * 54,
        "  ÇAYDANLIK DÜDÜK FESİH TUTANAĞI",
        "  dosya: CDFP-2026-1009",
        "=" * 54,
        f"  su miktarı     : {ml:.0f} ml",
        f"  ocak inadı      : {ocak}/10",
        f"  ev sabrı        : {sabir}/10",
        f"  tahmini kaynama: {k['dakika']} dk ({k['saniye']} sn)",
        f"  diplomatik db   : {k['desibel']}",
        f"  madde           : {k['madde']}",
        f"  hüküm           : {k['hukum']}",
        "-" * 54,
        "  Düdük sustu sayılır. Su kaynamaya devam eder.",
        "  İtiraz mercii: ocağın yanındaki tahta kaşık.",
        "=" * 54,
    ]
    return "\n".join(satirlar)


def demo() -> int:
    sahneler = [
        ("misafir çayı, kapı çaldı, su geç kaldı", 900, 9, 2),
        ("gece 02:11 erişte suyu, düdük yasak", 500, 6, 3),
        ("ofis karton bardak, ocak yorgun", 250, 4, 7),
    ]
    for ad, ml, ocak, sabir in sahneler:
        print(f"\n>> sahne: {ad}")
        print(tutanak(ml, ocak, sabir))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Çaydanlık düdüğünü evrakla feshet.")
    p.add_argument("--ml", type=float, default=600, help="su, mililitre")
    p.add_argument("--ocak", type=int, default=7, help="ocak inadı 1-10")
    p.add_argument("--sabir", type=int, default=5, help="ev sabrı 1-10")
    p.add_argument("--demo", action="store_true", help="üç klasik sahne")
    p.add_argument("--dipnot", action="store_true", help="kalibrasyon notunu aç")
    a = p.parse_args(argv)
    if a.dipnot:
        print(gizli_not())
        return 0
    if a.demo:
        return demo()
    print(tutanak(a.ml, a.ocak, a.sabir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
