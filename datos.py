import pandas as pd


def read_data_ebsa():
    file = pd.ExcelFile('cuentas.xlsx')
    work_sheet = file.parse('EBSA')

    return work_sheet
