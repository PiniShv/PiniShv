#!/usr/bin/env python3
"""Build the profile hero banner in a dark and a light version.

Run from the repo root:  python3 assets/hero.py
It writes assets/hero-dark.svg and assets/hero-light.svg.
Colours and type follow pinishv.com: navy, emerald, a block cursor, mono labels.
"""
from pathlib import Path

W, H = 1200, 460
X = 104  # left edge of the text column

SANS = 'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif'
MONO = 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace'

LABEL = "PINI SHVARTSMAN — AI TRANSFORMATION &amp; AUTONOMOUS ENGINEERING"
LINE1 = "The agent writes the code."
LINE2A, LINE2B = "The engineer ", "owns the outcome"
SUB = "I lead AI transformation for a global SaaS platform: 100+ engineers, AI agents in production."

# Widths measured with the macOS system font. textLength pins them, so the
# cursor lands in the same place whatever font the viewer's system picks.
L1_LEN, L2_LEN = 772, 936

# The thesis: execution is cheap; the other five stay with humans.
STAGES = ["INTENT", "CONTEXT", "EXECUTION", "VERIFICATION", "JUDGMENT", "CONTROL"]
AGENT_STAGE = "EXECUTION"
CHIP_CHAR, CHIP_PAD, CHIP_GAP, CHIP_H, CHIP_Y = 9.2, 30, 26, 34, 380
PULSE_S = 7.0  # seconds for one pass of the signal along the strip

THEMES = {
    "dark": dict(
        bg0="#0D1B2A", bg1="#071220", border="#23364D", text="#EEF2F7", muted="#8FA0B3",
        accent="#34D399", label="#34D399", cursor="#34D399", glow="#10B981", glow_op=0.20,
        dot="#8FA0B3", dot_op=0.20, rail="#23364D", chip_bg="#0B1826", chip_line="#2B4260",
        chip_text="#8FA0B3", exec_fill="#34D399", exec_text="#071220", ping_agent="#A7F3D0",
    ),
    "light": dict(
        bg0="#FFFFFF", bg1="#EEF2F7", border="#DFE6EE", text="#0D1B2A", muted="#45566B",
        accent="#059669", label="#047857", cursor="#10B981", glow="#34D399", glow_op=0.22,
        dot="#64748B", dot_op=0.22, rail="#C7D1DD", chip_bg="#FFFFFF", chip_line="#C7D1DD",
        chip_text="#45566B", exec_fill="#10B981", exec_text="#FFFFFF", ping_agent="#6EE7B7",
    ),
}


def chips():
    out, x = [], X
    for name in STAGES:
        w = round(len(name) * CHIP_CHAR + CHIP_PAD)
        out.append((name, x, w))
        x += w + CHIP_GAP
    return out


def build(t):
    cs = chips()
    first_cx = cs[0][1] + cs[0][2] / 2
    last_cx = cs[-1][1] + cs[-1][2] / 2
    line_y = CHIP_Y + CHIP_H / 2
    travel = 0.86  # share of the cycle the pulse spends moving

    chip_svg = []
    for i, (name, x, w) in enumerate(cs):
        cx = x + w / 2
        delay = PULSE_S * travel * (cx - first_cx) / (last_cx - first_cx)
        agent = name == AGENT_STAGE
        cls = "chip agent" if agent else "chip"
        d = f'style="animation-delay:{delay:.2f}s"'
        chip_svg.append(
            f'<g class="{cls}"><rect {d} x="{x}" y="{CHIP_Y}" width="{w}" height="{CHIP_H}" rx="6"/>'
            f'<text {d} x="{cx:.1f}" y="{CHIP_Y + 22}" text-anchor="middle">{name}</text></g>'
        )

    legend_x = cs[-1][1] + cs[-1][2] + 40
    rail_nodes = [92, 168, 248, 320, 397]

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Pini Shvartsman. The agent writes the code. The engineer owns the outcome.">
<title>Pini Shvartsman: the agent writes the code, the engineer owns the outcome</title>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t["bg0"]}"/><stop offset="1" stop-color="{t["bg1"]}"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.82" cy="0.18" r="0.6">
    <stop offset="0" stop-color="{t["glow"]}" stop-opacity="{t["glow_op"]}"/>
    <stop offset="1" stop-color="{t["glow"]}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="fade" cx="0.7" cy="0.35" r="0.75">
    <stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <mask id="gridmask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.1" fill="{t["dot"]}" fill-opacity="{t["dot_op"]}"/>
  </pattern>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="20"/></clipPath>
