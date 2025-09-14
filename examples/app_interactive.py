import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from semiconductor_sim.devices import LED, PNJunctionDiode

st.set_page_config(page_title="SemiconductorSim Demo", layout="wide")
st.title("SemiconductorSim Interactive Demo")
st.caption("Explore PN diode and LED behavior with interactive controls.")

tab_pn, tab_led = st.tabs(["PN Junction", "LED"])

with tab_pn:
    st.subheader("PN Junction Diode")
    col1, col2 = st.columns(2)
    with col1:
        doping_p = st.slider(
            "Acceptor doping p (cm^-3)",
            min_value=1e14,
            max_value=1e19,
            value=1e16,
            step=1e14,
            format="%.2e",
        )
        doping_n = st.slider(
            "Donor doping n (cm^-3)",
            min_value=1e14,
            max_value=1e19,
            value=1e16,
            step=1e14,
            format="%.2e",
        )
        area = st.slider(
            "Area (cm^2)", min_value=1e-6, max_value=1e-2, value=1e-4, step=1e-6, format="%.1e"
        )
        temperature = st.slider("Temperature (K)", min_value=250, max_value=400, value=300, step=5)
    with col2:
        v_min, v_max = st.slider(
            "Voltage range (V)", min_value=-0.5, max_value=1.0, value=(-0.2, 0.8), step=0.01
        )
        points = st.slider("Points", min_value=50, max_value=500, value=200, step=10)
        include_recomb = st.checkbox("Include SRH recombination input", value=True)
        n_const = (
            st.number_input("n concentration (cm^-3)", value=1e15, format="%.2e")
            if include_recomb
            else None
        )
        p_const = (
            st.number_input("p concentration (cm^-3)", value=1e15, format="%.2e")
            if include_recomb
            else None
        )

    pn = PNJunctionDiode(
        doping_p=doping_p, doping_n=doping_n, area=area, temperature=float(temperature)
    )
    V = np.linspace(v_min, v_max, int(points))
    if include_recomb and n_const is not None and p_const is not None:
        n_arr = np.full_like(V, float(n_const))
        p_arr = np.full_like(V, float(p_const))
        I, R = pn.iv_characteristic(V, n_arr, p_arr)
    else:
        I, R = pn.iv_characteristic(V)

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, subplot_titles=("IV Characteristic", "SRH Recombination")
    )
    fig.add_trace(go.Scatter(x=V, y=I, mode="lines", name="Current I"), row=1, col=1)
    fig.add_trace(
        go.Scatter(x=V, y=R, mode="lines", name="R_SRH", line=dict(dash="dash")), row=2, col=1
    )
    fig.update_xaxes(title_text="Voltage (V)", row=2, col=1)
    fig.update_yaxes(title_text="Current (A)", row=1, col=1)
    fig.update_yaxes(title_text="Recomb (cm^-3 s^-1)", row=2, col=1)
    fig.update_layout(height=700)
    st.plotly_chart(fig, use_container_width=True)

with tab_led:
    st.subheader("LED")
    col1, col2 = st.columns(2)
    with col1:
        doping_p = st.slider(
            "Acceptor doping p (cm^-3)",
            min_value=1e14,
            max_value=1e19,
            value=1e17,
            step=1e14,
            format="%.2e",
            key="led_dp",
        )
        doping_n = st.slider(
            "Donor doping n (cm^-3)",
            min_value=1e14,
            max_value=1e19,
            value=1e17,
            step=1e14,
            format="%.2e",
            key="led_dn",
        )
        efficiency = st.slider(
            "Radiative efficiency", min_value=0.0, max_value=1.0, value=0.2, step=0.01
        )
        temperature = st.slider(
            "Temperature (K)", min_value=250, max_value=400, value=300, step=5, key="led_T"
        )
    with col2:
        v_min, v_max = st.slider(
            "Voltage range (V)",
            min_value=0.0,
            max_value=3.0,
            value=(0.0, 2.0),
            step=0.01,
            key="led_Vrng",
        )
        points = st.slider("Points", min_value=50, max_value=500, value=200, step=10, key="led_pts")
        include_recomb = st.checkbox("Include recombination inputs", value=True, key="led_inc_rec")
        n_const = (
            st.number_input("n concentration (cm^-3)", value=1e16, format="%.2e", key="led_n")
            if include_recomb
            else None
        )
        p_const = (
            st.number_input("p concentration (cm^-3)", value=1e16, format="%.2e", key="led_p")
            if include_recomb
            else None
        )

    led = LED(
        doping_p=doping_p, doping_n=doping_n, efficiency=efficiency, temperature=float(temperature)
    )
    V = np.linspace(v_min, v_max, int(points))
    if include_recomb and n_const is not None and p_const is not None:
        n_arr = np.full_like(V, float(n_const))
        p_arr = np.full_like(V, float(p_const))
        I, Em, R = led.iv_characteristic(V, n_arr, p_arr)
    else:
        I, Em = led.iv_characteristic(V)
        R = np.zeros_like(V)

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        subplot_titles=("IV Characteristic", "Emission & Recombination"),
    )
    fig.add_trace(go.Scatter(x=V, y=I, mode="lines", name="Current I"), row=1, col=1)
    fig.add_trace(
        go.Scatter(x=V, y=Em, mode="lines", name="Emission", line=dict(dash="dot", color="red")),
        row=2,
        col=1,
    )
    if R is not None:
        fig.add_trace(
            go.Scatter(x=V, y=R, mode="lines", name="R_SRH", line=dict(dash="dash", color="green")),
            row=2,
            col=1,
        )
    fig.update_xaxes(title_text="Voltage (V)", row=2, col=1)
    fig.update_yaxes(title_text="Current (A)", row=1, col=1)
    fig.update_yaxes(title_text="Emission (arb) / Recomb", row=2, col=1)
    fig.update_layout(height=700)
    st.plotly_chart(fig, use_container_width=True)
