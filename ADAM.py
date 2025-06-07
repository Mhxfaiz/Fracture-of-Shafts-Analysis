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
htp="https://www.researchgate.net/profile/Changqing-Gong/publication/313456917/figure/fig1/AS:573308992266241@1513698923813/Schematic-illustration-of-the-geometry-of-a-typical-corrosion-defect.png"
st.image(htp, caption= "Fig. 1: Schematic illustration of the geometry of a typical corrosion defect.")

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
    minimum_stress = st.sidebar.number_input('Minimum Stress, Smin (MPa)', value = 0.01)
    maximum_stress = st.sidebar.number_input('Maximum Stress, Smax (MPa)', value = 0.01)
    
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
            'Smax (MPa)' : maximum_stress, }

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

st.subheader('Nomenclature')
st.write('P is the power, f is the rotation per second, d is the pipe diameter, HV is Vickers Hardness, Cload is the load factor, Csize is the size factor, Csurf is the surface factor, Ctemp is the temperature factor, creliab is the reliability factor, Kt is the stress concentration factor, r is the radius at the notch root, ρ is the characteristic length.')

# Calculate torsional loading T
T = P/(2*(22/7)*f)

# Calculate shear stress τ
τ = (16*T)/((22/7)*(math.pow(d, 3))

# Calculate uncorrected endurance strength Se
Se = (1.6*HV) + (0.1*HV)

# Calculate fatigue notch factor
Kf = 1 + ((Kt-1)/(1+m.sqrt(ρ/r)))

# Calculate notch correction factor
Cnotch = 1/Kf

# Calculate alternating stress
Smean = ((Smax - Smin)/2)

# Calculate mean stress
Smean = ((Smax + Smin)/2)

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
            'Smax (MPa)' : "{:.2f}".format (Smax), }

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
calculated_uncorrected_endurance_strength={'Se (MPa)': "{:.2f}".format(Se)}
calculated_uncorrected_endurance_strength_df=pd.DataFrame(calculated_uncorrected_endurance_strength, index=[0])
st.subheader('Calculated Uncorrected Endurance Strength')
st.write(calculated_uncorrected_endurance_strength_df)

calculated_param={'P_DnV (MPa)': "{:.2f}".format(P_DnV)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Corrorded Pipe Burst Pressure via DnV')
st.write(calculated_param_df)

calculated_param={'P_PCORRC (MPa)': "{:.2f}".format(P_PCORRC)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Corrorded Pipe Burst Pressure via PCORRC')
st.write(calculated_param_df)

Pressure = [Pvm, PTresca, P_ASME_B31G, P_DnV, P_PCORRC]
index = ["Pvm (MPa)", "PTresca (MPa)", "P_ASME_B31G (MPa)", "P_DnV (MPa)", "P_PCORRC (MPa)"]
df = pd.DataFrame({"Burst Pressure (MPa)": Pressure}, index=index)

# Principle stresses for Maximum Operating Pressure
P1max = Pop_Max*D/(2*P)
P2max = Pop_Max*D/(4*P)
P3max = 0

# Principle stresses for Minimum Operating Pressure
P1min = Pop_Min*D/(2*P)
P2min = Pop_Min*D/(4*P)
P3min = 0

# VM stress Max and Min Operating Pressure
Sigma_VM_Pipe_Max_Operating_Pressure = (1/m.sqrt(2))*((P1max-P2max)**2+(P2max-P3max)**2+(P3max-P1max)**2)**0.5

Sigma_VM_Pipe_Min_Operating_Pressure = 1/m.sqrt(2)*m.sqrt((P1min-P2min)**2+(P2min-P3min)**2+(P3min-P1min)**2)

calculated_param={'Sigma_VM_Pipe_Max_Operating_Pressure (MPa)': "{:.2f}".format(Sigma_VM_Pipe_Max_Operating_Pressure)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Von Mises stress of Maximum Operating Pressure')
st.write(calculated_param_df)

calculated_param={'Sigma_VM_Pipe_Min_Operating_Pressure (MPa)': "{:.2f}".format(Sigma_VM_Pipe_Min_Operating_Pressure)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Von Mises stress of Minimum Operating Pressure')
st.write(calculated_param_df)

Stresses = [Sigma_VM_Pipe_Max_Operating_Pressure, Sigma_VM_Pipe_Min_Operating_Pressure, Sy, UTS]
index = ["Svm_Max (MPa)", "Svm_Min (MPa)", "Yield Stress (MPa)", "UTS (MPa)"]
df = pd.DataFrame({"Stresses (MPa)": Stresses}, index=index)

st.subheader('Reference')
st.write('Xian-Kui Zhu, A comparative study of burst failure models for assessing remaining strength of corroded pipelines, Journal of Pipeline Science and Engineering 1 (2021) 36 - 50, https://doi.org/10.1016/j.jpse.2021.01.008')

st.subheader('Assesment')
st.markdown('[Case Study](https://drive.google.com/file/d/1Ako5uVRPYL5k5JeEQ_Xhl9f3pMRBjCJv/view?usp=sharing)', unsafe_allow_html=True)
st.markdown('[Corroded Pipe Burst Data](https://docs.google.com/spreadsheets/d/1YJ7ziuc_IhU7-MMZOnRmh4h21_gf6h5Z/edit?gid=56754844#gid=56754844)', unsafe_allow_html=True)
st.markdown('[Pre-Test](https://forms.gle/wPvcgnZAC57MkCxN8)', unsafe_allow_html=True)
st.markdown('[Post-Test](https://forms.gle/FdiKqpMLzw9ENscA9)', unsafe_allow_html=True)
