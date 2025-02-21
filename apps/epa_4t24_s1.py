import marimo

__generated_with = "0.11.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import pyarrow
    import numpy as np
    import pandas as pd
    return np, pd, pyarrow


@app.cell
def _(mo):
    data_path = (
        mo.notebook_location() / "public"
    )
    datos = data_path.joinpath("epa_4t2024_sel1.feather")
    return data_path, datos


@app.cell
def _(datos, pd):
    df = pd.read_feather(datos)
    return (df,)


@app.cell
def _(df, mo, np):
    d1 = mo.ui.dropdown(np.sort(df.Sector.dropna().unique()), label='Sector', value='01-Agricultura, gandaría, caza e servizos relacionados con elas')
    d2 = mo.ui.dropdown(np.sort(df.Sector.dropna().unique()), label='Sector', value='01-Agricultura, gandaría, caza e servizos relacionados con elas')
    return d1, d2


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # EPA 4º Trimestre 2024
        Os microdatos da *Encuesta de Población Activa* (EPA) proporcionan información detallada sobre o mercado de traballo galego. En particular, fornecen de valiosa información sobre as características dos traballadores ocupados desagregadas por sector e ocupación.

        Unha destas características é a idade do traballador, unha variable fundamental de cara a prever onde se producirán vacantes no próximo futuro derivadas das decisións de xubilación por parte dos traballadores actuais.

        Como exemplo, presentamos a continuación o número de traballadores maiores de 56 anos por idade, sector de actividade (CNAE-2009 a dous díxitos) e ocupación (CNO-2011 a dous díxitos):
        """
    )
    return


@app.cell
def _(d1, df, mo, pd):
    mo.vstack(
        (
            d1,
            mo.ui.table(
                (
                    pd.DataFrame(
                        df.query("Sector==@d1.value")
                        .groupby(["Ocupación", "Idade"], observed=False)
                        .Factor.sum()
                    )
                    .pivot_table(
                        index="Ocupación",
                        columns="Idade",
                        values="Factor",
                        observed=False,
                    )
                    .iloc[:,2:]
                    .assign(Total=lambda x: x.sum(
                                axis=1
                            )
                    )
                    .T
                    .assign(Total=lambda x:x.sum(axis=1))
                    .T
                    .reset_index()
                ),
                selection=None,
                show_column_summaries=False,
                pagination=False,
                format_mapping={
                    "57": "{:.0f}",
                    "58": "{:.0f}",
                    "59": "{:.0f}",
                    "60": "{:.0f}",
                    "61": "{:.0f}",
                    "62": "{:.0f}",
                    "63": "{:.0f}",
                    "64": "{:.0f}",
                    "65": "{:.0f}",
                    "Mais de 65": "{:.0f}",
                    "Total": "{:.0f}",
                },
                wrapped_columns=['Ocupación']
            ),
        )
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Xubilacións
        Os microdatos da EPA tamén permiten estimar con relativa precisión o número de traballadores que se xubilan nun período determinado.

        Como exemplo, presentamos a continuación o número de traballadores que se xubilaron ao longo do último trimestre do ano 2024. O total de **4.480** traballadores podemos desagregalo por idade, sector de actividade (CNAE-2009 a dous díxitos) e ocupación (CNO-2011 a dous díxitos). O dato da idade é importante, xa que a idade de xubilación efectiva varía moito por sector e ocupación:
        """
    )
    return


@app.cell
def _(d2, df, mo, pd):
    mo.vstack(
        (
            d2,
            mo.ui.table(
                (
                    pd.DataFrame(
                        df.query(
        "Sector_Anterior==@d2.value&Meses<4&Relación=='Inactivos 3 (resto de inactivos)'&Situación=='Percibía una pensión de jubilación o unos ingresos de prejubilación'"
    )
                        .groupby(["Ocupación_Anterior", "Idade2"], observed=False)
                        .Factor.sum()
                    )
                    .pivot_table(
                        index="Ocupación_Anterior",
                        columns="Idade2",
                        values="Factor",
                        observed=False,
                    )
                    .assign(Total=lambda x: x.sum(
                                axis=1
                            )
                    )
                    .T
                    .assign(Total=lambda x:x.sum(axis=1))
                    .T
                    .reset_index()
                    .rename(columns={'Ocupación_Anterior':'Ocupación'})
                ),
                selection=None,
                show_column_summaries=False,
                pagination=False,
                format_mapping={
                    "Menos de 60": "{:.0f}",
                    "60": "{:.0f}",
                    "61": "{:.0f}",
                    "62": "{:.0f}",
                    "63": "{:.0f}",
                    "64": "{:.0f}",
                    "65": "{:.0f}",
                    "Mais de 65": "{:.0f}",
                    "Total": "{:.0f}",
                },
                wrapped_columns=['Ocupación']
            ),
        )
    )
    return


if __name__ == "__main__":
    app.run()
