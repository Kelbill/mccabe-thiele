import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import matplotlib.pyplot as plt
import streamlit as st

from plotting import make_diagram
from stages import step_stages
from operating_lines import intersection

st.set_page_config(page_title="McCabe-Thiele", layout="centered")

THEMES = {
    "light": {
        "BG": "#FBFAF6",
        "SURF": "#F3F1EA",
        "BORDER": "#E5E2D8",
        "INK": "#1C1A15",
        "MUTED": "#8F8A7D",
        "SOFT": "#4A4740",
        "RED": "#E5484D",
    },
    "dark": {
        "BG": "#211F1A",
        "SURF": "#2A2721",
        "BORDER": "#3A362D",
        "INK": "#F2EFE6",
        "MUTED": "#8F8A7D",
        "SOFT": "#B9B4A7",
        "RED": "#E5484D",
    },
}

dark = st.sidebar.toggle("Dark mode", value=False)
theme = THEMES["dark" if dark else "light"]

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;500;700&display=swap');

.stApp {
    background-color: __BG__;
    font-family: 'Oswald', sans-serif;
}
.stApp p, .stApp label { font-family: 'Oswald', sans-serif; }

/* keep Streamlit's icons on their own font */
[data-testid="stIconMaterial"],
span.material-icons,
span[class*="material-symbols"] {
    font-family: 'Material Symbols Rounded' !important;
}

#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 5rem; max-width: 760px; }
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background-color: __SURF__; }

.eyebrow {
    font-family: 'Oswald', sans-serif;
    font-weight: 400;
    font-size: 0.8rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: __MUTED__;
}
.eyebrow .dot { color: __RED__; margin-right: 8px; }

.hero {
    font-family: 'Oswald', sans-serif;
    font-size: clamp(2.8rem, 8vw, 4.6rem);
    font-weight: 700;
    line-height: 1.0;
    letter-spacing: 0.01em;
    text-transform: uppercase;
    color: __INK__;
    margin: 0.7rem 0 1.1rem 0;
}
.hero .muted { color: __MUTED__; }
.hero .accent { color: __RED__; }

.lede {
    font-family: 'Oswald', sans-serif;
    font-size: 1.1rem;
    font-weight: 300;
    line-height: 1.6;
    letter-spacing: 0.02em;
    color: __SOFT__;
    max-width: 600px;
    margin-bottom: 1.4rem;
}

.tags-label {
    font-family: 'Oswald', sans-serif;
    font-size: 0.78rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: __MUTED__;
    margin-bottom: 0.5rem;
}
.pill {
    display: inline-block;
    font-family: 'Oswald', sans-serif;
    font-size: 0.85rem;
    letter-spacing: 0.06em;
    padding: 3px 14px;
    margin: 0 6px 8px 0;
    background: __SURF__;
    border: 1px solid __BORDER__;
    border-radius: 8px;
    color: __SOFT__;
}

.chart-title {
    font-family: 'Oswald', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    color: __INK__;
    margin: 1.4rem 0 0.2rem 0;
}
.chart-title .muted { color: __MUTED__; }

[data-testid="stMetric"] {
    background: __SURF__;
    border: 1px solid __BORDER__;
    border-radius: 12px;
    padding: 14px 18px;
}
[data-testid="stMetricLabel"] p {
    font-family: 'Oswald', sans-serif;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-size: 0.75rem;
    color: __MUTED__;
}
[data-testid="stMetricValue"] {
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    letter-spacing: 0.01em;
    color: __INK__;
}

[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] label p {
    font-family: 'Oswald', sans-serif !important;
    font-size: 0.95rem;
    letter-spacing: 0.04em;
    color: __SOFT__;
}
[data-testid="stSliderThumbValue"],
[data-testid="stSliderTickBarMin"],
[data-testid="stSliderTickBarMax"] {
    font-family: 'Oswald', sans-serif !important;
    color: __SOFT__;
}
[data-testid="stSlider"] [role="slider"] { background-color: __RED__ !important; }
[data-testid="stSliderThumbValue"] { color: __RED__ !important; }
</style>
"""

for key, value in theme.items():
    CSS = CSS.replace(f"__{key}__", value)
st.markdown(CSS, unsafe_allow_html=True)

st.markdown(
    """
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

    st.markdown(
        f'<div class="chart-title">{n} stages<span class="muted">, feed on stage {feed_stage}.</span></div>',
        unsafe_allow_html=True,
    )

    fig = make_diagram(alpha, R, xD, q, xF, xB, dark=dark)
    st.pyplot(fig)
    plt.close(fig)
except ValueError as e:
    st.error(str(e))