import xlrd


def generate_client_list_from_xl_input(excel_file):
    client_list = []
    book = xlrd.open_workbook(excel_file)
    sheet = book.sheet_by_index(0)
    num_rows = sheet.nrows
    for n in range(1, num_rows):
        row_values_list = [cell for cell in sheet.row_values(n)]
        client_list.append(row_values_list)
    return client_list


# def generate_gstin_list_from_dict(client_dict):
#     gstin_list = []
#     for gstin in client_dict.keys():
#         gstin_list.append(gstin)
#     return gstin_list
