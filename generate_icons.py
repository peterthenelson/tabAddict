#!/usr/bin/env python3
"""Generates all three TabAddict icons: icon_launch.svg, icon_open.svg, icon_capture.svg."""

import math


# ── Rocket helpers ────────────────────────────────────────────────────────────

def lune_path(x1, y1, R, x2, y2, r):
    """SVG path 'd' for the lune = inside circle A(x1,y1,R) and outside circle B(x2,y2,r)."""
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)

    if d >= R + r:
        return _circle(x1, y1, R)
    if d <= abs(R - r):
        if r < R:
            return _circle(x1, y1, R) + " " + _circle(x2, y2, r, reverse=True)
        return ""

    a = (R * R - r * r + d * d) / (2 * d)
    h = math.sqrt(max(0.0, R * R - a * a))
    mx, my = x1 + a * dx / d, y1 + a * dy / d
    ox, oy = -dy / d * h, dx / d * h
    p1 = (mx + ox, my + oy)
    p2 = (mx - ox, my - oy)

    arc_a = _arc(x1, y1, R, p1, p2, lambda px, py: math.hypot(px - x2, py - y2) > r)
    arc_b = _arc(x2, y2, r, p2, p1, lambda px, py: math.hypot(px - x1, py - y1) < R)
    return f"M {p1[0]:.2f} {p1[1]:.2f} {arc_a} {arc_b} Z"

def _arc(cx, cy, rad, start, end, test):
    a0 = math.atan2(start[1] - cy, start[0] - cx)
    a1 = math.atan2(end[1] - cy, end[0] - cx)
    inc = a1 - a0
    while inc <= 0:
        inc += 2 * math.pi
    mid = a0 + inc / 2
    use_inc = test(cx + rad * math.cos(mid), cy + rad * math.sin(mid))
    sweep = 1 if use_inc else 0
    swept = inc if use_inc else 2 * math.pi - inc
    large = 1 if swept > math.pi else 0
    return f"A {rad:.2f} {rad:.2f} 0 {large} {sweep} {end[0]:.2f} {end[1]:.2f}"

def _circle(cx, cy, rad, reverse=False):
    s = 0 if reverse else 1
    return (f"M {cx-rad:.2f} {cy:.2f} a {rad} {rad} 0 1 {s} {2*rad} 0 "
            f"a {rad} {rad} 0 1 {s} {-2*rad} 0 Z")

def crescent(cx, cy, R, thickness, curvature=1.0, angle_deg=0.0):
    """Symmetric crescent: lune of two circles.

    R          outer radius
    thickness  waist depth as fraction of R (0.1=sliver, 1.0=fat)
    curvature  inner radius ratio r/R (1.0=lens; >1 flatter bite; <1 bulgier)
    angle_deg  direction the bite is aimed (SVG coords: 270=up toward nose)
    """
    r = curvature * R
    D = thickness * R + r - R
    t = math.radians(angle_deg)
    return lune_path(cx, cy, R, cx + D * math.cos(t), cy + D * math.sin(t), r)


# ── Output helper ─────────────────────────────────────────────────────────────

def _write(filename, content):
    with open(filename, "w") as f:
        f.write(content)
    print(f"Wrote {filename}")


