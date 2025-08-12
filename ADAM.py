import streamlit as st
import pandas as pd
import math
from PIL import Image
import os
import sys
import matplotlib.pyplot as plt

# Custom CSS for vibrant styling
st.markdown("""
<style>
    :root {
        --primary: #4361ee;
        --secondary: #3f37c9;
        --accent: #4895ef;
        --success: #4cc9f0;
        --danger: #f72585;
        --warning: #f8961e;
        --info: #43aa8b;
        --light: #f8f9fa;
        --dark: #212529;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #e0f7fa 0%, #b2ebf2 100%);
        border-right: 1px solid #b2ebf2;
    }
    .metric-box {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid var(--accent);
        transition: transform 0.3s ease;
    }
    .metric-box:hover {
        transform: translateY(-5px);
    }
    .header {
        color: var(--secondary);
        border-bottom: 3px solid var(--accent);
        padding-bottom: 8px;
        margin-top: 25px;
        font-weight: 700;
    }
    .stExpander {
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .stButton>button {
        background: linear-gradient(45deg, var(--primary) 0%, var(--accent) 100%);
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        padding: 10px 24px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    .input-label {
        font-weight: 600;
        color: var(--secondary);
    }
    .section-title {
        background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 20px 0 15px 0;
        font-size: 1.1em;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .safety-box {
        padding: 20px;
        border-radius: 12px;
        margin: 25px 0;
        font-size: 1.1em;
        box-shadow: 0 6px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# App Header with animated icon
st.markdown("""
<div style="display: flex; align-items: center; margin-bottom: 20px;">
    <img src="https://img.icons8.com/fluency/96/000000/maintenance.png" width="80" style="margin-right: 20px; animation: pulse 2s infinite;">
    <div>
        <h1 style="color: #3f37c9; margin-bottom: 5px;">Shaft Fracture Analysis</h1>
        <p style="color: #555; font-size: 1.1em;">🔧 Analyze torsional loading and fatigue failure in rotating shafts with precision</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero section with key features
st.markdown("""
<div style="background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 6px 10px rgba(0,0,0,0.1);">
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 200px; margin: 10px;">
            <div style="display: flex; align-items: center;">
                <img src="https://img.icons8.com/color/48/000000/gears.png" width="30" style="margin-right: 10px;">
                <h4 style="margin: 0;">Shaft Specifications</h4>
            </div>
            <p style="margin: 5px 0 0 35px; font-size: 0.9em;">Diameter, power, rotation speed</p>
        </div>
        <div style="flex: 1; min-width: 200px; margin: 10px;">
            <div style="display: flex; align-items: center;">
                <img src="https://img.icons8.com/color/48/000000/maintenance.png" width="30" style="margin-right: 10px;">
                <h4 style="margin: 0;">Material Properties</h4>
            </div>
            <p style="margin: 5px 0 0 35px; font-size: 0.9em;">Hardness, strength, fatigue</p>
        </div>
        <div style="flex: 1; min-width: 200px; margin: 10px;">
            <div style="display: flex; align-items: center;">
                <img src="https://img.icons8.com/color/48/000000/engineering.png" width="30" style="margin-right: 10px;">
                <h4 style="margin: 0;">Stress Analysis</h4>
            </div>
            <p style="margin: 5px 0 0 35px; font-size: 0.9em;">Shear stress, endurance limits</p>
        </div>
        <div style="flex: 1; min-width: 200px; margin: 10px;">
            <div style="display: flex; align-items: center;">
                <img src="https://img.icons8.com/color/48/000000/safety-certificate.png" width="30" style="margin-right: 10px;">
                <h4 style="margin: 0;">Safety Factors</h4>
            </div>
            <p style="margin: 5px 0 0 35px; font-size: 0.9em;">Design validation, safety margins</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar for user inputs with icons
def user_input_features():
    st.sidebar.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 15px;">
        <img src="https://img.icons8.com/color/48/000000/settings.png" width="30" style="margin-right: 10px;">
        <h2 style="margin: 0; color: #3f37c9;">Input Parameters</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Shaft Specifications
    with st.sidebar.expander("🔧 Shaft Specifications", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p class="input-label">⚡ Power, P (W)</p>', unsafe_allow_html=True)
            power = st.number_input('', min_value=0.01, step=0.01, key='power',
                                  help="Input power transmitted by the shaft")
            
            st.markdown('<p class="input-label">🔄 Rotation, f (RPS)</p>', unsafe_allow_html=True)
            rotation_per_second = st.number_input('', min_value=0.01, step=0.01, key='rotation',
                                                help="Rotational speed in revolutions per second")
        
        with col2:
            st.markdown('<p class="input-label">📏 Diameter, d (mm)</p>', unsafe_allow_html=True)
            shaft_diameter = st.number_input('', min_value=0.01, step=0.01, key='diameter',
                                           help="Diameter of the shaft")
            
            st.markdown('<p class="input-label">💎 Hardness, HV (kgf/mm²)</p>', unsafe_allow_html=True)
            vickers_hardness = st.number_input('', min_value=0.01, step=0.01, key='hardness',
                                             help="Material hardness in Vickers scale")

    # Correction Factors
    with st.sidebar.expander("📊 Correction Factors", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p class="input-label">⚖️ Load Factor, Cload</p>', unsafe_allow_html=True)
            load_factor = st.number_input('', min_value=0.01, step=0.01, key='load_factor',
                                        help="Correction factor for loading type")
            
            st.markdown('<p class="input-label">📐 Size Factor, Csize</p>', unsafe_allow_html=True)
            size_factor = st.number_input('', min_value=0.01, step=0.01, key='size_factor',
                                        help="Correction factor for size effects")
            
            st.markdown('<p class="input-label">✨ Surface Factor, Csurf</p>', unsafe_allow_html=True)
            surface_factor = st.number_input('', min_value=0.01, step=0.01, key='surface_factor',
                                          help="Correction factor for surface finish")

        with col2:
            st.markdown('<p class="input-label">🌡️ Temp Factor, Ctemp</p>', unsafe_allow_html=True)
            temperature_factor = st.number_input('', min_value=0.01, step=0.01, key='temp_factor',
                                               help="Correction factor for temperature")
            
            st.markdown('<p class="input-label">🛡️ Reliability Factor, Creliab</p>', unsafe_allow_html=True)
            reliability_factor = st.number_input('', min_value=0.01, step=0.01, key='reliab_factor',
                                              help="Correction factor for reliability")

    # Stress Parameters
    with st.sidebar.expander("⚠️ Stress Parameters", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p class="input-label">❗ Stress Conc. Factor, Kt</p>', unsafe_allow_html=True)
            stress_concentration_factor = st.number_input('', min_value=0.01, step=0.01, key='stress_factor',
                                                        help="Theoretical stress concentration")
            
            st.markdown('<p class="input-label">🔵 Notch Radius, r (mm)</p>', unsafe_allow_html=True)
            radius = st.number_input('', min_value=0.01, step=0.01, key='radius',
                                   help="Radius of curvature at the notch")
            
            st.markdown('<p class="input-label">📏 Char. Length, ρ (mm)</p>', unsafe_allow_html=True)
            characteristic_length = st.number_input('', min_value=0.01, step=0.01, key='char_length',
                                                  help="Material characteristic length")

        with col2:
            st.markdown('<p class="input-label">🔻 Min Stress, Smin (MPa)</p>', unsafe_allow_html=True)
            minimum_stress = st.number_input('', min_value=0.00, step=0.01, key='min_stress',
                                           help="Minimum stress in the cycle")
            
            st.markdown('<p class="input-label">🔺 Max Stress, Smax (MPa)</p>', unsafe_allow_html=True)
            maximum_stress = st.number_input('', min_value=0.01, step=0.01, key='max_stress',
                                           help="Maximum stress in the cycle")
            
            st.markdown('<p class="input-label">💪 Ultimate Stress, Su (MPa)</p>', unsafe_allow_html=True)
            ultimate_stress = st.number_input('', min_value=0.01, step=0.01, key='ultimate_stress',
                                            help="Ultimate tensile strength")

    return {
        'power': power,
        'rotation_per_second': rotation_per_second,
        'shaft_diameter': shaft_diameter,
        'vickers_hardness': vickers_hardness,
        'load_factor': load_factor,
        'size_factor': size_factor,
        'surface_factor': surface_factor,
        'temperature_factor': temperature_factor,
        'reliability_factor': reliability_factor,
        'stress_concentration_factor': stress_concentration_factor,
        'radius': radius,
        'characteristic_length': characteristic_length,
        'minimum_stress': minimum_stress,
        'maximum_stress': maximum_stress,
        'ultimate_stress': ultimate_stress
    }

def calculate_results(inputs):
    # Calculations remain the same as original
    P = inputs['power']
    f = inputs['rotation_per_second']
    d = inputs['shaft_diameter']
    HV = inputs['vickers_hardness']
    Cload = inputs['load_factor']
    Csize = inputs['size_factor']
    Csurf = inputs['surface_factor']
    Ctemp = inputs['temperature_factor']
    Creliab = inputs['reliability_factor']
    Kt = inputs['stress_concentration_factor']
    r = inputs['radius']
    ρ = inputs['characteristic_length']
    Smin = inputs['minimum_stress']
    Smax = inputs['maximum_stress']
    Su = inputs['ultimate_stress']

    T = P/(2*math.pi*f)
    τ = (16*T)/(math.pi*((d/1000)**3))
    Sue = (1.6*HV) + (0.1*HV)
    Kf = 1 + ((Kt-1)/(1+math.sqrt(ρ/r)))
    Cnotch = 1/Kf
    Se = Cload*Csize*Csurf*Ctemp*Creliab*Cnotch*Sue
    Sa = (Smax - Smin)/2
    Smean = (Smax + Smin)/2
    Sf = (Sa*Su/(Su - Smean)) if (Su - Smean) != 0 else 0

    return {
        'T': T,
        'τ': τ/1e6,  # Convert to MPa
        'Sue': Sue,
        'Kf': Kf,
        'Cnotch': Cnotch,
        'Se': Se,
        'Sa': Sa,
        'Smean': Smean,
        'Sf': Sf
    }

def display_results(inputs, results):
    # Input summary with icons
    with st.expander("📋 Input Parameters Summary", expanded=False):
        input_data = {
            "Parameter": ["⚡ Power (W)", "🔄 Rotation (RPS)", "📏 Diameter (mm)", "💎 Hardness (HV)",
                         "⚖️ Load Factor", "📐 Size Factor", "✨ Surface Factor", "🌡️ Temp Factor",
                         "🛡️ Reliability Factor", "❗ Stress Conc. Factor", "🔵 Notch Radius (mm)",
                         "📏 Char. Length (mm)", "🔻 Min Stress (MPa)", "🔺 Max Stress (MPa)",
                         "💪 Ultimate Stress (MPa)"],
            "Value": [inputs['power'], inputs['rotation_per_second'], inputs['shaft_diameter'],
                     inputs['vickers_hardness'], inputs['load_factor'], inputs['size_factor'],
                     inputs['surface_factor'], inputs['temperature_factor'], 
                     inputs['reliability_factor'], inputs['stress_concentration_factor'],
                     inputs['radius'], inputs['characteristic_length'], inputs['minimum_stress'],
                     inputs['maximum_stress'], inputs['ultimate_stress']]
        }
        st.dataframe(pd.DataFrame(input_data), hide_index=True, use_container_width=True)

    # Results display with animated metrics
    st.markdown("<h2 class='header'>📊 Calculation Results</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
        st.metric("🔩 Torsional Loading, T", f"{results['T']:.2f} Nm", 
                 help="Torque applied to the shaft")
        st.metric("🌀 Shear Stress, τ", f"{results['τ']:.2f} MPa", 
                 help="Maximum shear stress in the shaft")
        st.metric("💎 Uncorrected Endurance, Sue", f"{results['Sue']:.2f} MPa", 
                 help="Material endurance limit without corrections")
        st.metric("❗ Fatigue Notch Factor, Kf", f"{results['Kf']:.2f}", 
                 help="Factor accounting for stress concentration effects")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
        st.metric("🔄 Notch Correction, Cnotch", f"{results['Cnotch']:.2f}", 
                 help="Correction factor for notches")
        st.metric("🛡️ Corrected Endurance, Se", f"{results['Se']:.2f} MPa", 
                 help="Adjusted endurance limit with all factors")
        st.metric("🔄 Alternating Stress, Sa", f"{results['Sa']:.2f} MPa", 
                 help="Amplitude of cyclic stress")
        st.metric("⚖️ Mean Stress, Smean", f"{results['Smean']:.2f} MPa", 
                 help="Average stress in the cycle")
        st.metric("⚠️ Fatigue Stress, Sf", f"{results['Sf']:.2f} MPa", 
                 help="Equivalent fatigue stress")
        st.markdown("</div>", unsafe_allow_html=True)

    # Enhanced safety factor display
    safety_factor = results['Se'] / (results['Sf'] if results['Sf'] != 0 else 1e-6)
    
    if safety_factor > 1.5:
        safety_style = "background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border-left: 5px solid #28a745;"
        safety_icon = "✅"
        safety_text = "Excellent Safety Margin"
    elif safety_factor > 1:
        safety_style = "background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%); border-left: 5px solid #ffc107;"
        safety_icon = "⚠️"
        safety_text = "Adequate Safety Margin"
    else:
        safety_style = "background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); border-left: 5px solid #dc3545;"
        safety_icon = "❌"
        safety_text = "Design Concern"
    
    st.markdown(f"""
    <div class="safety-box" style="{safety_style}">
        <div style="font-size: 1.5em; margin-bottom: 10px;">
            {safety_icon} <strong>{safety_text}</strong>
        </div>
        <div style="font-size: 2em; font-weight: bold; margin: 10px 0; color: {'#155724' if safety_factor > 1.5 else '#856404' if safety_factor > 1 else '#721c24'}">
            Safety Factor: {safety_factor:.2f}
        </div>
        <div style="font-size: 0.9em;">
            {"Design exceeds safety requirements" if safety_factor > 1.5 else 
             "Design meets minimum safety requirements" if safety_factor > 1 else 
             "Design may be unsafe - consider modifications"}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main function with visual enhancements
def main():
    # Visual diagram
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <h3 class="header">📐 Shaft Diagram and Critical Parameters</h3>
        <img src="https://www.researchgate.net/publication/334382748/figure/fig1/AS:779834947051520@1562868406585/Schematic-diagram-of-shaft-loading.png" 
             style="max-width: 100%; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        <p style="font-size: 0.9em; color: #666;">Figure: Schematic of shaft loading and critical stress locations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get user inputs
    inputs = user_input_features()
    
    # Calculate button with animation
    if st.button("🚀 Calculate Shaft Parameters", use_container_width=True):
        with st.spinner("⚙️ Analyzing shaft stresses..."):
            # Perform calculations
            results = calculate_results(inputs)
            
            # Display results
            display_results(inputs, results)
    else:
        st.info("👆 Enter your parameters above and click the Calculate button to analyze your shaft design")

    # References with cards
    st.markdown("---")
    st.markdown("<h3 class='header'>📚 References & Resources</h3>", unsafe_allow_html=True)
    
    ref_col1, ref_col2 = st.columns(2)

    with ref_col1:
        st.markdown("""
        <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px;">
            <h4 style="color: #3f37c9; margin-top: 0;">📖 Reference Paper</h4>
            <p>Xian-Kui Zhu, A comparative study of burst failure models for assessing remaining strength of corroded pipelines</p>
            <a href="https://doi.org/10.1016/j.jpse.2021.01.008" target="_blank" style="color: #4361ee; text-decoration: none;">🔗 DOI Link</a>
        </div>
        """, unsafe_allow_html=True)
        
    with ref_col2:
        st.markdown("""
        <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px;">
            <h4 style="color: #3f37c9; margin-top: 0;">🔧 Additional Resources</h4>
            <p><a href="https://drive.google.com/file/d/1Ako5uVRPYL5k5JeEQ_Xhl9f3pMRBjCJv/view?usp=sharing" target="_blank" style="color: #4361ee; text-decoration: none;">📂 Case Study</a></p>
            <p><a href="https://docs.google.com/spreadsheets/d/1YJ7ziuc_IhU7-MMZOnRmh4h21_gf6h5Z/edit?gid=56754844#gid=56754844" target="_blank" style="color: #4361ee; text-decoration: none;">📊 Corroded Pipe Data</a></p>
            <p><a href="https://forms.gle/wPvcgnZAC57MkCxN8" target="_blank" style="color: #4361ee; text-decoration: none;">📝 Pre-Test</a></p>
            <p><a href="https://forms.gle/FdiKqpMLzw9ENscA9" target="_blank" style="color: #4361ee; text-decoration: none;">📝 Post-Test</a></p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
