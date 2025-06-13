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

# Torsional Loading
calculated_torsional_loading={'T (Nm)': "{:.2f}".format(T)}
calculated_torsional_loading_df=pd.DataFrame(calculated_torsional_loading, index=[0])
st.subheader('Calculated Torsional Loading')
st.write(calculated_torsional_loading_df)

# Shear Stress
calculated_shear_stress={'τ (Pa)': "{:.2f}".format(τ)}
calculated_shear_stress_df=pd.DataFrame(calculated_shear_stress, index=[0])
st.subheader('Calculated Shear Stress')
st.write(calculated_shear_stress_df)

# Uncorrected Endurance Strength
calculated_uncorrected_endurance_strength={'Sue (MPa)': "{:.2f}".format(Sue)}
calculated_uncorrected_endurance_strength_df=pd.DataFrame(calculated_uncorrected_endurance_strength, index=[0])
st.subheader('Calculated Uncorrected Endurance Strength')
st.write(calculated_uncorrected_endurance_strength_df)

# Fatigue Notch Factor
calculated_fatigue_notch_factor={'Kf': "{:.2f}".format(Kf)}
calculated_fatigue_notch_factor_df=pd.DataFrame(calculated_fatigue_notch_factor, index=[0])
st.subheader('Calculated Fatigue Notch Factor')
st.write(calculated_fatigue_notch_factor_df)

# Notch Factor Correction
calculated_notch_factor_correction={'Cnotch': "{:.2f}".format(Cnotch)}
calculated_notch_factor_correction_df=pd.DataFrame(calculated_notch_factor_correction, index=[0])
st.subheader('Calculated Notch Factor Correction')
st.write(calculated_notch_factor_correction_df)

# Corrected Endurance Factor
calculated_corrected_endurance_factor={'Se (MPa)' : "{:.2f}".format(Se)}
calculated_corrected_endurance_factor_df=pd.DataFrame(calculated_corrected_endurance_factor, index=[0])
st.subheader('Calculated Corrected Endurance Factor')
st.write(calculated_corrected_endurance_factor_df)

# Alternating Stress
calculated_alternating_stress={'Sa (MPa)' : "{:.2f}".format(Sa)}
calculated_alternating_stress_df=pd.DataFrame(calculated_alternating_stress, index=[0])
st.subheader('Calculated Alternating Stress')
st.write(calculated_alternating_stress_df)

# Mean Stress
calculated_mean_stress={'Smean (MPa)' : "{:.2f}".format(Smean)}
calculated_mean_stress_df=pd.DataFrame(calculated_mean_stress, index=[0])
st.subheader('Calculated Mean Stress')
st.write(calculated_mean_stress_df)

# Fatigue Stress
calculated_fatigue_stress={'Sf (MPa)' :  "{:.2f}".format(Sf)}
calculated_fatigue_stress_df=pd.DataFrame(calculated_fatigue_stress, index=[0])
st.subheader('Calculated Fatigue Stress')
st.write(calculated_fatigue_stress_df)

# goodman_plot.py

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_goodman_plot(Sf, Su, Se, Smean, Sa):
    sns.set(style="whitegrid")
    fig, ax = plt.subplots()

    # Goodman Line
    ax.plot([0, Su], [Se, 0], label="Goodman Line", color='blue')

    # Soderberg Line
    ax.plot([0, Sf], [Su, 0], label="Soderberg Line", color='green', linestyle='--')

    # Gerber Curve
    sigma_m_vals = np.linspace(0, Su, 100)
    gerber_curve = Se * (1 - (sigma_m_vals / Su)**2)
    ax.plot(sigma_m_vals, gerber_curve, label="Gerber Curve", color='orange', linestyle='-.')

    # User Point
    ax.plot(Su, Sf, 'ro', label='User Input Point')

    ax.set_xlabel("Mean Stress σm (MPa)")
    ax.set_ylabel("Alternating Stress σa (MPa)")
    ax.set_title("Fatigue Failure Criteria")
    ax.legend()
    ax.grid(True)
    ax.set_xlim(0, max(Su, Sf) * 1.1)
    ax.set_ylim(0, max(Se, Su) * 1.1)

    return fig

st.subheader('Reference')
st.write('Xian-Kui Zhu, A comparative study of burst failure models for assessing remaining strength of corroded pipelines, Journal of Pipeline Science and Engineering 1 (2021) 36 - 50, https://doi.org/10.1016/j.jpse.2021.01.008')

st.subheader('Assesment')
st.markdown('[Case Study](https://drive.google.com/file/d/1Ako5uVRPYL5k5JeEQ_Xhl9f3pMRBjCJv/view?usp=sharing)', unsafe_allow_html=True)
st.markdown('[Corroded Pipe Burst Data](https://docs.google.com/spreadsheets/d/1YJ7ziuc_IhU7-MMZOnRmh4h21_gf6h5Z/edit?gid=56754844#gid=56754844)', unsafe_allow_html=True)
st.markdown('[Pre-Test](https://forms.gle/wPvcgnZAC57MkCxN8)', unsafe_allow_html=True)
st.markdown('[Post-Test](https://forms.gle/FdiKqpMLzw9ENscA9)', unsafe_allow_html=True)
