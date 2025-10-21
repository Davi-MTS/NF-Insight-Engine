import streamlit as st
from pyzbar import pyzbar
from PIL import Image
import pandas as pd
import os
import re
from datetime import datetime

# =========================
# CONFIGURAÇÕES INICIAIS
# =========================
st.set_page_config(page_title="Leitor de QR Code - NFC-e", layout="wide")
CSV_FILE = "qrcodes.csv"

# =========================
# FUNÇÕES AUXILIARES CSV
# =========================
def garantir_csv():
    colunas = ["Chave de Acesso", "Data e Hora", "Origem"]
    if not os.path.exists(CSV_FILE):
        pd.DataFrame(columns=colunas).to_csv(CSV_FILE, index=False)
    else:
        try:
            df = pd.read_csv(CSV_FILE)
            if list(df.columns) != colunas:
                pd.DataFrame(columns=colunas).to_csv(CSV_FILE, index=False)
        except Exception:
            pd.DataFrame(columns=colunas).to_csv(CSV_FILE, index=False)

def extract_chave_acesso(text):
    match = re.search(r"\b\d{44}\b", text)
    if match:
        return match.group(0)
    return None

def save_chave(chave, origem):
    garantir_csv()
    df = pd.read_csv(CSV_FILE)
    if chave not in df["Chave de Acesso"].values:
        novo = pd.DataFrame([[chave, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), origem]],
                            columns=["Chave de Acesso", "Data e Hora", "Origem"])
        df = pd.concat([df, novo], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        return True
    return False

garantir_csv()

# =========================
# INTERFACE PRINCIPAL
# =========================
st.title("📷 Leitor de QR Code de Nota Fiscal (NFC-e)")

tab1, tab2 = st.tabs(["📸 Tirar Foto", "🖼️ Upload de imagem"])

# =========================
# TIRAR FOTO
# =========================
with tab1:
    st.write("📸 Tire uma foto do QR Code da nota fiscal usando a câmera do seu celular ou notebook.")
    
    photo = st.camera_input("Tire uma foto do QR Code")

    if photo:
        img = Image.open(photo).convert("RGB")
        decoded = pyzbar.decode(img)
        if not decoded:
            st.warning("Nenhum QR Code encontrado na imagem.")
        else:
            for obj in decoded:
                data = obj.data.decode("utf-8")
                chave = extract_chave_acesso(data)
                if chave:
                    if save_chave(chave, "Foto"):
                        st.success(f"✅ Chave salva: {chave}")
                    else:
                        st.info(f"⚠️ Chave já existente: {chave}")
                else:
                    st.error("❌ Nenhuma chave válida (44 dígitos) foi encontrada.")

# =========================
# UPLOAD DE IMAGEM
# =========================
with tab2:
    file = st.file_uploader("Selecione uma imagem de nota fiscal (JPG, PNG)...", type=["jpg", "jpeg", "png"])
    if file:
        img = Image.open(file).convert("RGB")
        decoded = pyzbar.decode(img)
        if not decoded:
            st.warning("Nenhum QR Code encontrado na imagem.")
        else:
            for obj in decoded:
                data = obj.data.decode("utf-8")
                chave = extract_chave_acesso(data)
                if chave:
                    if save_chave(chave, "Upload"):
                        st.success(f"✅ Chave salva: {chave}")
                    else:
                        st.info(f"⚠️ Chave já existente: {chave}")
                else:
                    st.error("❌ Nenhuma chave válida (44 dígitos) foi encontrada.")

# =========================
# HISTÓRICO DE CHAVES
# =========================
st.markdown("---")
st.subheader("📋 Chaves de Acesso Salvas")
df = pd.read_csv(CSV_FILE)
st.dataframe(df.sort_values(by="Data e Hora", ascending=False), width="stretch")

col1, col2 = st.columns(2)
with col1:
    st.download_button("⬇️ Baixar CSV", df.to_csv(index=False), "qrcodes.csv", "text/csv")
with col2:
    if st.button("🗑️ Limpar histórico"):
        os.remove(CSV_FILE)
        pd.DataFrame(columns=["Chave de Acesso", "Data e Hora", "Origem"]).to_csv(CSV_FILE, index=False)
        st.warning("Histórico apagado com sucesso!")