import streamlit as st
import pandas as pd
import math
from PIL import Image
import numpy as np

# ===== 🎨 Custom CSS Styling =====
st.markdown("""
<style>
    /* Page background with subtle gradient */
    .main {
        background: linear-gradient(135deg, #f0f9ff, #cbebff);
    }

    /* Sidebar style */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #ffffff, #e6f2ff);
        padding: 15px;
    }

    /* Section headers */
    .section-header {
        font-size: 20px;
        font-weight: bold;
        color: #2c3e50;
        border-left: 5px solid #3498db;
        padding-left: 10px;
        margin-top: 15px;
    }

    /* Metric display box */
    .metric-box {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
        box-shadow: 0px 3px 8px rgba(0,0,0,0.05);
        transition: all 0.2s ease-in-out;
    }
    .metric-box:hover {
        transform: scale(1.02);
        box-shadow: 0px 5px 12px rgba(0,0,0,0.1);
    }

    /* Buttons */
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
        border: none;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #2c80b4;
        transform: scale(1.03);
    }
</style>
""", unsafe_allow_html=True)

# ===== 🚀 App Header =====
st.image("https://img.icons8.com/color/96/gear.png", width=80)
st.title("⚙️ Shaft Fracture Analysis (SFA)")
st.markdown("""
<div style="background-color:#e0f7fa;padding:15px;border-radius:10px;margin-bottom:20px;">
    <h4 style="color:#00796b;">Analyze torsional loading and fatigue failure in rotating shafts</h4>
    <p style="color:#004d40;">Enter your shaft specifications and material data to get instant calculations for stress, fatigue life, and safety factors.</p>
</div>
""", unsafe_allow_html=True)

# ===== 📥 Sidebar Inputs =====
def user_input_features():
    st.sidebar.header("📊 Input Parameters")

    # Shaft Specs
    with st.sidebar.expander("🔩 Shaft Specifications", expanded=True):
        power = st.number_input('⚡ Power, P (W)', min_value=0.01, step=0.01)
        rotation_per_second = st.number_input('🔄 Rotation, f (RPS)', min_value=0.01, step=0.01)
        shaft_diameter = st.number_input('📏 Diameter, d (mm)', min_value=0.01, step=0.01)
        vickers_hardness = st.number_input('💎 Hardness, HV (kgf/mm²)', min_value=0.01, step=0.01)

    # Correction Factors
    with st.sidebar.expander("🛠️ Correction Factors", expanded=False):
        load_factor = st.number_input('📦 Load Factor, Cload', min_value=0.01, step=0.01)
        size_factor = st.number_input('📐 Size Factor, Csize', min_value=0.01, step=0.01)
        surface_factor = st.number_input('✨ Surface Factor, Csurf', min_value=0.01, step=0.01)
        temperature_factor = st.number_input('🌡️ Temp Factor, Ctemp', min_value=0.01, step=0.01)
        reliability_factor = st.number_input('✅ Reliability Factor, Creliab', min_value=0.01, step=0.01)

    # Stress Parameters
    with st.sidebar.expander("⚠️ Stress Parameters", expanded=False):
        stress_concentration_factor = st.number_input('📎 Stress Conc. Factor, Kt', min_value=0.01, step=0.01)
        radius = st.number_input('🎯 Notch Radius, r (mm)', min_value=0.01, step=0.01)
        characteristic_length = st.number_input('📐 Char. Length, ρ (mm)', min_value=0.01, step=0.01)
        minimum_stress = st.number_input('⬇️ Min Stress, Smin (MPa)', min_value=0.00, step=0.01)
        maximum_stress = st.number_input('⬆️ Max Stress, Smax (MPa)', min_value=0.01, step=0.01)
        ultimate_stress = st.number_input('🏋️ Ultimate Stress, Su (MPa)', min_value=0.01, step=0.01)

    return locals()

# ===== 🧮 Calculations =====
def calculate_results(inputs):
    P, f, d, HV = inputs['power'], inputs['rotation_per_second'], inputs['shaft_diameter'], inputs['vickers_hardness']
    Cload, Csize, Csurf, Ctemp, Creliab = inputs['load_factor'], inputs['size_factor'], inputs['surface_factor'], inputs['temperature_factor'], inputs['reliability_factor']
    Kt, r, ρ, Smin, Smax, Su = inputs['stress_concentration_factor'], inputs['radius'], inputs['characteristic_length'], inputs['minimum_stress'], inputs['maximum_stress'], inputs['ultimate_stress']

    T = P / (2 * math.pi * f)  # Nm
    τ = (16 * T) / (math.pi * ((d/1000)**3))  # Pa
    Sue = (1.6 * HV) + (0.1 * HV)  # MPa
    Kf = 1 + ((Kt - 1) / (1 + math.sqrt(ρ / r)))
    Cnotch = 1 / Kf
    Se = Cload * Csize * Csurf * Ctemp * Creliab * Cnotch * Sue
    Sa = (Smax - Smin) / 2
    Smean = (Smax + Smin) / 2
    Sf = (Sa * Su / (Su - Smean))

    return locals()

# ===== 📊 Display Results =====
def display_results(results):
    st.markdown("<div class='section-header'>📈 Calculation Results</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
        st.metric("🔧 Torsional Loading, T", f"{results['T']:.2f} Nm")
        st.metric("🔩 Shear Stress, τ", f"{results['τ']/1e6:.2f} MPa")
        st.metric("💎 Uncorrected Endurance, Sue", f"{results['Sue']:.2f} MPa")
        st.metric("🧷 Fatigue Notch Factor, Kf", f"{results['Kf']:.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
        st.metric("📏 Notch Correction, Cnotch", f"{results['Cnotch']:.2f}")
        st.metric("📊 Corrected Endurance, Se", f"{results['Se']:.2f} MPa")
        st.metric("🔀 Alternating Stress, Sa", f"{results['Sa']:.2f} MPa")
        st.metric("➕ Mean Stress, Smean", f"{results['Smean']:.2f} MPa")
        st.metric("🏋️ Fatigue Stress, Sf", f"{results['Sf']:.2f} MPa")
        st.markdown("</div>", unsafe_allow_html=True)

    # Safety Factor
    sf = results['Se'] / (results['Sf'] if results['Sf'] != 0 else 1)
    st.markdown(f"""
    <div style="background-color:{"#d4edda" if sf > 1 else "#f8d7da"};
                padding:15px;border-radius:10px;
                border-left:5px solid {"#28a745" if sf > 1 else "#dc3545"}">
        <h4>{"✅ Safe Design" if sf > 1 else "⚠️ Design Concern"}</h4>
        <p>Safety Factor: <strong>{sf:.2f}</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ===== Main App =====
def main():
    inputs = user_input_features()
    results = calculate_results(inputs)
    display_results(results)

if __name__ == "__main__":
    main()


