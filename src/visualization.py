import streamlit as st
import plotly.express as px
import polars as pl
from . import utils
import pandas as pd


def visual_globe(df: pd.DataFrame) -> px.scatter_geo:
    df_aux = (
        df[df['liters'] > 1000]
        .groupby(["continent", "iso_code", "country"])
        .agg({"value": "sum"})
        .reset_index()
    )

    fig = px.scatter_geo(
        df_aux,
        locations="iso_code",
        size="value",
        color="continent",
        projection="orthographic",
        size_max=50,
        hover_name="country",
        custom_data=["value", "continent"]
    )

    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>%{customdata[0]} Litros<extra>%{customdata[1]}</extra>"
    )

    fig.update_layout(
        title={
            "text": "Total de Litros de vinho exportados por País",
            "xanchor": "center",
            "xref": "paper",
            "yanchor": "top",
            "x": 0.5,
            "y": 0.95,
            "font": {"size": 20},
        },
        template="seaborn",
        height=500,
        margin={"l": 10, "r": 10, "b": 80, "t": 70, "pad": 5},
        legend={
            "orientation": "v",
            "yanchor": "middle",
            "xanchor": "center",
            "x": 1,
            "y": 0.5,
            "title": "",
            "itemsizing": "constant",
        },
    )

    return fig

def table_info(df: pd.DataFrame) -> pd.DataFrame:
    df = pl.from_pandas(df)
    return df.select(
        pl.lit("Brasil").alias("País de Origem"),
        pl.col("country").alias("País de Destino"),
        pl.col("year").alias("Ano de Referência"),
        pl.col("liters").alias("Quantidade de Vinho Exportado (Litros)"),
        pl.col("value").alias("Valor Total Exportado (US$)"),
    )

