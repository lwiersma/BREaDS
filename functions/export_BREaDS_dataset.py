import pandas as pd


def export_BREaDS_dataset(filename, df, residue):
    """
    This function exports all simulation data into the Excel worksheet that has been used for importing data.
    """
    with pd.ExcelWriter(
        filename, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as writer:
        df.to_excel(excel_writer=writer, sheet_name="outputBREaDS")
        residue.to_excel(excel_writer=writer, sheet_name="residue")
