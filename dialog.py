import PySimpleGUI as sg
from misc import get_excel_file_path, get_excel_file_name
import os
from sqlquery import MySqlite3
from excel_processing import generate_client_list_from_xl_input


def getCaptcha():
    layout = [
        [sg.Text("Enter Captcha"), ],
        [sg.InputText(key='captcha'), ],
        [sg.Button(button_text="Submit")],
    ]

    window = sg.Window('Captcha Entry', auto_size_text=True,
                       button_color=('white', 'blue'),
                       icon='N.ico').Layout(layout)

    captcha_text = ""
    while True:
        event, values = window.Read()
        if event == "Submit":
            captcha_text = window.Element('captcha').Get()
            break
        elif event == 'Quit' or values is None:
            break
    window.close()
    return captcha_text


def main_windows():
    mysqldb = ""
    xl_file_path = ""
    layout = [
        [
            sg.Text('Choose Excel Template to generate .db file',
                    size=(32, 1), auto_size_text=False, justification='left'),
            sg.InputText(key='xl_file'), sg.FileBrowse(
                file_types=(("ALL Files", "*.xlsx*"),)),
        ],
        [
            sg.Button(button_text='Generate DB',), sg.Text(
                '', key='gen_db_status', size=(60, 1), auto_size_text=True,
                justification='left')
        ],
        [
            sg.Text('OR'),
        ],
        [
            sg.Text('Choose .db file to process',
                    size=(32, 1),),
            sg.InputText(key='db_file'), sg.FileBrowse(
                file_types=(("ALL Files", "*.db*"),)),
        ],
        [
            sg.Button(button_text='Start Processing'),
        ],
    ]

    window = sg.Window('NR GSTR-3B Turnover Report Generator',
                       auto_size_text=True,
                       default_element_size=(40, 1),
                       button_color=('white', 'blue'),
                       icon='N.ico').Layout(layout)

    while True:
        event, values = window.Read(timeout=0)

        # Event handling for closing window
        if event == 'Quit' or values is None or event == "Start Processing":
            db_file = window.Element("db_file").Get()
            if db_file != "":
                xl_file_path = get_excel_file_path(db_file)
                mysqldb = MySqlite3(db_file)
            break
        elif event == "Generate DB":
            # get excel related info
            xl_file = window.Element("xl_file").Get()
            xl_file_name = get_excel_file_name(xl_file)
            xl_file_path = get_excel_file_path(xl_file)
            # check if db already exist if yes then
            db_file = xl_file_path + "//" + xl_file_name + ".db"
            try:
                if os.path.isfile(db_file):
                    # delete it
                    # TODO if db exist then ask whether to overwrite it or not
                    os.remove(db_file)
            except Exception:
                pass
            # now no db exist so generate it
            mysqldb = MySqlite3(db_file)
            # process excel data and list of row data
            data_list = generate_client_list_from_xl_input(xl_file)
            # generate table into db and put all excel data into it
            # client data table
            mysqldb.create_table("client_data",
                                 ["srn", "name", "gstin", "userid", "password",
                                  "processed"])
            for count, data in enumerate(data_list):
                mysqldb.edit_insert(
                    "INSERT INTO client_data(srn, name, gstin, userid, password,\
                    processed)VALUES(?, ?, ?, ?, ?, ?)",
                    (count+1, data[0], data[1], data[2], data[3], "no"))
            mysqldb.create_table(
                "gstr3b_data", ["gstin", "name", "month", "normal_sales", "nor_igst",
                                "nor_cgst", "nor_sgst", "nor_cess", "export",
                                "exp_igst", "exp_cess", "exempt", "rcm_taxval",
                                "rcm_igst", "rcm_cgst", "rcm_sgst", "rcm_cess",
                                "non_gst"])
            # for count, data in enumerate(data_list):
            #     mysqldb.edit_insert(
            #         "INSERT INTO gstr3b_data(gstin,) VALUES(?,)", (data[0],))
            #     # normal_sales, nor_igst, nor_cgst, nor_sgst,\
            #     # nor_cess, export, exp_igst, exp_cess, exempt, rcm_taxval\
            #     # rcm_igst, rcm_cgst, rcm_sgst, rcm_cess, non_gst\
            window.Element("db_file").Update(value=db_file)
    window.Close()
    return [mysqldb, xl_file_path]


def data_not_selected_dialog():
    return sg.PopupError("Invalid Inputs", icon='N.ico')


def look_into_report_dialog():
    return sg.PopupOK("Processing Completed. Look into report csv files",
                      icon='N.ico')
