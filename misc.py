def get_excel_file_path(excel_file):
    xl_file_path = ""
    for index, value in enumerate(excel_file.split("/")[:-1]):
        if index == 0:
            xl_file_path += value
        else:
            xl_file_path += "\\"
            xl_file_path += value
    return xl_file_path


def get_excel_file_name(excel_file):
    return excel_file.split("/")[-1].split(".")[0]


def generate_3bdata_report(file_name, mysqldb):
    with open(file_name, "w", encoding="utf-8") as outputFile:
        outputFile.write(
            "gstin, name, month, normal_sales, nor_igst, nor_cgst, nor_sgst, nor_cess, export, exp_igst, exp_cess, exempt, rcm_taxval, rcm_igst, rcm_cgst, rcm_sgst, rcm_cess, non_gst"
        )
        outputFile.write("\n")
        for row in mysqldb.query("SELECT * FROM gstr3b_data"):
            writeRow = ",".join([str(i) for i in row])
            outputFile.write(writeRow)
            outputFile.write("\n")


def generate_client_report(file_name, mysqldb):
    with open(file_name, "w", encoding="utf-8") as outputFile:
        outputFile.write(
            "srn, name, gstin, userid, password, processed"
        )
        outputFile.write("\n")
        for row in mysqldb.query("SELECT * FROM client_data"):
            writeRow = ",".join([str(i) for i in row])
            outputFile.write(writeRow)
            outputFile.write("\n")
