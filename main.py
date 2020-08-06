from sel_browser import login_to_GST_Portal
from dialog import (
    main_windows,
    data_not_selected_dialog,
    look_into_report_dialog)
from misc import generate_3bdata_report, generate_client_report


def main():
    # start main window and get mysqldb
    main_window_outputs = main_windows()
    if main_window_outputs[0] != "":
        mysqldb = main_window_outputs[0]
        xl_file_path = main_window_outputs[1]
        client_data = mysqldb.query2(
            "SELECT * FROM client_data WHERE processed=?", ("no",))
        # start processing # if successful then in db processed = yes else
        # pass to next client
        if len(client_data) > 0:
            login_to_GST_Portal(client_data, mysqldb)
            # generate report from sql
            generate_3bdata_report(xl_file_path + "//gstr3b_data.csv", mysqldb)
            generate_client_report(xl_file_path + "//client_data.csv", mysqldb)
        look_into_report_dialog()
    else:
        data_not_selected_dialog()


if __name__ == "__main__":
    main()
