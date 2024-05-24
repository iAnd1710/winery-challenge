import streamlit as st
import polars as pl
import plotly.express as px
from . import visualization
from . import layout
import pandas as pd

def l_visual_two_bar(df: pd.DataFrame) -> None:
    
    config_graph = {}
    cols = st.columns([2, 1], gap="large")
    with cols[1]:
        with st.expander("⚙️ Configuração do Gráfico", expanded=False):
            decade = st.checkbox("Agrupar por Década", key="decade_visual_two_bar")
        
        config_graph["decade"] = decade
        
        # Assuming l_description is a custom function for displaying descriptions
        l_description(
            "Texto de análise"      
        )
            
    with cols[0]:
        
        fig = visualization.visual_two_bar(df, config_graph)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.markdown("<div style='margin-bottom: 30px'></div>", unsafe_allow_html=True)

    return None

def l_visual_three_bar(df: pd.DataFrame) -> None:
    
    config_graph = {}
    cols = st.columns([2, 1], gap="large")
    
    with cols[1]:
        with st.expander("⚙️ Configuração do Gráfico", expanded=False):
            metric = st.selectbox(
                "Métrica",
                ("Valor Exportado", "Litros Exportados"),
                key="metric_visual_three_bar",
            )
            agg = st.selectbox(
                "Visualização", ("Valor Total", "Valor Médio"),
                key="agg_visual_three_bar",
            )
        
        config_graph["metric"] = metric
        config_graph["agg"] = agg
        
        l_description(
            "Texto de análise"      
        )
        
    with cols[0]:
        
        fig = visualization.visual_three_bar(df, config_graph)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.markdown("<div style='margin-bottom: 30px'></div>", unsafe_allow_html=True)

    return None

def l_visual_four_map(df: pd.DataFrame) -> None:
    
    config_graph = {}
    cols = st.columns([2, 1], gap="large")
    
    with cols[1]:
        with st.expander("⚙️ Configuração do Gráfico", expanded=False):
            year = st.slider(
                "Período", 1970, 2022, (1970, 2022),
                key="year_visual_four_map"
            )
            metric = st.selectbox(
                "Métrica",
                ("Valor Exportado", "Litros Exportados"),
                key="metric_visual_four_map",
            )
            agg = st.selectbox(
                "Visualização",
                ("Valor Total", "Valor Médio"),
                key="agg_visual_four_map",
            )
        
        config_graph["metric"] = metric
        config_graph["agg"] = agg
        config_graph["year"] = year

        l_description(
            "Texto de análise"      
        )
            
    with cols[0]:
        
        fig = visualization.visual_four_map(df, config_graph)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.markdown("<div style='margin-bottom: 30px'></div>", unsafe_allow_html=True)

    return None

def l_visual_five_map(df: pd.DataFrame) -> None:
    
    config_graph = {}
    cols = st.columns([2, 1], gap="large")
    
    with cols[1]:
        with st.expander("⚙️ Configuração do Gráfico", expanded=False):
            metric = st.selectbox(
                "Métrica",
                ("Valor Exportado", "Litros Exportados"),
                key="metric_visual_five_map",
            )
            viz = st.selectbox("Visualização", ("Top 5 Países", "Customizar"), key="viz_visual_five_map")
            
            var = {"Valor Exportado": "value", "Litros Exportados": "liters"}
            col_name = var[metric]
            
            if viz == "Customizar":
                list_name = (
                    df.groupby("country")
                    .agg({col_name: "sum"})
                    .reset_index()
                    .sort_values(by=col_name, ascending=False)
                    .loc[:, "country"]
                    .tolist()
                )
                config_graph['list_selected'] = st.multiselect("Paises selecionados", list_name)
            
        
        config_graph["metric"] = metric
        config_graph["viz"] = viz
        config_graph["col_name"] = col_name
        
        l_description(
            "Texto de análise"      
        )
            
    with cols[0]:
        
        fig = visualization.visual_five_map(df, config_graph)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.markdown("<div style='margin-bottom: 30px'></div>", unsafe_allow_html=True)

    return None

def l_visual_six_bar(df: pd.DataFrame) -> None:
    
    config_graph = {}
    cols = st.columns([2, 1], gap="large")
    
    with cols[1]:
        with st.expander("⚙️ Configuração do Gráfico", expanded=False):
            median_region = st.checkbox("Ver Preço mediano total por Região", key="median_region_visual_six_bar")
        
        config_graph["median_region"] = median_region
        
        l_description(
            "Texto de análise"      
        )
            
    with cols[0]:
        
        fig = visualization.visual_six_bar(df, config_graph)
        st.plotly_chart(fig, use_container_width=True)

    return None

