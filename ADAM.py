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

st.sidebar.header('User Input Parameters')

def user_input_features():
    power = st.sidebar.number_input('Power, P (W)', value = 0.01)
    rotation_per_second = st.sidebar.number_input('Rotation Per Second, f (RPS)', value = 0.01)
    shaft_diameter = st.sidebar.number_input('Shaft Diameter, d (mm)', value = 0.01)
    vickers_hardness = st.sidebar.number_input('Vickers Hardness, HV (kgf/mm)', value = 0.01)
    load_factor = st.sidebar.number_input('Load Factor, Cload', value = 0.01)
    size_factor = st.sidebar.number_input('Size Factor, Csize', value = 0.01)
    surface_factor = st.sidebar.number_input('Surface Factor, Csurf', value = 0.01)
    temperature_factor = st.sidebar.number_input('Temperature Factor, Ctemp', value = 0.01)
    reliability_factor = st.sidebar.number_input('Reliability Factor, Creliab', value = 0.01)
    stress_concentration_factor = st.sidebar.number_input('Stress Concentration Factor, Kt', value = 0.01)
    radius = st.sidebar.number_input('Radius at the Notch Root, r (mm)', value = 0.01)
    characteristic_length = st.sidebar.number_input('Characteristic Length, ρ (mm)', value = 0.01)
    minimum_stress = st.sidebar.number_input('Minimum Stress, Smin (MPa)', value = 0.00)
    maximum_stress = st.sidebar.number_input('Maximum Stress, Smax (MPa)', value = 0.00)
    ultimate_stress = st.sidebar.number_input('Ultimate Stress, Su (MPa)', value = 0.01)
    
    data = {'P (W)': power,
            'f (RPS)': rotation_per_second,
            'd (mm)': shaft_diameter,
            'HV (kgf/mm)': vickers_hardness,
            'Cload' : load_factor,
            'Csize' : size_factor,
            'Csurf' : surface_factor,
            'Ctemp' : temperature_factor,
            'Creliab' : reliability_factor,
            'Kt' : stress_concentration_factor,
            'r (mm)' : radius,
            'ρ (mm)' : characteristic_length,
            'Smin (MPa)' : minimum_stress,
            'Smax (MPa)' : maximum_stress, 
            'Su (MPa)' : ultimate_stress, }

    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

P=df['P (W)'].values.item()
f=df['f (RPS)'].values.item()
d=df['d (mm)'].values.item()
HV=df['HV (kgf/mm)'].values.item()
Cload=df['Cload'].values.item()
Csize=df['Csize'].values.item()
Csurf=df['Csurf'].values.item()
Ctemp=df['Ctemp'].values.item()
Creliab=df['Creliab'].values.item()
Kt=df['Kt'].values.item()
r=df['r (mm)'].values.item()
ρ=df['ρ (mm)'].values.item()
Smin=df['Smin (MPa)'].values.item()
Smax=df['Smax (MPa)'].values.item()
Su=df['Su (MPa)'].values.item()

st.subheader('Notes')
st.write('If shaft diameter,d ≤ 8mm, Csize = 1.00')
st.write('Else if shaft diameter,d > 8mm and ≤ 250mm, Csize = 1.189(pow(d, -0.097))')

# Calculate torsional loading T
T = P/(2*(22/7)*f)

# Calculate shear stress τ
τ = (16*T)/((22/7)*((d/1000)*(d/1000)*(d/1000)))

# Calculate uncorrected endurance strength Sue
Sue = (1.6*HV) + (0.1*HV)

# Calculate fatigue notch factor
Kf = 1 + ((Kt-1)/(1+m.sqrt(ρ/r)))

# Calculate notch correction factor
Cnotch = 1/Kf

# Calculate corrected endurance factor Se
Se = Cload*Csize*Csurf*Ctemp*Creliab*Cnotch*Sue

# Calculate alternating stress
Sa = ((Smax - Smin)/2)

# Calculate mean stress
Smean = ((Smax + Smin)/2)

# Calculate fatigue stress
Sf = (Sa*Su/(Su - Smean))

user_input={'P (W)': "{:.2f}".format(P),
            'f (RPS)': "{:.2f}".format(f),
            'd (mm)': "{:.2f}".format(d),
            'HV (kgf/mm)': "{:.2f}".format(HV),
            'Cload': "{:.2f}".format(Cload),
            'Csize': "{:.2f}".format(Csize),
            'Csurf': "{:.2f}".format(Csurf),
            'Ctemp': "{:.2f}".format(Ctemp),
            'Creliab': "{:.2f}".format(Creliab),
            'Kt': "{:.2f}".format(Kt),
            'r (mm)': "{:.2f}".format(r),
            'ρ (mm)': "{:.2f}".format(ρ),
            'Smin (MPa)' : "{:.2f}".format (Smin),
            'Smax (MPa)' : "{:.2f}".format (Smax), 
            'Su (MPa)' : "{:.2f}".format (Su), }

user_input_df=pd.DataFrame(user_input, index=[0])
st.subheader('User Input Parameters')
st.write(user_input_df)

