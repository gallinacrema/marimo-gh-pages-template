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
    return (d1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # EPA 4º Trimestre 2024
        Os microdatos da *Encuesta de Población Activa* proporcionan información detallada sobre o mercado de traballo galego. En particular, fornecen de valiosa información sobre as características dos traballadores ocupados desagregadas por sector e ocupación.

        Unha destas características é a idade do traballador, unha variable fundamental de cara a prever onde se producirán vacantes no próximo futuro derivadas das decisións de xubilación por parte dos traballadores actuais.

        Como exemplo, presentamos a continuación o número de traballadores maiores de 55 anos por idade, sector de actividade (CNAE-2009 a dous díxitos) e ocupación (CNO-2011 a dous díxitos):
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
                    "Menor de 56": "{:.0f}",
                    "56": "{:.0f}",
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


if __name__ == "__main__":
    app.run()
