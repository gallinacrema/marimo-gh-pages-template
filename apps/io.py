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
    return functools, inv, matrix_power, np, openpyxl, pd


@app.cell
def _(mo):
    data_path = mo.notebook_location() / "public" / "Matriz_Simetrica_MIOGAL21.xlsx"
    return (data_path,)


@app.cell
def _(data_path, pd):
    Z_MIOGAL_21 = pd.read_excel(data_path, sheet_name=1).iloc[5:76,2:73].to_numpy().astype(float)
    x_MIOGAL_21 = pd.read_excel(data_path, sheet_name=1).iloc[87,2:73].to_numpy().astype(float)
    A_MIOGAL_21 = pd.read_excel(data_path, sheet_name=4).iloc[5:76,2:73].to_numpy().astype(float)
    L_MIOGAL_21 = pd.read_excel(data_path, sheet_name=6).iloc[5:76,2:73].to_numpy().astype(float)
    return A_MIOGAL_21, L_MIOGAL_21, Z_MIOGAL_21, x_MIOGAL_21


@app.cell
def _(functools, np):
    def coef(func):
        @functools.wraps(func)
        def ratio(array,x):
            return array @ np.linalg.inv(np.diag(x))
        return ratio
    return (coef,)


@app.cell
def _(coef, numpy):
    @coef
    def A(Z: numpy.ndarray, x: numpy.ndarray) -> numpy.ndarray:
        """
        Compute the technical coefficients matrix

        Parameters
        ----------
        Z : numpy.ndarray
        The transactions matrix

        x : numpy.ndarray
        The vector of total outputs

        Returns
        -------
        A : numpy.ndarray
        The technical coefficients matrix
        """
        return  Z, x
    return (A,)


@app.cell
def _(functools, np):
    def leontief(func):
        @functools.wraps(func)
        def inverse(matrix):
            return np.linalg.inv(np.identity(matrix.shape[0]) - matrix)
        return inverse
    return (leontief,)


@app.cell
def _(leontief, numpy):
    @leontief
    def L(A: numpy.ndarray) -> numpy.ndarray:
        """
        Compute the Leontief inverse matrix

        Parameters
        ----------
        A : numpy.ndarray
        The technical coefficients matrix

        Returns
        -------
        L : numpy.ndarray
        The Leontief inverse matrix
        """
        return A
    return (L,)


@app.cell
def _(functools):
    def requirements(func):
        @functools.wraps(func)
        def product(L,vector):
            return L @ vector
        return product
    return (requirements,)


@app.cell
def _(numpy, requirements):
    @requirements
    def x_new(L: numpy.ndarray, f_new:numpy.ndarray) -> numpy.ndarray:
        """
        Compute the total outputs necessary to meet a new final demand vector

        Parameters
        ----------
        L : numpy.ndarray
        The Leontief inverse matrix

        f_new : numpy.ndarray
        The vector of new final demands

        Returns
        -------
        x_new : numpy.ndarray
        The new values of total outputs
        """
        return L, f_new
    return (x_new,)


@app.cell
def _(functools, np):
    def impact(func):
        @functools.wraps(func)
        def translation(vector,x):
            return np.diag(vector) @ x
        return translation
    return (impact,)


@app.cell
def _(impact, numpy):
    @impact
    def varepsilon(e: numpy.ndarray, x_new: numpy.ndarray) -> numpy.ndarray:
        """
        Compute the total labor income necessary to meet a new final demand vector

        Parameters
        ----------
        e : numpy.ndarray
        The original vector of labor incomes per monetary unit

        x_new : numpy.ndarray
        The new values of total outputs

        Returns
        -------
        varepsilon : numpy.ndarray
        The new values of total labor incomes
        """
        return e, x_new
    return (varepsilon,)


@app.cell
def _(functools, np):
    def disaggregation(func):
        @functools.wraps(func)
        def proportion(matrix,vector):
            return matrix @ np.diag(vector)
        return proportion
    return (disaggregation,)


@app.cell
def _(disaggregation, numpy):
    @disaggregation
    def varepsilon_tilde(
        P: numpy.ndarray, varepsilon: numpy.ndarray
    ) -> numpy.ndarray:
        """
        Compute a matrix of employment by sector by occupation type

        Parameters
        ----------
        P : numpy.ndarray
        An occupation-by-industry matrix

        varepsilon : numpy.ndarray
        The new values of total labor incomes

        Returns
        -------
        varepsilon_tilde : numpy.ndarray
        The new values of total labor incomes by occupation by sector
        """
        return P, varepsilon
    return (varepsilon_tilde,)


@app.cell
def _(coef, numpy):
    @coef
    def vc(v: numpy.ndarray, x: numpy.ndarray) -> numpy.ndarray:
        """
        Compute the vector of value-added coefficients

        Parameters
        ----------
        v : numpy.ndarray
        The vector of total value-added expenditures by each sector

        x : numpy.ndarray
        The vector of total outputs

        Returns
        -------
        vc : numpy.ndarray
        The vector of value-added coefficients
        """
        return  v, x
    return (vc,)


@app.cell
def _(numpy, requirements):
    @requirements
    def ptil(L_prime: numpy.ndarray, vc:numpy.ndarray) -> numpy.ndarray:
        """
        Compute the index prices

        Parameters
        ----------
        L_prime : numpy.ndarray
        The Leontief inverse matrix transposed

        vc : numpy.ndarray
        The vector of value-added coefficients

        Returns
        -------
        ptil : numpy.ndarray
        The vector of index prices
        """
        return L_prime, vc
    return (ptil,)


@app.cell
def _(data_path, pd):
    labels = pd.read_excel(data_path, sheet_name=1).iloc[5:76,1].to_numpy()
    return (labels,)


@app.cell
def _(labels, pd):
    entry_table = pd.DataFrame([labels, [0]*71], index=['Sector','Cambio na produción']).T
    return (entry_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # MIOGAL-21
        ## Impacto sobre produción (modelo de Leontief)
        Introduza variacións na demanda final dos sectores (en miles de €) e obterá como resultado a estimación das variacións na produción por sector (tamén en miles de €) segundo o modelo de Leontief.
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
def _(L_MIOGAL_21, f_new, labels, mo, pd, x_new):
    df = pd.DataFrame([labels, x_new(L_MIOGAL_21,f_new)], ['Sector','Cambio na produción']).T
    row_sums = df.iloc[:,1].sum()
    last_row = pd.DataFrame([{'Sector':'TOTAL','Cambio na produción':row_sums}])
    mo.ui.table(pd.concat([df, last_row]).reset_index().drop('index', axis=1), pagination=False, selection=None, show_column_summaries=False, format_mapping={'Cambio na produción':'{:.1f}'.format})
    return df, last_row, row_sums


if __name__ == "__main__":
    app.run()