</defs>
<style>
  .label {{ font: 600 15px {MONO}; letter-spacing: 2.4px; fill: {t["label"]}; }}
  .h {{ font: 700 64px {SANS}; letter-spacing: -1.2px; fill: {t["text"]}; }}
  .h .em {{ fill: {t["accent"]}; }}
  .sub {{ font: 400 21px {SANS}; fill: {t["muted"]}; }}
  .legend {{ font: 500 12px {MONO}; letter-spacing: 1.2px; fill: {t["muted"]}; }}
  .chip rect {{ fill: {t["chip_bg"]}; stroke: {t["chip_line"]}; stroke-width: 1.2; }}
  .chip text {{ font: 600 13px {MONO}; letter-spacing: 1.4px; fill: {t["chip_text"]}; }}
  .chip.agent rect {{ fill: {t["exec_fill"]}; stroke: {t["exec_fill"]}; }}
  .chip.agent text {{ fill: {t["exec_text"]}; }}
  .chip rect {{ animation: ping-box {PULSE_S}s ease-out infinite; }}
  .chip text {{ animation: ping-text {PULSE_S}s ease-out infinite; }}
  .chip.agent rect {{ animation-name: ping-agent; }}
  .chip.agent text {{ animation: none; }}
  @keyframes ping-box {{ 0% {{ stroke: {t["cursor"]}; }} 12%, 100% {{ stroke: {t["chip_line"]}; }} }}
  @keyframes ping-text {{ 0% {{ fill: {t["label"]}; }} 12%, 100% {{ fill: {t["chip_text"]}; }} }}
  @keyframes ping-agent {{ 0% {{ fill: {t["ping_agent"]}; stroke: {t["ping_agent"]}; }} 12%, 100% {{ fill: {t["exec_fill"]}; stroke: {t["exec_fill"]}; }} }}
  .cursor {{ fill: {t["cursor"]}; animation: blink 2.6s ease-in-out infinite; }}
  @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.35; }} }}
  .pulse {{ fill: {t["cursor"]}; animation: travel {PULSE_S}s linear infinite; }}
  @keyframes travel {{
    0% {{ transform: translateX(0); opacity: 0; }}
    4% {{ opacity: 1; }}
    {travel * 100:.0f}% {{ transform: translateX({last_cx - first_cx:.1f}px); opacity: 1; }}
    {travel * 100 + 6:.0f}%, 100% {{ transform: translateX({last_cx - first_cx:.1f}px); opacity: 0; }}
  }}
  .node {{ fill: {t["rail"]}; }}
  .node.on {{ fill: {t["cursor"]}; }}
  @media (prefers-reduced-motion: reduce) {{
    .chip rect, .chip text, .cursor {{ animation: none; }}
    .pulse {{ animation: none; opacity: 0; }}
  }}
</style>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#gridmask)"/>
  <rect width="{W}" height="{H}" fill="url(#glow)"/>
</g>
<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="19.5" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>

<line x1="62" y1="{rail_nodes[0]}" x2="62" y2="{rail_nodes[-1]}" stroke="{t["rail"]}" stroke-width="1.5"/>
{"".join(f'<rect class="node{" on" if i == 1 else ""}" x="58" y="{y - 4}" width="8" height="8" rx="1.5"/>' for i, y in enumerate(rail_nodes))}

<g>
  <rect x="{X}" y="81" width="10" height="10" rx="2" fill="{t["cursor"]}"/>
  <text class="label" x="{X + 22}" y="91">{LABEL}</text>
</g>
<text class="h" x="{X - 3}" y="182" textLength="{L1_LEN}" lengthAdjust="spacing">{LINE1}</text>
<g>
  <text class="h" x="{X - 3}" y="262" textLength="{L2_LEN}" lengthAdjust="spacing" xml:space="preserve">{LINE2A}<tspan class="em">{LINE2B}</tspan></text>
  <rect class="cursor" x="{X - 3 + L2_LEN + 12}" y="212" width="26" height="54" rx="3"/>
</g>
<text class="sub" x="{X}" y="322">{SUB}</text>

<g>
  <line x1="{first_cx:.1f}" y1="{line_y}" x2="{last_cx:.1f}" y2="{line_y}" stroke="{t["chip_line"]}" stroke-width="1.5" stroke-dasharray="3 5"/>
  <circle class="pulse" cx="{first_cx:.1f}" cy="{line_y}" r="4"/>
  {"".join(chip_svg)}
  <rect x="{legend_x}" y="{CHIP_Y + 3}" width="10" height="10" rx="2" fill="{t["exec_fill"]}"/>
  <text class="legend" x="{legend_x + 18}" y="{CHIP_Y + 12}">AGENTS RUN IT</text>
  <rect x="{legend_x + 0.6}" y="{CHIP_Y + 21.6}" width="8.8" height="8.8" rx="2" fill="none" stroke="{t["chip_line"]}" stroke-width="1.2"/>
  <text class="legend" x="{legend_x + 18}" y="{CHIP_Y + 31}">HUMANS OWN IT</text>
</g>
</svg>
'''


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    for name, theme in THEMES.items():
        (here / f"hero-{name}.svg").write_text(build(theme), encoding="utf-8")
        print(f"wrote assets/hero-{name}.svg")
