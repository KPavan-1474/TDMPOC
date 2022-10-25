from faker import Faker
import secrets
import string
import pandas
import pandas as pd
import re
#import pyodbc
import os
from pathlib import Path
from pandas import read_excel
import helperLibrary as helperLib
import openpyxl
import mysql.connector
import collections
from sqlalchemy import create_engine
import xlrd
import numpy as np

def logger():
    config_folder_path = Path("./Configuration/")
    config_file_path = config_folder_path / "config.ini"
    if not os.path.exists(config_file_path):
        print(f"Failed to read Config file '{config_file_path}'... Exiting!!", flush=True)
        return False, f"Failed to read Config file '{config_file_path}'"
        # Get the Logging configuration properties from the config file
    log_config_values = helperLib.get_config_section(config_file_path, "LoggerSettings")
    if not log_config_values:
        # Do not use helperLib.print_msg before logger is initialized
        print("ERROR", "Failed to read 'LoggerSettings'... Exiting!!", flush=True)
        return False, "Failed to read 'LoggerSettings'"

    log_folder_path = log_level = log_mode = ""
    try:
        log_folder_path = log_config_values["log_folder_path"]
        log_level = log_config_values["log_level"]
        log_mode = log_config_values["log_mode"]
    except Exception as e:
        # Do not use helperLib.print_msg before logger is initialized
        print("CRITICAL", "Failed to get all log properties from LoggerSettings config... Exiting!!")
        return False, "Failed to get all log properties from LoggerSettings config"

    if not os.path.exists(log_folder_path):
        print("ERROR", f"Invalid 'log_folder_path' '{log_folder_path}' specified in "
                       f"config... Exiting!!")
        return False, f"Invalid 'log_folder_path' '{log_folder_path}' specified in config"

    logger_status = helperLib.init_logger(log_folder_path=log_folder_path, log_level=log_level, log_mode=log_mode)
    if not logger_status:
        helperLib.print_msg("ERROR", "Failed to initialize logger... Exiting!!")
        return False, "Failed to initialize logger"

    conf_status, inbound_folder_path = helperLib.get_config_value(config_file_path, "FolderPaths",
                                                                  "inbound_folder_path")
    if not conf_status:
        helperLib.print_msg("ERROR", "Failed to read 'inbound_folder_path' from 'FolderPaths'... Exiting!!")
        return False, "Failed to read 'inbound_folder_path' from 'FolderPaths'"

    if not os.path.exists(inbound_folder_path):
        helperLib.print_msg("ERROR", f"Invalid 'inbound_folder_path' '{inbound_folder_path}' specified in "
                                     f"config... Exiting!!")
        return False, f"Invalid 'inbound_folder_path' '{inbound_folder_path}' specified in config"

    conf_status, outbound_folder_path = helperLib.get_config_value(config_file_path, "FolderPaths",
                                                                   "outbound_folder_path")
    if not conf_status:
        helperLib.print_msg("ERROR", "Failed to read 'outbound_folder_path' from 'FolderPaths'... Exiting!!")
        return False, "Failed to read 'outbound_folder_path' from 'FolderPaths'"

    helperLib.print_msg("INFO", f"paths : {inbound_folder_path}, {outbound_folder_path}")

def tdm_api_genrate(database_connect, script_type, no_of_rows, datavalues, columns_array, pyodbc=None):
    # Initialize
    if database_connect == "True":
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQL$1474",
            database="POCTDM"
        )

        cur = mydb.cursor()

        cur.execute("SELECT * FROM customer")

        rows = cur.fetchall()

        objects_list = []
        d = dict()
        for row in rows:
            d = collections.OrderedDict()
            d['id'] = row[0]
            d['Name'] = row[1]
            d['Age'] = row[2]
            d['SSN'] = row[3]
            d['OrderId'] = row[4]
            objects_list.append(d)
        d = {"database-connect": "false", "type": "mask", "rows": 100, "data": objects_list,
             "mask-columns": [
                 "ssn",
                 "ccn"
             ]
             }
        j = json.dumps(d)

        print(j)

    else:
        fake = Faker(locale='en_US')
        fake_workers = [
            {'emp_id': '',
             'emp_name': fake.name(),
             'emp_address': fake.address(),
             'emp_dob': fake.date_between(start_date='-60y', end_date='-20y'),
             'credit_card_number': fake.credit_card_number(),
             'emp_ssn': ''.join(secrets.choice(string.digits) for i in range(9))
             }
            for x in range(no_of_rows)]
        df = pd.DataFrame(fake_workers)
        if script_type == "mask":
            for col in columns_array:
                if col == "ssn":
                    df.emp_ssn = df.emp_ssn.apply(lambda x: re.sub(r'\d', '*', x, count=5))
                elif col == "ccn":
                    df.credit_card_number = df.credit_card_number.apply(lambda x: re.sub(r'\d', '*', x, count=10))
            df.to_excel("C:/Users/pavankumark/PycharmProjects/POCTDM/Output/Data.xlsx", sheet_name="Masked_Data")
            df['emp_id']=np.arange(len(df))
            engine = create_engine("mysql+mysqldb://root:MySQL$1474@localhost/POCTDM", echo=False)
        df.to_sql(con=engine, name='data masked', if_exists='append', index=False)

        json = df.to_json()
        return json





