import streamlit as st
import pandas as pd
# from functions import *
from module import *
import matplotlib.pyplot as plt
from PIL import Image
# plt.style.use('science')
import io

# image1 = Image.open('cismid.jpg')
# st.image(image1)

# st.write('## Espectro de Diseño RNE-E.030 2020')

# image2 = Image.open('uni.jpg')
# st.sidebar.image(image2,width=150)

#Espectro de la norma de diseño Sismorresistente E030
periodo_P = {'S0':0.3,'S1':0.4,'S2':0.6,'S3':1.0,} #TP
periodo_L = {'S0':3.0,'S1':2.5,'S2':2.0,'S3':1.6,} #TL
suelo  = {'S0':{'Z4':0.8,'Z3':0.8,'Z2':0.8,'Z1':0.8,},
          'S1':{'Z4':1.0,'Z3':1.0,'Z2':1.0,'Z1':1.0,},
          'S2':{'Z4':1.05,'Z3':1.15,'Z2':1.20,'Z1':1.60,},
          'S3':{'Z4':1.10,'Z3':1.20,'Z2':1.40,'Z1':2.00,},}
zona = {'Z1':0.10,'Z2':0.25,'Z3':0.35,'Z4':0.45,}
red = {'Acero: Pórticos Especiales Resistentes a Momentos (SMF)':8,
      'Acero: Pórticos Intermedios Resistentes a Momentos (IMF)':5,
      'Acero: Pórticos Ordinarios Resistentes a Momentos (OMF)':4,
      'Acero: Pórticos Especiales Concéntricamente Arriostrados (SCBF)':7,
      'Acero: Pórticos Ordinarios Concéntricamente Arriostrados (OCBF)':4,
      'Acero: Pórticos Excéntricamente Arriostrados (EBF)':8,
      'Concreto Armado: Pórticos':8,
      'Concreto Armado: Dual':7,
      'Concreto Armado: De muros estructurales':6,
      'Concreto Armado: Muros de ductilidad limitada':4,
      'Albañilería armada o confinada':3,
      'Madera':7,} #coeficiente básico de reducción

irreA = {'Regular':1,
        'Irregularidad de Rigidez – Piso Blando':0.75,
        'Irregularidades de Resistencia – Piso Débil':0.75,
        'Irregularidad Extrema de Rigidez':0.50,
        'Irregularidad Extrema de Resistencia':0.50,
        'Irregularidad de Masa o Peso':0.9,
        'Irregularidad Geométrica Vertical':0.9,
        'Discontinuidad en los Sistemas Resistentes':0.8,
        'Discontinuidad extrema de los Sistemas Resistentes':0.6,} #Irregularidades en altura

irreP = {'Regular':1,
        'Irregularidad Torsional':0.75,
        'Irregularidad Torsional Extrema':0.6,
        'Esquinas Entrantes':0.9,
        'Discontinuidad del Diafragma':0.85,
        'Sistemas no Paralelos':0.9,} #Irregularidades en planta


with st.sidebar.container():
    st.write("# PARÁMETROS SÍSMICOS")
    col1, col2, col3 = st.columns(3)
    with col1:
        Z = st.selectbox('Zona',('Z1', 'Z2','Z3', 'Z4'),index=3)
    with col2:
        u = st.selectbox('Uso',(1, 1.3, 1.5),index=0)
    with col3:    
        S = st.selectbox('Suelo',('S0','S1','S2','S3'),index=0)
        
    st.write("# COEFICIENTE SÍSMICO DE REDUCCIÓN, R")
    red0 = st.selectbox('Coeficiente básico de reducción, R0',('Acero: Pórticos Especiales Resistentes a Momentos (SMF)',
      'Acero: Pórticos Intermedios Resistentes a Momentos (IMF)',
      'Acero: Pórticos Ordinarios Resistentes a Momentos (OMF)',
      'Acero: Pórticos Especiales Concéntricamente Arriostrados (SCBF)',
      'Acero: Pórticos Ordinarios Concéntricamente Arriostrados (OCBF)',
      'Acero: Pórticos Excéntricamente Arriostrados (EBF)',
      'Concreto Armado: Pórticos',
      'Concreto Armado: Dual',
      'Concreto Armado: De muros estructurales',
      'Concreto Armado: Muros de ductilidad limitada',
      'Albañilería armada o confinada',
      'Madera'),index=6)
    
    irrA = st.selectbox('Irregularidad en Altura, Ia',('Regular',
        'Irregularidad de Rigidez – Piso Blando',
        'Irregularidades de Resistencia – Piso Débil',
        'Irregularidad Extrema de Rigidez',
        'Irregularidad Extrema de Resistencia',
        'Irregularidad de Masa o Peso',
        'Irregularidad Geométrica Vertical',
        'Discontinuidad en los Sistemas Resistentes',
        'Discontinuidad extrema de los Sistemas Resistentes'),index=0)
    
    irrP = st.selectbox('Irregularidad en Planta, Ip',('Regular',
        'Irregularidad Torsional',
        'Irregularidad Torsional Extrema',
        'Esquinas Entrantes',
        'Discontinuidad del Diafragma',
        'Sistemas no Paralelos',),index=0)

s = suelo[S][Z]
z = zona[Z]
TP = periodo_P[S]
TL = periodo_L[S]
R0 = red[red0]
Ia = irreA[irrA]
Ip = irreP[irrP]

R = R0*Ia*Ip

with st.sidebar.container():
    st.write("Coeficiente sísmico de Reducción, R")
    st.write(f"R = {R}")

T = np.arange(0.0,10.01,0.025,dtype = 'double')
T[0] = 0.005
T = np.round(T,3)
C = np.zeros(T.shape[0])

ii = 0

for i1 in T:

    if i1 < 0.2*TP:
        C[ii] = 1+7.5*i1/TP
    elif 0.2*TP <= i1 <TP:
        C[ii] = 2.5
    elif TP <= i1 <TL:
        C[ii] = 2.5*TP/i1
    else:
        C[ii] = 2.5*TP*TL/i1**2
    ii += 1 

Sa_e030 = np.round(z*u*s*C*981/R,3) #gal

#Gráficos
fig1, ax1 = plt.subplots(1,1,constrained_layout=True,facecolor=(1, 1, 1, 1),figsize=(15,8))
c = st.container()

ax1.plot(T,Sa_e030, 'blue', linewidth=3,label='E030')
ax1.set_title('Espectro de Diseño RNE-E.030 2020', fontsize=40, fontweight = 'bold')
ax1.set_xlabel('$Periodo,$ $T(s)$', fontsize=25, fontweight = 'bold')
ax1.set_ylabel('$S_a (cm/s^2)$', fontsize=25, fontweight = 'bold')
ax1.set_xlim(0,10)
ax1.tick_params(labelsize=20)
# ax1.legend(loc='best', fontsize=15)
c.pyplot(fig1)

#Descargar archivo txt
name ='Espectro_E030'
resultados = np.transpose(np.append(T,Sa_e030).reshape(2,len(T)))
df = pd.DataFrame(resultados,columns=['T (s)','Sa (cm/s2)'])
df = df.set_index('T (s)')

csv = df.to_csv(sep = '\t').encode('utf-8')

st.download_button(label=f'Descargar {name}',data=csv,file_name='Espectro_E030.txt',mime='text/csv')

image1 = Image.open('imge030.jpg')
st.image(image1)

st.info('Elaborado por: Elvis Daniel Guizado Caceres')
st.info('Email: elvis.guizado.c@uni.pe')
st.info('Linkedin: linkedin.com/in/elvis-guizado-9233771b9')