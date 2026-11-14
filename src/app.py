import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import matplotlib.pyplot as plt
import streamlit as st

from plotting import make_diagram

st.title("McCabe-Thiele Distillation Calculator")
st.write("Binary distillation with constant relative volatility.")

# Sidebar inputs: st.sidebar.slider(label, min, max, default, step)
alpha = st.sidebar.slider("Relative volatility (alpha)", 1.05, 10.0, 2.5, 0.05)
R = st.sidebar.slider("Reflux ratio (R)", 0.1, 10.0, 2.0, 0.1)
xD = st.sidebar.slider("Distillate composition (xD)", 0.50, 0.99, 0.90, 0.01)
xF = st.sidebar.slider("Feed composition (xF)", 0.01, 0.99, 0.60, 0.01)
xB = st.sidebar.slider("Bottoms composition (xB)", 0.01, 0.99, 0.10, 0.01)
q = st.sidebar.slider("Feed condition (q)", -0.5, 2.0, 1.0, 0.05)
q = round(q, 2)

try:
    fig = make_diagram(alpha, R, xD, q, xF, xB)
    st.pyplot(fig)
    plt.close(fig)
except ValueError as e:
    st.error(str(e))