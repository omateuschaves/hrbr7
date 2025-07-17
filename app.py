
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Controle de Jornada", layout="wide")
st.title("📋 Controle de Jornada dos Motoristas")

def calc_dif(h1, h2):
    try:
        t1 = datetime.strptime(str(h1), "%H:%M")
        t2 = datetime.strptime(str(h2), "%H:%M")
        return (t2 - t1).total_seconds() / 60
    except:
        return None

arquivo = st.file_uploader("📤 Envie a planilha (.xlsx) com os dados", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)

    df["Dif. Entrada (min)"] = df.apply(lambda row: calc_dif(row["Entrada Programada"], row["Entrada Real"]), axis=1)
    df["Dif. Saída (min)"] = df.apply(lambda row: calc_dif(row["Saída Programada"], row["Saída Real"]), axis=1)
    df["Duração Refeição Programada (min)"] = df.apply(lambda row: calc_dif(row["Refeição Programada Início"], row["Refeição Programada Fim"]), axis=1)
    df["Duração Refeição Real (min)"] = df.apply(lambda row: calc_dif(row["Refeição Real Início"], row["Refeição Real Fim"]), axis=1)
    df["Dif. Duração Refeição (min)"] = df["Duração Refeição Real (min)"] - df["Duração Refeição Programada (min)"]

    st.success("✅ Dados carregados e calculados com sucesso!")
    st.dataframe(df, use_container_width=True)

    if st.button("📥 Baixar resultado com cálculos"):
        df.to_excel("resultado_jornada.xlsx", index=False)
        with open("resultado_jornada.xlsx", "rb") as file:
            st.download_button("Clique para baixar", file, file_name="resultado_jornada.xlsx")

else:
    st.info("💡 A planilha deve conter os seguintes campos:\n\n"
            "- Entrada Programada\n"
            "- Entrada Real\n"
            "- Refeição Programada Início\n"
            "- Refeição Programada Fim\n"
            "- Refeição Real Início\n"
            "- Refeição Real Fim\n"
            "- Saída Programada\n"
            "- Saída Real\n\n"
            "Os horários devem estar no formato **HH:MM**.")
