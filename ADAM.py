import streamlit as st
import pandas as pd
from pickle import load
import pickle
import numpy as np
import math as m
from PIL import Image
import os
from glob import glob

st.header("Shaft Fracture Analysis (SFA)")

st.subheader('Dimensional Parameters')
htp="https://ars.els-cdn.com/content/image/1-s2.0-S135063071000004X-gr1.jpg"
st.image(htp, caption= "Fig. 1. Typical failure locations of the palm oil press machine and the model and keyway of the worm screw.")

import streamlit as st
import pandas as pd
import math

def user_input_features():
    st.sidebar.header("Input Parameters")
    
    # Divide inputs into logical sections
    with st.sidebar.expander("🔧 Shaft Specifications", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            power = st.number_input('Power, P (W)', 
                                  min_value=0.01, 
                                  value=1000.0, 
                                  step=10.0,
                                  help="Input power transmitted by the shaft")
            
            rotation_per_second = st.number_input('Rotation, f (RPS)', 
                                               min_value=0.01, 
                                               value=10.0, 
                                               step=0.1,
                                               help="Rotational speed in revolutions per second")
        
        with col2:
            shaft_diameter = st.number_input('Diameter, d (mm)', 
                                           min_value=0.01, 
                                           value=20.0, 
                                           step=0.1,
                                           help="Diameter of the shaft")
            
            vickers_hardness = st.number_input('Hardness, HV (kgf/mm²)', 
                                            min_value=0.01, 
                                            value=200.0, 
                                            step=5.0,
                                            help="Material hardness in Vickers scale")

    with st.sidebar.expander("📏 Correction Factors", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            load_factor = st.number_input('Load Factor, Cload', 
                                        min_value=0.01, 
                                        max_value=1.0, 
                                        value=0.9, 
                                        step=0.01,
                                        help="Correction factor for loading type")
            
            size_factor = st.number_input('Size Factor, Csize', 
                                       min_value=0.01, 
                                       max_value=1.0, 
                                       value=0.85, 
                                       step=0.01,
                                       help="Correction factor for size effects")
            
            surface_factor = st.number_input('Surface Factor, Csurf', 
                                           min_value=0.01, 
                                           max_value=1.0, 
                                           value=0.8, 
                                           step=0.01,
                                           help="Correction factor for surface finish")

        with col2:
            temperature_factor = st.number_input('Temp Factor, Ctemp', 
                                               min_value=0.01, 
                                               max_value=1.0, 
                                               value=1.0, 
                                               step=0.01,
                                               help="Correction factor for temperature")
            
            reliability_factor = st.number_input('Reliability Factor, Creliab', 
                                               min_value=0.01, 
                                               max_value=1.0, 
                                               value=0.9, 
                                               step=0.01,
                                               help="Correction factor for reliability")

    with st.sidebar.expander("⚠️ Stress Parameters", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            stress_concentration_factor = st.number_input('Stress Conc. Factor, Kt', 
                                                       min_value=0.01, 
                                                       value=1.5, 
                                                       step=0.1,
                                                       help="Theoretical stress concentration")
            
            radius = st.number_input('Notch Radius, r (mm)', 
                                   min_value=0.01, 
                                   value=2.0, 
                                   step=0.1,
                                   help="Radius of curvature at the notch")
            
            characteristic_length = st.number_input('Char. Length, ρ (mm)', 
                                                 min_value=0.01, 
                                                 value=0.1, 
                                                 step=0.01,
                                                 help="Material characteristic length")

        with col2:
            minimum_stress = st.number_input('Min Stress, Smin (MPa)', 
                                          min_value=0.00, 
                                          value=50.0, 
                                          step=1.0,
                                          help="Minimum stress in the cycle")
            
            maximum_stress = st.number_input('Max Stress, Smax (MPa)', 
                                          min_value=0.01, 
                                          value=150.0, 
                                          step=1.0,
                                          help="Maximum stress in the cycle")
            
            ultimate_stress = st.number_input('Ultimate Stress, Su (MPa)', 
                                           min_value=0.01, 
                                           value=400.0, 
                                           step=1.0,
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
    # Unpack inputs
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

    # Calculations
    T = P/(2*math.pi*f)  # Torsional loading in Nm
    τ = (16*T)/(math.pi*((d/1000)**3))  # Shear stress in Pa
    Sue = (1.6*HV) + (0.1*HV)  # Uncorrected endurance strength in MPa
    Kf = 1 + ((Kt-1)/(1+math.sqrt(ρ/r)))  # Fatigue notch factor
    Cnotch = 1/Kf  # Notch correction factor
    Se = Cload*Csize*Csurf*Ctemp*Creliab*Cnotch*Sue  # Corrected endurance factor in MPa
    Sa = (Smax - Smin)/2  # Alternating stress in MPa
    Smean = (Smax + Smin)/2  # Mean stress in MPa
    Sf = (Sa*Su/(Su - Smean))  # Fatigue stress in MPa

    return {
        'T': T,
        'τ': τ,
        'Sue': Sue,
        'Kf': Kf,
        'Cnotch': Cnotch,
        'Se': Se,
        'Sa': Sa,
        'Smean': Smean,
        'Sf': Sf
    }

def display_results(inputs, results):
    # Display input parameters in a compact format
    with st.expander("📋 Input Parameters Summary", expanded=True):
        input_data = {
            "Parameter": ["Power (W)", "Rotation (RPS)", "Diameter (mm)", "Hardness (HV)",
                         "Load Factor", "Size Factor", "Surface Factor", "Temp Factor",
                         "Reliability Factor", "Stress Conc. Factor", "Notch Radius (mm)",
                         "Char. Length (mm)", "Min Stress (MPa)", "Max Stress (MPa)",
                         "Ultimate Stress (MPa)"],
            "Value": [inputs['power'], inputs['rotation_per_second'], inputs['shaft_diameter'],
                     inputs['vickers_hardness'], inputs['load_factor'], inputs['size_factor'],
                     inputs['surface_factor'], inputs['temperature_factor'], 
                     inputs['reliability_factor'], inputs['stress_concentration_factor'],
                     inputs['radius'], inputs['characteristic_length'], inputs['minimum_stress'],
                     inputs['maximum_stress'], inputs['ultimate_stress']]
        }
        st.dataframe(pd.DataFrame(input_data), hide_index=True)

    # Display calculation results in a professional layout
    st.header("Calculation Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Torsional Loading, T", f"{results['T']:.2f} Nm")
        st.metric("Shear Stress, τ", f"{results['τ']/1e6:.2f} MPa")  # Convert Pa to MPa
        st.metric("Uncorrected Endurance, Sue", f"{results['Sue']:.2f} MPa")
        st.metric("Fatigue Notch Factor, Kf", f"{results['Kf']:.2f}")
    
    with col2:
        st.metric("Notch Correction, Cnotch", f"{results['Cnotch']:.2f}")
        st.metric("Corrected Endurance, Se", f"{results['Se']:.2f} MPa")
        st.metric("Alternating Stress, Sa", f"{results['Sa']:.2f} MPa")
        st.metric("Mean Stress, Smean", f"{results['Smean']:.2f} MPa")
        st.metric("Fatigue Stress, Sf", f"{results['Sf']:.2f} MPa")

def main():
    st.title("Shaft Torsional Loading Analyzer")
    st.markdown("""
    This application calculates various stress parameters for a rotating shaft under torsional loading,
    considering material properties and correction factors.
    """)
    
    # Get user inputs
    inputs = user_input_features()
    
    # Perform calculations
    results = calculate_results(inputs)
    
    # Display results
    display_results(inputs, results)

if __name__ == "__main__":
    main()
#
#
#
#

def display_results(T, τ, Sue, Kf, Cnotch, Se, Sa, Smean, Sf):
    """Improved version that requires all variables to be passed"""
    τ_mpa = τ / 1e6  # Convert to MPa
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Loading & Stresses")
        st.metric("Torsional Loading", f"{T:.2f} Nm")
        st.metric("Shear Stress", f"{τ_mpa:.2f} MPa")
        st.metric("Alternating Stress", f"{Sa:.2f} MPa")
        st.metric("Mean Stress", f"{Smean:.2f} MPa")
        st.metric("Fatigue Stress", f"{Sf:.2f} MPa")
    
    with col2:
        st.subheader("Material Properties")
        st.metric("Uncorrected Endurance", f"{Sue:.2f} MPa")
        st.metric("Corrected Endurance", f"{Se:.2f} MPa")
        st.metric("Fatigue Notch Factor", f"{Kf:.2f}")
        st.metric("Notch Correction", f"{Cnotch:.2f}")

# Call it like this:
display_results(T, τ, Sue, Kf, Cnotch, Se, Sa, Smean, Sf)

st.subheader('Reference')
st.write('Xian-Kui Zhu, A comparative study of burst failure models for assessing remaining strength of corroded pipelines, Journal of Pipeline Science and Engineering 1 (2021) 36 - 50, https://doi.org/10.1016/j.jpse.2021.01.008')

st.subheader('Assesment')
st.markdown('[Case Study](https://drive.google.com/file/d/1Ako5uVRPYL5k5JeEQ_Xhl9f3pMRBjCJv/view?usp=sharing)', unsafe_allow_html=True)
st.markdown('[Corroded Pipe Burst Data](https://docs.google.com/spreadsheets/d/1YJ7ziuc_IhU7-MMZOnRmh4h21_gf6h5Z/edit?gid=56754844#gid=56754844)', unsafe_allow_html=True)
st.markdown('[Pre-Test](https://forms.gle/wPvcgnZAC57MkCxN8)', unsafe_allow_html=True)
st.markdown('[Post-Test](https://forms.gle/FdiKqpMLzw9ENscA9)', unsafe_allow_html=True)
