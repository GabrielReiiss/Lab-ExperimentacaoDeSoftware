import streamlit as st

from dashboard.data import list_snapshots, load_snapshot


def render():
    st.title("Snapshots de Sprint")

    arquivos = list_snapshots()

    if not arquivos:
        st.info(
            "Nenhum snapshot encontrado em data/snapshots/. Gere um rodando, no "
            "terminal: python -m scripts.snapshot_project --sprint S01"
        )
        return

    nomes_sprint = [arquivo.stem.replace("snapshot_", "") for arquivo in arquivos]
    abas = st.tabs(nomes_sprint)

    for aba, arquivo in zip(abas, arquivos):
        with aba:
            df = load_snapshot(arquivo)
            st.caption(f"{len(df)} itens no board, arquivo {arquivo.name}")

            contagem_status = df["status"].value_counts()
            st.bar_chart(contagem_status)

            st.dataframe(df, width="stretch", hide_index=True)
