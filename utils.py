import pandas as pd
import streamlit as st


def rfid_processing(path: str):
    """
    Process RFID data from an Excel file.

    Parameters:
    - path (str): Path to the Excel file.

    Returns:
    - pandas.DataFrame: Processed RFID data.
    """
    # Read Excel file into a pandas dataframe
    df = pd.read_excel(path)

    # Clean and transform data columns
    df["GRAI Code"] = df.Serial.str.strip()
    df["Pool"] = df["Tipo molde"].str.strip().str.capitalize()
    df["Manufacturer"] = "Riduco"
    df["Product type"] = df["Tamaño"].str.strip().str.lower()
    df["Provisioning device"] = df["Equipo provisioning"]
    df["Provisioning location"] = df["Ubicación"].str.strip().str.capitalize()
    df["Provisioning date (GRAI)"] = df["Fecha"]
    df["Batch number"] = df["Lote"]

    # Select specific columns for the output
    df = df[
        [
            "GRAI Code",
            "Pool",
            "Manufacturer",
            "Product type",
            "Provisioning device",
            "Provisioning location",
            "Provisioning date (GRAI)",
            "Batch number",
        ]
    ]

    return df



def ble_rfid_processing(path: str):
    df = (
        pd.read_excel(path, skiprows=4, usecols=["ID", "Device Descr", "Device ID"])
        .dropna(subset="Device ID")
        .drop_duplicates(subset="Device ID")
    )
    df = df.pivot(index="ID", values="Device ID", columns="Device Descr")
    meta = pd.read_excel(path, sheet_name=1)
    meta.iloc[:, 0] = meta.iloc[:, 0].str.capitalize()
    meta = meta.dropna().T
    meta.columns = meta.iloc[0, :]
    meta.reset_index(drop=True, inplace=True)
    meta = meta.drop(index=0)

    df["Ciudad"] = meta["Ciudad"].values[0]
    df["Tipo Molde"] = meta["Tipo molde"].values[0]
    df["Referencia"] = meta["Referencia"].values[0]
    df["Cantidad"] = meta["Cantidad"].values[0]
    df["Color"] = meta["Color"].values[0]
    df["Lote"] = meta["Lote"].values[0]
    df["Fecha"] = meta["Fecha"].values[0]

    df["GRAI Code"] = df["RFID Tag"]
    df["Sensor Id"] = df["GPS Device"]
    df["Pool"] = df["Tipo Molde"].str.strip().str.capitalize()
    df["Manufacturer"] = "Riduco"
    df["Product type"] = df["Referencia"].str.strip().str.lower()
    df["Pairing device"] = "2D SCANNER"
    df["Pairing location"] = df["Ciudad"].str.strip().str.capitalize()
    df["Pairing date (Sensor)"] = df["Fecha"]
    df["Batch number"] = df["Lote"]

    sensor_pairing = df[
        [
            "GRAI Code",
            "Sensor Id",
            "Pool",
            "Manufacturer",
            "Product type",
            "Pairing device",
            "Pairing location",
            "Pairing date (Sensor)",
        ]
    ].reset_index(drop=True)

    rfid_provisioning = df[
        [
            "GRAI Code",
            "Pool",
            "Manufacturer",
            "Product type",
            "Pairing device",
            "Pairing location",
            "Pairing date (Sensor)",
            "Batch number",
        ]
    ].reset_index(drop=True)

    rfid_provisioning["Provisioning device"] = rfid_provisioning["Pairing device"]
    rfid_provisioning["Provisioning location"] = rfid_provisioning["Pairing location"]
    rfid_provisioning["Provisioning date (GRAI)"] = rfid_provisioning[
        "Pairing date (Sensor)"
    ]

    rfid_provisioning = rfid_provisioning[
        [
            "GRAI Code",
            "Pool",
            "Manufacturer",
            "Product type",
            "Provisioning device",
            "Provisioning location",
            "Provisioning date (GRAI)",
            "Batch number",
        ]
    ]

    return sensor_pairing, rfid_provisioning


@st.cache_data
def convert_df(df):
    """
    Converts a dataframe to .csv and caches the data.

    Parameters:
    - df (pandas.DataFrame): Input dataframe to be converted.

    Returns:
    - bytes: Encoded CSV data.
    """
    return df.to_csv(index=False).encode("utf-8")


def read_and_process_file(input_path):
    """
    Reads excel or csv file
    """
    a = pd.read_excel(input_path)
    if any(a.iloc[:, 2].str.contains("GPS")):
        ble_process, rfid_process = ble_rfid_processing(input_path)
        rfid_process.drop_duplicates(subset="GRAI Code", inplace=True)
        # st.dataframe(ble_process)
        ble_process = ble_process.drop_duplicates(subset="GRAI Code").drop_duplicates(
            subset="Sensor Id"
        )
        return ble_process, rfid_process
    else:
        rfid_process = rfid_processing(input_path)
        rfid_process.drop_duplicates(subset="GRAI Code", inplace=True)
        return rfid_process