def l_description(text: str) -> None:
    st.markdown(
        f"""
        <div style="background: #f8f8f8; padding: 20px 25px 10px 20px; border-radius: 5px; border: 1px solid #ddd; margin-bottom: 100px">
            <p style="text-align: left; font-size:13px; color: #bbb">
                Análise
            </p>
            <p style="text-align: left;">
                {text}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return None

def header() -> None:
    st.markdown("# :violet[The Winery] Challenge")
    st.markdown(
        """
        **Fonte de Dados:** [**Dados da Vitivinicultura**](http://vitibrasil.cnpuv.embrapa.br/)
        """
    )
    
    with st.expander("↓ Download dos Arquivos", expanded=False):
            
        with open('./data/dataframe_final.csv', 'rb') as file:
            btn = st.download_button(
                label="💿 Baixar CSV completo",
                data=file,
                file_name="data.csv",
                mime='text/csv',
                type='primary',
                key="download_csv"
            )
            
    st.markdown("<div style='margin-bottom: 40px'></div>", unsafe_allow_html=True)

    return None

def tab_intro(df: pd.DataFrame) -> None:
    
    cols1, cols2 = st.columns([2, 2])
    with cols1:
        st.markdown(
        """
        Coluna 1
        """
    )

    with cols2:
        st.plotly_chart(visualization.visual_globe(df), use_container_width=True)

    st.markdown(
        """
        ###### Tabela com informações sobre a exportação de vinho
        Tabela contendo as informações solicitadas sobre a exportação de vinho, como país de origem, país de destino, ano de referência, quantidade de vinho exportado (em litros) e valor total exportado (em US$)
        """
    )
    st.dataframe(visualization.table_info(df), use_container_width=True)
    st.dataframe(visualization.table_info_top(df), use_container_width=True)


    return None

def tab_tabela(df: pd.DataFrame) -> None:
    df = pl.from_pandas(df)
    st.markdown(
        """
        ###### Tabela Geral
        Tabela contendo todas as informações sobre a exportação de vinho e os paises de destino
        """
    )
    
    with st.expander("📄 Descrição dos Campos", expanded=False):
        st.markdown(
            """
                **Ano de Referência**: Ano em que a exportação foi realizada
                \n**País de Destino**: País para onde o vinho foi exportado
                \n**População do País**: População do País no ano de referência
                \n**Idade Média do** País: Idade Média do País no ano de referência
                \n**Dens. Pop**. do País: Densidade Populacional do País no ano de referência
                \n**Razão de Sexo** do País: Número de Homens para cada 100 Mulheres no ano de referência
                \n**Vinho Exportado (Litros**): Quantidade de Vinho Exportado (em Litros)
                \n**Vinho Exportado por** Pessoa (Litros): Quantidade de Vinho Exportado por Pessoa (em Litros)
                \n**Valor Exportado (US**\$): Valor Total Exportado (em US\$)
                \n**Preço do Vinho** (US\$/Litro): Preço do Vinho em US\$/Litro
            """
        )
    df_aux = (
        df.select(
            pl.col("year").alias("Ano de Referência"),
            pl.col("country").alias("País de Destino"),
            pl.col("population").alias("População do País"),
            pl.col("median_age").alias("Idade Média do País"),
            pl.col("pop_density").alias("Dens. Pop. do País"),
            pl.col("sex_ratio").alias("Razão de Sexo do País"),
            pl.col("liters").alias("Vinho Exportado (Litros)"),
            pl.col("liters_per_capita").alias("Vinho Exportado por Pessoa (Litros)"),
            pl.col("value").alias("Valor Exportado (US$)"),
            pl.col("price_per_liter").alias("Preço do Vinho (US$/Litro)"),
        )
        .fill_nan(0)
        .fill_null(0)
    )

    st.dataframe(
        df_aux,
        use_container_width=True,
        column_config={
            "Valor Exportado (US$)": st.column_config.NumberColumn(
                "Valor Exportado (US$)",
                help="Valor Total Exportado (em US\$)",
                format="US$ %.2f",
            ),
            "Preço do Vinho (US$/Litro)": st.column_config.NumberColumn(
                "Preço do Vinho (US$/Litro)",
                help="Preço do Vinho em US\$/Litro",
                format="US$ %.2f",
            ),
        },
    )

    return None

def tab_graph(df: pd.DataFrame) -> None:
    st.markdown("<div style='margin-bottom: 40px'></div>", unsafe_allow_html=True)
    
    layout.l_visual_two_bar(df)
    layout.l_visual_three_bar(df)
    layout.l_visual_four_map(df)
    layout.l_visual_five_map(df)
    layout.l_visual_six_bar(df)

    return None