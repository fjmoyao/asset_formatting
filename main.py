import streamlit as st
import pandas as pd
import utils


st.header("Procesamiento de Provisioning and Pairing")

file = st.file_uploader(
    "Please upload your file to be converted",
    accept_multiple_files=False,
    type={"xlsx"},
)


if file:
    # Creating the button
    process_button = st.button("Procesa el archivo")
    if process_button:
        current_date = pd.to_datetime("today").date()
        # try:
        with st.spinner("Procesando los archivos"):
            processed_file = utils.read_and_process_file(file)

            if len(processed_file) == 2:
                new_file_name_ble = f"Crate_Sensor_pairing_{current_date}.csv"
                new_file_name_rfid = f"Crate_RFID_provisioning_{current_date}.csv"

                output_file_ble = utils.convert_df(processed_file[0])
                output_file_rfid = utils.convert_df(processed_file[1])

                d1 = st.download_button(
                    label="Descargar archivo BLE",
                    data=output_file_ble,
                    file_name=new_file_name_ble,
                    mime="text/csv",
                    type="primary",
                )
                d2 = st.download_button(
                    label="Descargar archivo RFID",
                    data=output_file_rfid,
                    file_name=new_file_name_rfid,
                    mime="text/csv",
                    type="primary",
                )
                st.write("**BLE**")
                st.dataframe(processed_file[0])

                st.write("**RFID**")
                st.dataframe(processed_file[1])

            else:
                output_file = utils.convert_df(processed_file)

                new_file_name = f"Crate_RFID_provisioning_{current_date}.csv"
                st.download_button(
                    label="Descargar archivo",
                    data=output_file,
                    file_name=new_file_name,
                    mime="text/csv",
                    type="primary",
                )
                st.write("**RFID**")
                st.dataframe(processed_file)
            st.success("Se han procesado los archivos!")

        # except  Exception as e:
        #      st.error(f"An error occurred: {e}")
