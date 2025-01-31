import marimo

__generated_with = "0.10.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import functools
    import numpy as np
    import pandas as pd
    import openpyxl
    from numpy.linalg import inv, matrix_power
    from iotools.iotools import A, L, x_new, varepsilon, varepsilon_tilde, vc, ptil
    return (
        A,
        L,
        functools,
        inv,
        matrix_power,
        np,
        openpyxl,
        pd,
        ptil,
        varepsilon,
        varepsilon_tilde,
        vc,
        x_new,
    )


@app.cell
def _(mo):
    data_path = (
        mo.notebook_location() / "public" / "Matriz_Simetrica_MIOGAL21.xlsx"
    )
    return (data_path,)


@app.cell
def _(data_path, np, pd):
    Z_MIOGAL_21 = (
        pd.read_excel(data_path, sheet_name=1)
        .iloc[5:76, 2:73]
        .to_numpy()
        .astype(float)
    )
    x_MIOGAL_21 = (
        pd.read_excel(data_path, sheet_name=1)
        .iloc[87, 2:73]
        .to_numpy()
        .astype(float)
    )
    A_MIOGAL_21 = (
        pd.read_excel(data_path, sheet_name=4)
        .iloc[5:76, 2:73]
        .to_numpy()
        .astype(float)
    )
    L_MIOGAL_21 = (
        pd.read_excel(data_path, sheet_name=6)
        .iloc[5:76, 2:73]
        .to_numpy()
        .astype(float)
    )
    e_MIOGAL_21 = (
        pd.read_excel(data_path, sheet_name=1)
        .iloc[80, 2:73]
        .to_numpy()
        .astype(float)
    )
    C_MIOGAL_21 = (
        pd.read_excel(data_path, sheet_name=1)
        .iloc[5:76, 74]
        .to_numpy()
        .astype(float)
    )
    eC_MIOGAL_21 = np.array(
        [pd.read_excel(data_path, sheet_name=1).fillna(0).iloc[80, 74]]
    ).astype(float)

    v_MIOGAL_21_pa = x_MIOGAL_21 - np.ones(Z_MIOGAL_21.shape[0])@Z_MIOGAL_21
    return (
        A_MIOGAL_21,
        C_MIOGAL_21,
        L_MIOGAL_21,
        Z_MIOGAL_21,
        eC_MIOGAL_21,
        e_MIOGAL_21,
        v_MIOGAL_21_pa,
        x_MIOGAL_21,
    )


@app.cell
def _(
    C_MIOGAL_21,
    Z_MIOGAL_21,
    data_path,
    eC_MIOGAL_21,
    e_MIOGAL_21,
    np,
    pd,
    x_MIOGAL_21,
):
    Z_bar_MIOGAL_21 = np.vstack(
        (
            np.column_stack((Z_MIOGAL_21, C_MIOGAL_21)),
            np.hstack((e_MIOGAL_21, eC_MIOGAL_21)),
        )
    )
    x_bar_MIOGAL_21 = np.hstack(
        (
            x_MIOGAL_21,
            np.array([pd.read_excel(data_path, sheet_name=1).iloc[76, 74]]).astype(
                float
            ),
        )
    )
    return Z_bar_MIOGAL_21, x_bar_MIOGAL_21


@app.cell
def _(data_path, pd):
    labels = pd.read_excel(data_path, sheet_name=1).iloc[5:76,1].to_numpy()
    return (labels,)


@app.cell
def _(labels, pd):
    entry_table = pd.DataFrame([labels, [0]*71], index=['Sector','Variación demanda']).T
    return (entry_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # MIOGAL-21
        ## Impacto sobre produción (modelo de Leontief)
        Introduza variacións na demanda final dos sectores (en miles de €) e obterá como resultado a estimación das variacións na produción por sector (tamén en miles de €) segundo o modelo de Leontief, nas súas versións aberta e pechada aos fogares.
        """
    )
    return


@app.cell
def _(entry_table, mo):
    enter = mo.ui.experimental_data_editor(data=entry_table, pagination=False)
    enter
    return (enter,)


@app.cell
def _(enter):
    f_new = enter.value.iloc[:,1].to_numpy().astype(float)
    return (f_new,)


@app.cell
def _(
    A,
    L,
    L_MIOGAL_21,
    Z_bar_MIOGAL_21,
    f_new,
    labels,
    np,
    pd,
    x_bar_MIOGAL_21,
    x_new,
):
    df = (
        pd.DataFrame(
            [labels, x_new(L_MIOGAL_21, f_new)],
            ["Sector", "Variación produción (modelo aberto)"],
        )
        .T.convert_dtypes(convert_integer=False)
        .merge(
            pd.DataFrame(
                [
                    labels,
                    x_new(
                        L(A(Z_bar_MIOGAL_21, x_bar_MIOGAL_21)),
                        np.hstack((f_new, np.array([0]))),
                    ),
                ],
                ["Sector", "Variación produción (modelo pechado aos fogares)"],
            )
            .T[:-1]
            .convert_dtypes(convert_integer=False)
            .set_index("Sector"),
            on="Sector",
        )
        .set_index("Sector")
    )
    return (df,)


@app.cell
def _(df):
    df_next = df.agg(
        {
            "Variación produción (modelo aberto)": ["sum"],
            "Variación produción (modelo pechado aos fogares)": ["sum"],
        }
    )
    return (df_next,)


@app.cell
def _(df, df_next, mo, pd):
    mo.ui.table(
        pd.concat([df, df_next]).rename(index={"sum": "TOTAL"}),
        pagination=False,
        selection=None,
        show_column_summaries=False,
        format_mapping={
            "Variación produción (modelo aberto)": "{:.1f}".format,
            "Variación produción (modelo pechado aos fogares)": "{:.1f}".format,
        },
    )
    return


if __name__ == "__main__":
    app.run()