def visual_two_bar(df: pd.DataFrame, config: dict) -> None:
   
    if not config['decade']:
        df_aux = df.groupby("year").agg({"value": "sum"}).reset_index()
        group = "year"
        hovertemplate = "<b>Ano de %{x}</b><br>U$ %{y:.2f}"
    else:
        df_aux = (
            df.assign(decade=df["year"] // 10 * 10)
            .groupby("decade")
            .agg({"value": "sum"})
            .reset_index()
        )
        group = "decade"
        hovertemplate = "<b>Década de %{x}</b><br>U$ %{y:.2f}"

    fig = px.bar(df_aux, x=group, y="value")

    utils.layout_graphs(
        fig,
        title_text="Valor Total Exportado (US$)",
        title_sup="Gráfico de Barras exibindo o valor total de vinhos exportados ao longo dos anos",
        xaxis={"title": "Ano de Referência" if group == "year" else "Década"},
        yaxis={"title": "Valor Total Exportado (US$)"},
        hovertemplate=hovertemplate,
        marker_color="#794A9E"
    )

    return fig

def visual_three_bar(df: pd.DataFrame, config: dict) -> None:
    var = "value" if config['metric'] == "Valor Exportado" else "liters"
    agg_func = "sum" if config['agg'] == "Valor Total" else "mean"

    df_aux = df.groupby("continent").agg({var: agg_func}).reset_index().sort_values(by=var, ascending=False)
    fig = px.bar(df_aux, x="continent", y=var)

    layout_info = {
        "Valor Exportado": {
            "Valor Total": {
                "yaxis": {"title": "Valor Total Exportado (US$)"},
                "hovertemplate": "<b>%{x}</b><br>Total: U$ %{y}",
                "title": "Valor Total Exportado por Região",
                "sup": "Gráfico de Barras exibindo o valor total de vinhos exportado (em US$) para cada região do mundo",
            },
            "Valor Médio": {
                "yaxis": {"title": "Valor Médio Exportado (US$)"},
                "hovertemplate": "<b>%{x}</b><br>Média: U$ %{y}",
                "title": "Valor Médio Exportado por Região",
                "sup": "Gráfico de Barras exibindo o valor médio de vinho exportado (em US$) para cada região do mundo",
            },
        },
        "Litros Exportados": {
            "Valor Total": {
                "yaxis": {"title": "Total de Vinho Exportados (Litros)"},
                "hovertemplate": "<b>%{x}</b><br>Total: %{y} Litros",
                "title": "Volume de Vinho Exportado por Região",
                "sup": "Gráfico de Barras exibindo o volume total de vinho exportado (em litros) para cada região do mundo",
            },
            "Valor Médio": {
                "yaxis": {"title": "Volume Médio de Vinho Exportado (Litros)"},
                "hovertemplate": "<b>%{x}</b><br>Média: %{y} Litros",
                "title": "Volume Médio de Vinho Exportado por Região",
                "sup": "Gráfico de Barras exibindo o volume médio de vinho exportado (em litros) para cada região do mundo",
            },
        },
    }
    
    layout_info_selected = layout_info[config['metric']][config['agg']]

    utils.layout_graphs(
        fig,
        yaxis=layout_info_selected["yaxis"],
        xaxis={"title": "Região"},
        hovertemplate=layout_info_selected["hovertemplate"],
        title_text=layout_info_selected["title"],
        title_sup=layout_info_selected["sup"],
        marker_color="#794A9E"
    )
    
    return fig

def visual_four_map(df: pd.DataFrame, config: dict) -> None:
    var = "value" if config['metric'] == "Valor Exportado" else "liters"
    agg_func = "sum" if config['agg'] == "Valor Total" else "mean"
    year = config['year']

    df_aux = (
        df[(df["year"] >= year[0]) & (df["year"] <= year[1])]
        .groupby(["continent", "iso_code", "country"])
        .agg({var: agg_func})
        .reset_index()
        .sort_values(by="continent")
    )

    fig = px.scatter_geo(
        df_aux,
        locations="iso_code",
        size=var,
        color="continent",
        projection="natural earth",
        size_max=30,
        custom_data=["country", var],
        color_discrete_map={
            "Oceania": "#636EFA",
            "América Central e Caribe": "#EF553B",
            "América do Norte": "#00CC96",
            "África": "#AB63FA",
            "Europa": "#FFA15A",
            "Oriente Médio": "#19D3F3",
            "América do Sul": "#FECB52",
            "Ásia": "#FF6692",
        },
    )

    layout_info = {
        "Valor Exportado": {
            "Valor Total": {
                "yaxis": {"title": "Valor Total Exportado (US$)"},
                "hovertemplate": "<b>%{customdata[0]}</b><br>Total: U$ %{customdata[1]}",
                "title": "Valor Total Exportado (US$) por País",
                "sup": "Mapa exibindo o valor total de vinho exportado (em US$) para cada país do mundo",
            },
            "Valor Médio": {
                "yaxis": {"title": "Valor Médio Exportado (US$)"},
                "hovertemplate": "<b>%{customdata[0]}</b><br>Média: U$ %{customdata[1]:.2f}",
                "title": "Valor Médio Exportado por País",
                "sup": "Mapa exibindo o valor médio de vinho exportado (em US$) para cada país do mundo",
            },
        },
        "Litros Exportados": {
            "Valor Total": {
                "yaxis": {"title": "Total de Vinho Exportados (Litros)"},
                "hovertemplate": "<b>%{customdata[0]}</b><br>Total: %{customdata[1]} Litros",
                "title": "Total de Vinho Exportados por País",
                "sup": "Mapa exibindo o volume total de vinho exportado (em litros) para cada país do mundo",
            },
            "Valor Médio": {
                "yaxis": {"title": "Volume Médio de Vinho Exportado (Litros)"},
                "hovertemplate": "<b>%{customdata[0]}</b><br>Média: %{customdata[1]:.2f} Litros",
                "title": "Volume Médio de Vinho Exportado por País",
                "sup": "Mapa exibindo o volume médio de vinho exportado (em litros) para cada país do mundo",
            },
        },
    }
    
    layout_info_selected = layout_info[config['metric']][config['agg']]

    utils.layout_graphs(
        fig,
        yaxis=layout_info_selected["yaxis"],
        xaxis={"title": "Continente"},
        hovertemplate=layout_info_selected["hovertemplate"],
        legend={
            "orientation": "h",
            "yanchor": "middle",
            "xanchor": "center",
            "x": 0.5,
            "y": -0.1,
            "title": "",
            "itemsizing": "constant",
        },
        title_text=layout_info_selected["title"],
        title_sup=layout_info_selected["sup"]
    )

    return fig

def visual_five_map(df: pd.DataFrame, config: dict) -> None:
    cols = st.columns([2, 1], gap="large")
    col_name = config['col_name']
    
    if config['viz'] == "Customizar":
        list_selected = config['list_selected']
    else:
        df_list_country = (
            df.groupby("country")
            .agg({col_name: "sum"})
            .reset_index()
            .sort_values(by=col_name, ascending=False)
            .head(3)
        )
        list_selected = df_list_country["country"].tolist()

    with cols[0]:
        df["group"] = df["country"].apply(lambda x: x if x in list_selected else "Outros")
        df["order"] = df.apply(lambda row: row[col_name] if row["country"] in list_selected else 0, axis=1)

        df_aux = (
            df.groupby(["year", "group"])
            .agg({col_name: "sum", "order": "sum"})
            .reset_index()
            .sort_values(by=["year", "order"])
        )

        fig = px.line(
            df_aux,
            x="year",
            y=col_name,
            color="group",
            color_discrete_sequence=px.colors.qualitative.Plotly,
            color_discrete_map={"Outros": "#ccc"},
            markers=True,
        )

        layout_info = {
            "Valor Exportado": {
                "yaxis": {"title": "Valor Total Exportado (US$)"},
                "hovertemplate": "<b>%{x}</b><br>U$ %{y}",
                "title": "Valor Total Exportado nos Anos de Referência",
                "sup": "Gráfico de Linha exibindo o valor total de vinho exportado (em US$) por país ao longo do tempo",
            },
            "Litros Exportados": {
                "yaxis": {"title": "Total de Vinho Exportados (Litros)"},
                "hovertemplate": "<b>%{x}</b><br>%{y} Litros",
                "title": "Total de Vinho Exportados nos Anos de Referência",
                "sup": "Gráfico de Linha exibindo o volume total de vinho exportado (em litros) por país ao longo do tempo",
            },
        }
        
        layout_info_selected = layout_info[config['metric']]

        utils.layout_graphs(
            fig,
            yaxis=layout_info_selected["yaxis"],
            xaxis={"title": "Ano de Referência"},
            hovertemplate=layout_info_selected["hovertemplate"],
            legend={
                "orientation": "h",
                "yanchor": "middle",
                "xanchor": "center",
                "x": 0.5,
                "y": -0.3,
                "title": "",
                "itemsizing": "constant",
                "traceorder": "reversed",
            },
            title_text=layout_info_selected["title"],
            title_sup=layout_info_selected["sup"]
        )
        
    return fig

def visual_six_bar(df: pd.DataFrame, config: dict) -> None:

    if not config['median_region']:
        df_aux = (
            df[df["price_per_liter"] > 0]
            .groupby("year")
            .agg({"price_per_liter": "median"})
            .reset_index()
            .sort_values("year")
        )
        fig = px.line(df_aux, x="year", y="price_per_liter")
        hovertemplate = "<b>Ano de %{x}</b><br>U$ %{y:.2f}"
        titlex = "Ano de Referência"
        title = "Preço mediano por litro por Ano"
        title_sup = "Gráfico de Linha exibindo o preço mediano por litro de vinho exportado (em US$) ao longo do tempo"
        line_color = "#794A9E"
        marker_color = ""
    else:
        df_aux = (
            df[df["price_per_liter"] > 0]
            .groupby("continent")
            .agg({"price_per_liter": "median"})
            .reset_index()
            .sort_values("price_per_liter", ascending=False)
        )
        fig = px.bar(df_aux, x="continent", y="price_per_liter")
        hovertemplate = "<b>%{x}</b><br>U$ %{y:.2f}"
        titlex = "Região"
        title = "Preço mediano por litro (US$) por Região"
        title_sup = "Gráfico de Linha exibindo o preço total mediano por litro de vinho exportado (em US$) para cada região do mundo"
        line_color = ""
        marker_color = "#794A9E"

    utils.layout_graphs(
        fig,
        xaxis={"title": titlex},
        yaxis={"title": "Preço mediano por Litro (US$)"},
        hovertemplate=hovertemplate,
        legend={
            "orientation": "h",
            "yanchor": "middle",
            "xanchor": "center",
            "x": 0.5,
            "y": -0.3,
            "title": "",
            "itemsizing": "constant",
            "traceorder": "reversed",
        },
        title_text=title,
        title_sup=title_sup,
        line_color=line_color,
        marker_color=marker_color
    )

    return fig