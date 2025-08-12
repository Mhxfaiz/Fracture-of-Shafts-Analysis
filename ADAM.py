import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards  # Extra styling

# ====== 🎨 Custom CSS for Dark Neon Theme ======
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #0d1b2a, #1b263b);
        color: white;
    }
    .main {
        background-color: transparent;
    }
    /* Glassmorphism effect for cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 20px rgba(0, 255, 255, 0.2);
        margin-bottom: 20px;
    }
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: rgba(10, 20, 40, 0.95);
        border-right: 2px solid #00ffff;
    }
    /* Headers */
    .section-header {
        font-size: 20px;
        font-weight: bold;
        color: #00ffff;
        border-left: 5px solid #00ffff;
        padding-left: 10px;
        margin-bottom: 10px;
    }
    /* Metric hover animation */
    .stMetric {
        transition: all 0.3s ease-in-out;
    }
    .stMetric:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 15px rgba(0,255,255,0.5);
    }
</style>
""", unsafe_allow_html=True)

# ====== 🚀 App Header ======
st.image("https://img.icons8.com/external-flat-juicy-fish/100/00ffff/external-engine-industry-flat-flat-juicy-fish.png", width=80)
st.markdown("<h1 style='color:#00ffff;'>Shaft Fracture Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#a3f7ff;'>Real-time engineering calculations for torsional loading, fatigue failure & safety factors</p>", unsafe_allow_html=True)

# ====== Sidebar Inputs ======
def user_input_features():
    st.sidebar.markdown("<h2 style='color:#00ffff;'>⚙️ Input Parameters</h2>", unsafe_allow_html=True)

    with st.sidebar.expander("🔩 Shaft Specifications", expanded=True):
        power = st.number_input('⚡ Power, P (W)', min_value=0.01, step=0.01)
        rotation_per_second = st.number_input('🔄 Rotation, f (RPS)', min_value=0.01, step=0.01)
        shaft_diameter = st.number_input('📏 Diameter, d (mm)', min_value=0.01, step=0.01)
        vickers_hardness = st.number_input('💎 Hardness, HV (kgf/mm²)', min_value=0.01, step=0.01)

    with st.sidebar.expander("🛠️ Correction Factors", expanded=False):
        load_factor = st.number_input('📦 Load Factor, Cload', min_value=0.01, step=0.01)
        size_factor = st.number_input('📐 Size Factor, Csize', min_value=0.01, step=0.01)
        surface_factor = st.number_input('✨ Surface Factor, Csurf', min_value=0.01, step=0.01)
        temperature_factor = st.number_input('🌡️ Temp Factor, Ctemp', min_value=0.01, step=0.01)
        reliability_factor = st.number_input('✅ Reliability Factor, Creliab', min_value=0.01, step=0.01)

    with st.sidebar.expander("⚠️ Stress Parameters", expanded=False):
        stress_concentration_factor = st.number_input('📎 Stress Conc. Factor, Kt', min_value=0.01, step=0.01)
        radius = st.number_input('🎯 Notch Radius, r (mm)', min_value=0.01, step=0.01)
        characteristic_length = st.number_input('📐 Char. Length, ρ (mm)', min_value=0.01, step=0.01)
        minimum_stress = st.number_input('⬇️ Min Stress, Smin (MPa)', min_value=0.00, step=0.01)
        maximum_stress = st.number_input('⬆️ Max Stress, Smax (MPa)', min_value=0.01, step=0.01)
        ultimate_stress = st.number_input('🏋️ Ultimate Stress, Su (MPa)', min_value=0.01, step=0.01)

    return locals()

# ====== Calculations ======
def calculate_results(inputs):
    P, f, d, HV = inputs['power'], inputs['rotation_per_second'], inputs['shaft_diameter'], inputs['vickers_hardness']
    Cload, Csize, Csurf, Ctemp, Creliab = inputs['load_factor'], inputs['size_factor'], inputs['surface_factor'], inputs['temperature_factor'], inputs['reliability_factor']
    Kt, r, rho, Smin, Smax, Su = inputs['stress_concentration_factor'], inputs['radius'], inputs['characteristic_length'], inputs['minimum_stress'], inputs['maximum_stress'], inputs['ultimate_stress']

    T = P / (2 * math.pi * f)
    tau = (16 * T) / (math.pi * ((d/1000)**3))
    Sue = (1.6 * HV) + (0.1 * HV)
    Kf = 1 + ((Kt - 1) / (1 + math.sqrt(rho / r)))
    Cnotch = 1 / Kf
    Se = Cload * Csize * Csurf * Ctemp * Creliab * Cnotch * Sue
    Sa = (Smax - Smin) / 2
    Smean = (Smax + Smin) / 2
    Sf = (Sa * Su / (Su - Smean))
    SF_ratio = Se / (Sf if Sf != 0 else 1)

    return locals()

# ====== Gauges for Results ======
def gauge_chart(value, title, max_value, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        gauge={'axis': {'range': [None, max_value]},
               'bar': {'color': color},
               'bgcolor': "rgba(255,255,255,0)",
               'borderwidth': 2,
               'bordercolor': "#00ffff"},
        title={'text': title, 'font': {'color': 'white', 'size': 16}}
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': 'white'})
    return fig

# ====== Display Results ======
def display_results(results):
    st.markdown("<div class='section-header'>📊 Calculation Results</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.plotly_chart(gauge_chart(results['T'], "Torsional Load (Nm)", results['T']*1.5, "#00ffff"), use_container_width=True)
    col2.plotly_chart(gauge_chart(results['tau']/1e6, "Shear Stress (MPa)", results['tau']/1e6*1.5, "#ff5e57"), use_container_width=True)
    col3.plotly_chart(gauge_chart(results['SF_ratio'], "Safety Factor", 3, "#28a745"), use_container_width=True)

    with st.expander("📄 Detailed Numbers"):
        style_metric_cards()
        st.metric("Uncorrected Endurance (Sue)", f"{results['Sue']:.2f} MPa")
        st.metric("Fatigue Notch Factor (Kf)", f"{results['Kf']:.2f}")
        st.metric("Corrected Endurance (Se)", f"{results['Se']:.2f} MPa")
        st.metric("Alternating Stress (Sa)", f"{results['Sa']:.2f} MPa")
        st.metric("Mean Stress (Smean)", f"{results['Smean']:.2f} MPa")
        st.metric("Fatigue Stress (Sf)", f"{results['Sf']:.2f} MPa")

# ====== Main App ======
def main():
    inputs = user_input_features()
    results = calculate_results(inputs)
    display_results(results)

if __name__ == "__main__":
    main()
