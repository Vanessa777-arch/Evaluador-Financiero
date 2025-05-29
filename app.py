import streamlit as st
import pandas as pd
import numpy_financial as npf

st.set_page_config(page_title="Evaluador Financiero", layout="centered")

st.title("📊 Evaluador Financiero de Proyectos")
st.markdown("Sube un archivo Excel con la inversión inicial y flujos de caja.")

uploaded_file = st.file_uploader("📁 Sube tu archivo Excel", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        st.subheader("👀 Vista previa de los datos")
        st.write(df)

        inversion = df.iloc[0, 0]
        flujos = df.iloc[0, 1:].astype(float).values
        tasa_descuento = st.number_input("🔻 Ingresa la tasa de descuento (%)", min_value=0.0, max_value=1.0, value=0.1)

        flujos_completos = [inversion] + list(flujos)

        van = npf.npv(tasa_descuento, flujos_completos)
        tir = npf.irr(flujos_completos)
        roi = (sum(flujos) + inversion) / abs(inversion)

        acumulado = 0
        payback = None
        for i, flujo in enumerate(flujos, start=1):
            acumulado += flujo
            if acumulado + inversion >= 0:
                payback = i
                break

        st.subheader("💥 Resultados financieros")
        st.success(f"✅ VAN: ${van:,.2f}")
        st.info(f"📈 TIR: {tir * 100:.2f}%")
        st.info(f"💰 ROI: {roi * 100:.2f}%")
        if payback:
            st.info(f"📆 PAYBACK: {payback} años")
        else:
            st.warning("⚠️ PAYBACK: No se recupera en el período indicado.")

    except Exception as e:
        st.error("❌ Error al procesar los datos. Verifica el formato del Excel.")
        st.exception(e)
else:
    st.info("👉 Sube tu archivo Excel para comenzar.")