def display_results():
    # Create a container for better organization
    with st.container():
        st.header("Torsional Loading Analysis Results")
        
        # Divide results into logical sections with columns
        col1, col2 = st.columns(2)
        
        with col1:
            # Loading and Stress Section
            st.subheader("Loading & Stresses")
            
            # Torsional Loading
            st.metric(label="Torsional Loading (T)", 
                     value=f"{T:.2f} Nm",
                     help="Calculated torsional moment")
            
            # Shear Stress
            st.metric(label="Shear Stress (τ)", 
                     value=f"{τ:.2f} Pa",
                     help="Calculated shear stress")
            
            # Alternating Stress
            st.metric(label="Alternating Stress (Sa)", 
                     value=f"{Sa:.2f} MPa",
                     help="Calculated alternating stress")
            
            # Mean Stress
            st.metric(label="Mean Stress (Smean)", 
                     value=f"{Smean:.2f} MPa",
                     help="Calculated mean stress")
            
            # Fatigue Stress
            st.metric(label="Fatigue Stress (Sf)", 
                     value=f"{Sf:.2f} MPa",
                     help="Calculated fatigue stress")
        
        with col2:
            # Material Properties Section
            st.subheader("Material Properties")
            
            # Uncorrected Endurance Strength
            st.metric(label="Uncorrected Endurance Strength (Sue)", 
                     value=f"{Sue:.2f} MPa",
                     help="Material's uncorrected endurance limit")
            
            # Corrected Endurance Factor
            st.metric(label="Corrected Endurance Factor (Se)", 
                     value=f"{Se:.2f} MPa",
                     help="Corrected endurance strength")
            
            # Fatigue Notch Factor
            st.metric(label="Fatigue Notch Factor (Kf)", 
                     value=f"{Kf:.2f}",
                     help="Stress concentration factor for fatigue")
            
            # Notch Factor Correction
            st.metric(label="Notch Factor Correction (Cnotch)", 
                     value=f"{Cnotch:.2f}",
                     help="Correction factor for notches")
        
        # Add a divider
        st.divider()
        
        # Detailed Data Section (expandable)
        with st.expander("View Detailed Data Tables"):
            st.subheader("Detailed Results")
            
            # Create tabs for different result categories
            tab1, tab2, tab3 = st.tabs(["Loading & Stresses", "Material Properties", "All Results"])
            
            with tab1:
                st.write("**Loading and Stress Values**")
                loading_data = {
                    "Parameter": ["Torsional Loading (Nm)", "Shear Stress (Pa)", 
                                "Alternating Stress (MPa)", "Mean Stress (MPa)", 
                                "Fatigue Stress (MPa)"],
                    "Value": [T, τ, Sa, Smean, Sf]
                }
                st.dataframe(pd.DataFrame(loading_data), hide_index=True)
            
            with tab2:
                st.write("**Material Property Values**")
                material_data = {
                    "Parameter": ["Uncorrected Endurance Strength (MPa)", 
                                "Corrected Endurance Factor (MPa)",
                                "Fatigue Notch Factor", 
                                "Notch Factor Correction"],
                    "Value": [Sue, Se, Kf, Cnotch]
                }
                st.dataframe(pd.DataFrame(material_data), hide_index=True)
            
            with tab3:
                st.write("**Complete Results**")
                complete_data = {
                    "Parameter": ["Torsional Loading", "Shear Stress", 
                                 "Uncorrected Endurance Strength", "Fatigue Notch Factor",
                                 "Notch Factor Correction", "Corrected Endurance Factor",
                                 "Alternating Stress", "Mean Stress", "Fatigue Stress"],
                    "Symbol": ["T", "τ", "Sue", "Kf", "Cnotch", "Se", "Sa", "Smean", "Sf"],
                    "Value": [T, τ, Sue, Kf, Cnotch, Se, Sa, Smean, Sf],
                    "Units": ["Nm", "Pa", "MPa", "", "", "MPa", "MPa", "MPa", "MPa"]
                }
                st.dataframe(pd.DataFrame(complete_data), hide_index=True)

display_results()

st.subheader('Reference')
st.write('Xian-Kui Zhu, A comparative study of burst failure models for assessing remaining strength of corroded pipelines, Journal of Pipeline Science and Engineering 1 (2021) 36 - 50, https://doi.org/10.1016/j.jpse.2021.01.008')

st.subheader('Assesment')
st.markdown('[Case Study](https://drive.google.com/file/d/1Ako5uVRPYL5k5JeEQ_Xhl9f3pMRBjCJv/view?usp=sharing)', unsafe_allow_html=True)
st.markdown('[Corroded Pipe Burst Data](https://docs.google.com/spreadsheets/d/1YJ7ziuc_IhU7-MMZOnRmh4h21_gf6h5Z/edit?gid=56754844#gid=56754844)', unsafe_allow_html=True)
st.markdown('[Pre-Test](https://forms.gle/wPvcgnZAC57MkCxN8)', unsafe_allow_html=True)
st.markdown('[Post-Test](https://forms.gle/FdiKqpMLzw9ENscA9)', unsafe_allow_html=True)