def main():
    VIEWBOX  = 100
    BG       = "#C7D2FE"
    FG       = "#1E1B4B"
    RECT_RX  = 12

    # ── icon_launch.svg (rocket) ──────────────────────────────────────────────

    BW        = 9    # body half-width at shoulder (widest point)
    BW_BOT    = 7    # body half-width at base (after taper)

    CROSS_FRAC = 0.01  # crossbar top as fraction of BODY_H from body_top
    CROSS_H    = 5     # crossbar height
    CROSS_ARC  = 5     # how many px the edges arc upward at centre
    CROSS_W    = BW + 1  # crossbar half-width (slightly wider than body to cover edges)

    FIN_H     = 8     # fin section height (used in ROCKET_H centering)
    FIN_R     = 22    # crescent outer radius
    FIN_THICK = 0.5   # waist thickness as fraction of R (0=sliver, 1=fat)
    FIN_CURVE = 1.6   # inner radius ratio r/R (1=lens, >1 flatter bite)
    FIN_ANGLE = 90    # bite direction in degrees (90=downward in SVG = toward tail)

    ANGLE_DEG = 40    # icon rotation clockwise (tilts rocket up-right)

    BODY_H    = 22    # body height
    NOSE_H    = 27
    EX_H      = 30
    EX_W      = 5    # exhaust half-width at base (narrower than body)

    # Full rocket height: nose(27) + body(22) + fin(8) + exhaust(30) = 87
    # Centre at y=50  =>  nose tip at y = 50 - 87/2 = 6.5
    ROCKET_H  = NOSE_H + BODY_H + FIN_H + EX_H

    cx        = VIEWBOX / 2
    top_y     = (VIEWBOX - ROCKET_H) / 2

    nose_tip  = top_y
    body_top  = top_y + NOSE_H
    body_bot  = body_top + BODY_H

    # Both the nose and body use quadratic Beziers whose control points share
    # x = cx+BW (the shoulder x).  This forces a VERTICAL tangent at the shoulder
    # on both sides of the join, giving C1 continuity and no visible corner.
    NOSE_QY   = nose_tip + NOSE_H * 0.72   # closer to body_top = sharper tip
    BODY_QY   = body_top + BODY_H * 0.50   # midway through body

    cross_top = body_top + CROSS_FRAC * BODY_H
    cross_bot = cross_top + CROSS_H

    fin_bot   = body_bot + FIN_H
    ex_tip    = fin_bot + EX_H
    fin_cy    = (body_bot + ex_tip) / 2    # crescent centre: halfway down exhaust

    path_d = " ".join([
        f"M {cx:.2f},{nose_tip:.2f}",
        f"Q {cx+BW:.2f},{NOSE_QY:.2f} {cx+BW:.2f},{body_top:.2f}",
        f"Q {cx+BW:.2f},{BODY_QY:.2f} {cx+BW_BOT:.2f},{body_bot:.2f}",
        f"L {cx-BW_BOT:.2f},{body_bot:.2f}",
        f"Q {cx-BW:.2f},{BODY_QY:.2f} {cx-BW:.2f},{body_top:.2f}",
        f"Q {cx-BW:.2f},{NOSE_QY:.2f} {cx:.2f},{nose_tip:.2f}",
        "Z",
    ])

    cross_d = (
        f'M {cx-CROSS_W:.2f},{cross_top:.2f} '
        f'Q {cx:.2f},{cross_top-CROSS_ARC:.2f} {cx+CROSS_W:.2f},{cross_top:.2f} '
        f'L {cx+CROSS_W:.2f},{cross_bot:.2f} '
        f'Q {cx:.2f},{cross_bot-CROSS_ARC:.2f} {cx-CROSS_W:.2f},{cross_bot:.2f} '
        f'Z'
    )

    rocket_shapes = [
        f'<path d="{path_d}" fill="{FG}"/>',
        f'<path d="{cross_d}" fill="{BG}"/>',
        f'<polygon points="{cx-EX_W:.2f},{body_bot:.2f} {cx+EX_W:.2f},{body_bot:.2f} {cx:.2f},{ex_tip:.2f}" fill="{FG}"/>',
        f'<path d="{crescent(cx, fin_cy, FIN_R, FIN_THICK, FIN_CURVE, FIN_ANGLE)}" fill="{FG}"/>',
    ]

    inner = "\n    ".join(rocket_shapes)
    _write("icon_launch.svg", (
        f'<svg viewBox="0 0 {VIEWBOX} {VIEWBOX}" xmlns="http://www.w3.org/2000/svg">\n'
        f'  <rect width="{VIEWBOX}" height="{VIEWBOX}" rx="{RECT_RX}" fill="{BG}"/>\n'
        f'  <g transform="rotate({ANGLE_DEG}, {cx}, {cx})">\n'
        f'    {inner}\n'
        f'  </g>\n'
        f'</svg>\n'
    ))

    # ── icon_open.svg (folder) ────────────────────────────────────────────────
    # Body:  BL=12 BR=88 BT=32 BB=80  r=8
    # Tab:   left=12, top at y=20, top-right corner at (42,20),
    #        bottom-right at (49,32) — right side angled 60° from horizontal
    #        (12px drop × 1/tan60° ≈ 7px rightward shift)
    # Corner geometry: 90° top-left (tr=5), 120° top-right (tr=5), 120° concave (ic=4)
    # Arc setback for 120° corners: r/tan(60°) ≈ 0.577r
    #   top-right tangents: (39.1,20) and (43.5,22.5)
    #   concave tangents:   (47.8,30.0) and (51.3,32)
    folder_d = (
        "M 12,25 "
        "A 5 5 0 0 1 17,20 "       # top-left tab corner (90°)
        "L 39.1,20 "               # tab top
        "A 5 5 0 0 1 43.5,22.5 "  # top-right tab corner (120° interior)
        "L 47.8,30.0 "             # angled right side
        "A 4 4 0 0 0 51.3,32 "    # concave inner corner (120°)
        "L 80,32 "
        "A 8 8 0 0 1 88,40 "
        "L 88,72 "
        "A 8 8 0 0 1 80,80 "
        "L 20,80 "
        "A 8 8 0 0 1 12,72 "
        "Z"
    )

    _write("icon_open.svg", (
        f'<svg viewBox="0 0 {VIEWBOX} {VIEWBOX}" xmlns="http://www.w3.org/2000/svg">\n'
        f'  <rect width="{VIEWBOX}" height="{VIEWBOX}" rx="{RECT_RX}" fill="{BG}"/>\n'
        f'  <path d="{folder_d}" fill="{FG}"/>\n'
        f'</svg>\n'
    ))

    # ── icon_capture.svg (camera) ─────────────────────────────────────────────
    # Body:  BL=12 BR=88 BT=32 BB=80  r=8
    # Bump:  bottom (33,32)–(67,32), top (40,20)–(60,20)
    #        both sides angled 60° from horizontal (7px shift per 12px drop)
    # Lens:  cx=50 cy=56  outer r=19 (BG annulus), inner r=11 (FG dot)
    # Arc setback for 120° corners: r/tan(60°) ≈ 0.577r
    #   top-left tangents:   (38.5,22.5) and (42.9,20)
    #   top-right tangents:  (57.1,20) and (61.5,22.5)
    #   right concave:       (65.8,30.0) and (69.3,32)
    #   left concave:        (30.7,32) and (34.2,30.0)
    # Path starts on left angled side at top-left setback; Z closes left angled side.
    camera_d = (
        "M 38.5,22.5 "
        "A 5 5 0 0 1 42.9,20 "    # top-left bump corner (120° interior)
        "L 57.1,20 "               # bump top
        "A 5 5 0 0 1 61.5,22.5 "  # top-right bump corner (120° interior)
        "L 65.8,30.0 "             # angled right side
        "A 4 4 0 0 0 69.3,32 "    # right concave corner (120°)
        "L 80,32 "
        "A 8 8 0 0 1 88,40 "
        "L 88,72 "
        "A 8 8 0 0 1 80,80 "
        "L 20,80 "
        "A 8 8 0 0 1 12,72 "
        "L 12,40 "
        "A 8 8 0 0 1 20,32 "
        "L 30.7,32 "               # body top left
        "A 4 4 0 0 0 34.2,30.0 "  # left concave corner (120°)
        "Z"                        # angled left side back to start
    )

    _write("icon_capture.svg", (
        f'<svg viewBox="0 0 {VIEWBOX} {VIEWBOX}" xmlns="http://www.w3.org/2000/svg">\n'
        f'  <rect width="{VIEWBOX}" height="{VIEWBOX}" rx="{RECT_RX}" fill="{BG}"/>\n'
        f'  <path d="{camera_d}" fill="{FG}"/>\n'
        f'  <circle cx="50" cy="56" r="19" fill="{BG}"/>\n'
        f'  <circle cx="50" cy="56" r="11" fill="{FG}"/>\n'
        f'</svg>\n'
    ))


if __name__ == "__main__":
    main()
