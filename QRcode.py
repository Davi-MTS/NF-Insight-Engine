import streamlit as st
import cv2
import numpy as np
from PIL import Image
from datetime import datetime
from supabase import create_client, Client
import pandas as pd
import re

# =========================
# CONFIGURAÇÕES INICIAIS
# =========================
st.set_page_config(page_title="Leitor de QR Code - NFC-e", layout="wide")

# =========================
# SUPABASE CONFIGURAÇÃO
# =========================
SUPABASE_URL = "https://ybgbyrjbczftmcuyxrvi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InliZ2J5cmpiY3pmdG1jdXl4cnZpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEwNTc5NzYsImV4cCI6MjA3NjYzMzk3Nn0.3g8UnQNsiEjwgvGtgdH2NRUoYCH09CMM2l3X2o2hlBw"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("❌ Erro ao conectar ao Supabase.")

# =========================
# FUNÇÕES AUXILIARES
# =========================
def extract_chave_acesso(text: str) -> str:
    """Extrai a chave de 44 dígitos do QR Code"""
    match = re.search(r"\b\d{44}\b", text)
    return match.group(0) if match else None

def decode_qrcode(image: Image.Image) -> str:
    """Lê QR Code usando OpenCV (funciona na nuvem)"""
    img_array = np.array(image.convert("RGB"))
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img_cv)
    return data.strip() if data else None

def save_chave_supabase(chave: str, origem: str) -> bool:
    """Salva a chave no Supabase se ainda não existir"""
    try:
        # Checa duplicidade real
        existing = supabase.table("qrcodes").select("chave").eq("chave", chave).execute()
        if existing.data:
            return False  # Já existe

        # Insere nova chave
        supabase.table("qrcodes").insert({
            "chave": chave,
            "origem": origem,
            "datahora": datetime.now().isoformat()
        }).execute()
        return True
    except:
        return False

def get_historico() -> pd.DataFrame:
    """Retorna todas as chaves salvas no Supabase"""
    try:
        response = supabase.table("qrcodes").select("*").order("datahora", desc=True).execute()
        if response.data:
            return pd.DataFrame(response.data)
        return pd.DataFrame(columns=["chave", "origem", "datahora"])
    except:
        return pd.DataFrame(columns=["chave", "origem", "datahora"])

# =========================
# INTERFACE PRINCIPAL
# =========================
st.title("📷 Leitor de QR Code de Nota Fiscal (NFC-e)")

tab1, tab2 = st.tabs(["📸 Tirar Foto", "🖼 Upload de imagem"])

# -------------------------
# TAB 1: Tirar Foto
# -------------------------
with tab1:
    st.write("📸 Tire uma foto do QR Code da nota fiscal usando a câmera do seu celular ou notebook.")
    photo = st.camera_input("Tire uma foto do QR Code")

    if photo:
        img = Image.open(photo)
        data = decode_qrcode(img)
        if not data:
            st.warning("Nenhum QR Code encontrado na imagem.")
        else:
            chave = extract_chave_acesso(data)
            if chave:
                if save_chave_supabase(chave, "Foto"):
                    st.success(f"✅ Chave salva: {chave}")
                else:
                    st.info(f"⚠ Chave já existente: {chave}")
            else:
                st.error("❌ Nenhuma chave válida (44 dígitos) foi encontrada.")

# -------------------------
# TAB 2: Upload de Imagem
# -------------------------
with tab2:
    file = st.file_uploader("Selecione uma imagem de nota fiscal (JPG, PNG)...", type=["jpg", "jpeg", "png"])

    if file:
        img = Image.open(file)
        data = decode_qrcode(img)
        if not data:
            st.warning("Nenhum QR Code encontrado na imagem.")
        else:
            chave = extract_chave_acesso(data)
            if chave:
                if save_chave_supabase(chave, "Upload"):
                    st.success(f"✅ Chave salva: {chave}")
                else:
                    st.info(f"⚠ Chave já existente: {chave}")
            else:
                st.error("❌ Nenhuma chave válida (44 dígitos) foi encontrada.")

# -------------------------
# HISTÓRICO
# -------------------------
st.markdown("---")
st.subheader("📋 Chaves de Acesso Salvas")
df = get_historico()

if not df.empty:
    st.dataframe(df.sort_values(by="datahora", ascending=False), width="stretch")

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("⬇ Baixar CSV", df.to_csv(index=False), "qrcodes.csv", "text/csv")
    with col2:
        if st.button("🗑 Limpar histórico"):
            try:
                supabase.table("qrcodes").delete().neq("id", 0).execute()
                st.warning("Histórico apagado com sucesso!")
            except:
                st.error("Erro ao limpar histórico.")
else:
    st.info("Nenhuma chave registrada até o momento.")
