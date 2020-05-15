import numpy as np
import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.palettes import Colorblind

TOOLS="hover,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,reset,save,"

temp_vet = [i for i in range(295, 1000)]
T_targets = st.multiselect('Temperature of the Target', temp_vet)

T_ref = float(st.sidebar.text_input('Temp reference', 300))
P_ratio = float(st.sidebar.text_input('Power Ratio', 2))
P_target = float(st.sidebar.text_input('Power Target', 2.8))
sigma =  float(st.sidebar.text_input('Sigma', 5))
mu =  float(st.sidebar.text_input('Mean', 633))
l_laser = float(st.sidebar.text_input('Laser wavelength', 633))
scelta = st.sidebar.radio('switch',('on','off'))

c = 299792458
w_laser = c/(l_laser*1e-9)
if scelta == 'off':
    w_laser = 0
    st.latex(r'''{I_1} =  \frac{P_1}{{\left(e^{\frac{\hbar c}{k_b T_1} \left(\frac{1}{\lambda} \right)} - 1 \right)}}''')
elif scelta == 'on':
    st.latex(r'''{I_1} =  \frac{P_1}{{\left(e^{\frac{\hbar c}{k_b T_1} \left(\frac{1}{\lambda} - \frac{1}{\lambda_{laser}} \right)} - 1 \right)}}''')

p = figure(title='', x_axis_label='x', y_axis_label='y', tools = TOOLS)
p2 = figure(title='', x_axis_label='x', y_axis_label='y', tools = TOOLS)
p3 = figure(title='', x_axis_label='x', y_axis_label='y', tools = TOOLS)
p4 = figure(title='', x_axis_label='x', y_axis_label='y', tools = TOOLS)

if T_targets:
    x = np.linspace(int(l_laser)-70, int(l_laser) - 5, 130).tolist() + np.linspace(int(l_laser) + 5, int(l_laser) + 70, 130).tolist()
    y_PL_ratio = pd.DataFrame()

    for j, T_target in enumerate(T_targets):
        def funzione_ratio(x):
            h_bar = 4.1356*1e-15
            kb = 8.617*1e-5
            w = c/(x*1e-9)

            numeratore   = np.exp((h_bar/(kb*T_ref))   *(w - w_laser)) - 1
            denominatore = np.exp((h_bar/(kb*T_target))*(w - w_laser)) - 1
            return P_ratio*numeratore/denominatore

        def funzione_PL(x):
            h_bar = 4.1356*1e-15
            kb = 8.617*1e-5
            w = c/(x*1e-9)

            denominatore = np.exp((h_bar/(kb*T_target))*(w - w_laser)) - 1
            return P_target/denominatore

        def funzione_resonance(x):
            return np.exp(-(1/2)*((x-mu)/sigma)*((x-mu)/sigma))

        y_ration = np.array(list(map(funzione_ratio,x)))
        y_resonance = np.array(list(map(funzione_resonance,x)))
        y_PL = np.array(list(map(funzione_PL,x)))
        y_real = y_resonance*y_PL

        y_PL_ratio[T_target] = y_PL

        p.scatter(x, y_ration, legend=str(T_target), line_width=2, color = Colorblind[8][j])
        p.line((l_laser,l_laser), (y_ration.min(),y_ration.max()), line_width=0.5, color = 'red')

        p2.scatter(x, y_PL, legend=str(T_target), line_width=2, color = Colorblind[8][j])
        p2.line((l_laser,l_laser), (y_PL.min(),y_PL.max()), line_width=0.5, color = 'red')

        p3.scatter(x, y_resonance, legend=str(T_target), line_width=2, color = Colorblind[8][j])
        p3.line((l_laser,l_laser), (y_resonance.min(),y_resonance.max()), line_width=0.5, color = 'red')

        p4.scatter(x, y_real, legend=str(T_target), line_width=2, color = Colorblind[8][j])
        p4.line((l_laser,l_laser), (y_real.min(),y_real.max()), line_width=0.5, color = 'red')

    st.subheader('Ratio')
    st.bokeh_chart(p, use_container_width=True)
    st.subheader('PL')
    st.bokeh_chart(p2, use_container_width=True)
    st.subheader('Resonance')
    st.bokeh_chart(p3, use_container_width=True)
    st.subheader('Real')
    st.bokeh_chart(p4, use_container_width=True)


    # y_PL_ratio['diff'] =y_PL_ratio[T_targets[1]]/y_PL_ratio[T_targets[0]]
    # st.write(y_PL_ratio)
    # ds().nuova_fig(5)
    # ds().dati(x, y_PL_ratio['diff'].to_numpy())
    # st.pyplot()
