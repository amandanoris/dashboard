import pandas as pd
from pathlib import Path
from models import Thesis
import streamlit as st

st.set_page_config(page_title="MatCom Dashboard - Tesis", page_icon="🎓", layout="wide")


listing, create = st.tabs(["📃 Listado", "➕ Crear nueva Tesis"])


with listing:
    theses = []

    for path in Path("/src/data/Thesis/").rglob("*.yaml"):
        with open(path) as fp:
            theses.append(Thesis.load(fp))

    st.write("##### 📃 Listado de Tesis")
    data = pd.DataFrame([thesis.encode() for thesis in theses])
    st.dataframe(data)


def save_thesis(thesis):
    thesis.save()
    st.session_state.thesis_title = ""
    st.session_state.thesis_authors = ""
    st.session_state.thesis_advisors = ""
    st.session_state.thesis_keywords = ""

    st.success(f"¡Tesis _{thesis.title}_ creada con éxito!")


with create:
    left, right = st.columns([2, 1])

    with left:
        title = st.text_input("Título", key="thesis_title")
        authors = [
            s.strip()
            for s in st.text_area(
                "Autores (uno por línea)", key="thesis_authors"
            ).split("\n")
        ]
        advisors = [
            s.strip()
            for s in st.text_area(
                "Tutores (uno por línea)", key="thesis_advisors"
            ).split("\n")
        ]
        keywords = [
            s.strip()
            for s in st.text_input(
                "Palabras clave (separadas por ;)", key="thesis_keywords"
            ).split(";")
        ]

    with right:
        thesis = Thesis(
            title=title,
            authors=[a for a in authors if a],
            advisors=[a for a in advisors if a],
            keywords=[k for k in keywords if k],
        )

        try:
            thesis.validate()
            st.button("➕ Crear nueva Tesis", on_click=save_thesis, args=(thesis,))
        except ValueError as e:
            st.error(e)

        st.code(thesis.yaml(), "yaml")
