import marimo

__generated_with = "0.11.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import numpy as np
    import pandas as pd
    return np, pd


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


@app.cell
def _(d1, df, mo, pd):
    mo.vstack(
        (
            d1,
            mo.ui.table(
                pd.DataFrame(
                    df.query("Sector==@d1.value").groupby("Ocupación").Factor.sum()
                )
                .rename(columns={"Factor": "Ocupados"})
                .reset_index()
                .to_dict(orient="records"),
                selection=None,
                show_column_summaries=False,
                pagination=False,
                format_mapping={"Ocupados": "{:.0f}"},
            ),
        )
    )
    return


if __name__ == "__main__":
    app.run()
