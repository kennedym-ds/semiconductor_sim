"""Minimal CLI to run quick semiconductor_sim demos for learners.

Usage:
    semisim demo pn
    semisim demo led

This avoids any heavy dependencies and prints a short numeric summary.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence

import numpy as np

from . import LED, PNJunctionDiode


def demo_pn() -> None:
    voltage = np.linspace(-0.2, 0.7, 10)
    d = PNJunctionDiode(doping_p=1e17, doping_n=1e17)
    current, recomb = d.iv_characteristic(voltage, n_conc=1e16, p_conc=1e16)
    print("PN Junction demo")
    print("V [V]    I [A]       R_SRH [cm^-3 s^-1]")
    for v, i, r in zip(voltage, current, recomb, strict=False):
        print(f"{v: .3f}  {i: .3e}  {r: .3e}")


def demo_led() -> None:
    voltage = np.linspace(0.0, 2.0, 10)
    d = LED(doping_p=1e17, doping_n=1e17)
    current, emission = d.iv_characteristic(voltage)
    print("LED demo")
    print("V [V]    I [A]       Emission [arb]")
    for v, i, e in zip(voltage, current, emission, strict=False):
        print(f"{v: .3f}  {i: .3e}  {e: .3e}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="semisim", description="SemiconductorSim CLI demos")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo", help="Run a quick device demo")
    demo.add_argument("device", choices=["pn", "led"], help="Which device demo to run")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "demo":
        if args.device == "pn":
            demo_pn()
        elif args.device == "led":
            demo_led()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
