import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import matplotlib.pyplot as plt
import streamlit as st

from plotting import make_diagram
from stages import step_stages
from operating_lines import intersection

st.set_page_config(page_title="McCabe-Thiele", layout="centered")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;700;800&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap');

.stApp, .stApp p, .stApp label { font-family: 'Inter', sans-serif; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 5rem; max-width: 760px; }
header[data-testid="stHeader"] { background: transparent; }

.eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #8F8A7D;
}
.eyebrow .dot { color: #1B7A43; margin-right: 6px; }

.hero {
    font-family: 'Inter Tight', sans-serif;
    font-size: clamp(2.6rem, 7vw, 4.2rem);
    font-weight: 800;
    line-height: 1.02;
    letter-spacing: -0.045em;
    color: #1C1A15;
    margin: 0.7rem 0 1.1rem 0;
}
.hero .muted { color: #8F8A7D; }
.hero .accent { color: #1B7A43; }

.lede {
    font-size: 1.1rem;
    line-height: 1.6;
    color: #4A4740;
    max-width: 600px;
    margin-bottom: 1.4rem;
}

.tags-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #8F8A7D;
    margin-bottom: 0.5rem;
}
.pill {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    padding: 4px 12px;
    margin: 0 6px 8px 0;
    background: #F3F1EA;
    border: 1px solid #E5E2D8;
    border-radius: 8px;
    color: #4A4740;
}

[data-testid="stMetric"] {
    background: #F3F1EA;
    border: 1px solid #E5E2D8;
    border-radius: 12px;
    padding: 14px 18px;
}
[data-testid="stMetricLabel"] p {
    font-family: 'JetBrains Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-size: 0.68rem;
    color: #8F8A7D;
}
[data-testid="stMetricValue"] {
    font-family: 'Inter Tight', sans-serif;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #1C1A15;
}

[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem;
    color: #4A4740;
}
[data-testid="stSliderThumbValue"],
[data-testid="stSliderTickBarMin"],
[data-testid="stSliderTickBarMax"] {
    font-family: 'JetBrains Mono', monospace !important;
}
</style>

<div class="eyebrow"><span class="dot">●</span>Chemical engineering · Separation processes</div>
<div class="hero">McCabe-Thiele<span class="accent">.</span><br><span class="muted">Distillation, stage</span><br>by stage.</div>
<div class="lede">Binary distillation with constant relative volatility. Move the sliders in the sidebar and the diagram, stage count, and feed stage update.</div>
<div class="tags-label">Built with</div>
<div><span class="pill">Python</span><span class="pill">NumPy</span><span class="pill">Matplotlib</span><span class="pill">Streamlit</span><span class="pill">pytest</span></div>
<br>
""",
    unsafe_allow_html=True,
)

st.sidebar.markdown('<div class="eyebrow">Column inputs</div>', unsafe_allow_html=True)
alpha = st.sidebar.slider("Relative volatility (alpha)", 1.05, 10.0, 2.5, 0.05)
R = st.sidebar.slider("Reflux ratio (R)", 0.1, 10.0, 2.0, 0.1)
xD = st.sidebar.slider("Distillate composition (xD)", 0.50, 0.99, 0.90, 0.01)
xF = st.sidebar.slider("Feed composition (xF)", 0.05, 0.95, 0.60, 0.01)
xB = st.sidebar.slider("Bottoms composition (xB)", 0.01, 0.50, 0.10, 0.01)
q = round(st.sidebar.slider("Feed condition (q)", -0.5, 2.0, 1.0, 0.05), 2)

try:
    n, feed_stage, _ = step_stages(alpha, R, xD, q, xF, xB)
    xi, yi = intersection(R, xD, q, xF)

    c1, c2, c3 = st.columns(3)
    c1.metric("Theoretical stages", n)
    c2.metric("Feed stage", feed_stage)
    c3.metric("Line intersection", f"({xi:.2f}, {yi:.2f})")

    fig = make_diagram(alpha, R, xD, q, xF, xB)
    st.pyplot(fig)
    plt.close(fig)
except ValueError as e:
    st.error(str(e))