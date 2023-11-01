import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date

def pharmacy_login():
    st.title("Pharmacy Login Page")

    if "pharmacy_login" not in st.session_state:
        st.session_state.pharmacy_login = False

    if not st.session_state.pharmacy_login:
        pharmacy_id = st.text_input("Enter Pharmacist ID")
        password = st.text_input("Enter Pharmacist Password", type="password")
        btn = st.button("LOGIN")

        if btn:
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            c = mydb.cursor()
            c.execute("SELECT * FROM pharmacy")

            login_successful = False

            for row in c:
                if row[0] == pharmacy_id and row[1] == password:
                    st.session_state.pharmacy_login = True
                    login_successful = True
                    st.header("Pharmacy Login Successful")
                    break

            if not login_successful:
                st.error("Incorrect Pharmacy ID or Password")

    if st.session_state.pharmacy_login:
        choice = st.selectbox("Features", ("home", "View available medicines", "View Prescription"))

        if choice == "home":
            st.image("https://t4.ftcdn.net/jpg/00/89/89/91/360_F_89899105_UN5Bv2hYUx0TFzBdwpi8K1rkPzl3dYLx.jpg")

        elif choice == "View available medicines":
            st.subheader("Available Medicines")
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            c = mydb.cursor()
            c.execute("SELECT * FROM Medicines")
            medicines_data = c.fetchall()
            mydb.close()

            if not medicines_data:
                st.warning("No medicines available in the database.")
            else:
                search_query = st.text_input("Search for a medicine by name:")
                filtered_medicines = [medicine for medicine in medicines_data if search_query.lower() in medicine[1].lower()]
                if not filtered_medicines:
                    st.warning("No matching medicines found.")
                else:
                    columns = [i[0] for i in c.description]
                    filtered_medicines_df = pd.DataFrame(filtered_medicines, columns=columns)
                    st.dataframe(filtered_medicines_df)

        elif choice == "View Prescription":
            st.subheader("Prescriptions")

            patient_id = st.text_input("Enter Patient ID:")
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            c = mydb.cursor()

            if patient_id:
                c.execute("SELECT DISTINCT report_id, username FROM report WHERE username=%s", (patient_id,))
                report_data = c.fetchall()

                if report_data:
                    report_ids = [data[0] for data in report_data]
                    st.write(f"Prescriptions for Patient ID: {patient_id}")
                    report_id = st.selectbox("Select Report ID:", report_ids)

                    # Check if the report ID has already been prescribed
                    c.execute("SELECT report_id FROM medical_bill WHERE report_id=%s", (report_id,))
                    prescribed_report_ids = [row[0] for row in c.fetchall()]

                    if report_id in prescribed_report_ids:
                        st.warning("This report ID has already been prescribed.")
                    else:
                        selected_report = [data for data in report_data if data[0] == report_id]

                        if selected_report:
                            username = selected_report[0][1]
                            st.write(f"Selected Report ID: {report_id}")
                            st.write(f"Patient Name: {username}")

                            c.execute("SELECT report_id, doctor_id, medicine_prescribed FROM report WHERE report_id=%s", (report_id,))
                            prescriptions_data = c.fetchall()
                            if not prescriptions_data:
                                st.warning("No prescriptions available for the selected Report ID.")
                            else:
                                st.write("Prescriptions:")
                                for prescription in prescriptions_data:
                                    report_id, doctor_id, medicine_prescribed = prescription
                                    st.write(f"Doctor ID: {doctor_id}")
                                    st.write(f"Medicine Prescribed: {medicine_prescribed}")

                                    
                                    for prescription in prescriptions_data:
                                        _, _, medicine_prescribed = prescription
                                        st.write(f"Prescribe Medicine: {medicine_prescribed}")
                                        prescribed_amount = st.number_input("Enter Amount:", min_value=0.01)
                                        payment_confirmed = st.checkbox("Confirm Payment")

                                        if payment_confirmed and st.button("Prescribe"):
                                            today = date.today().strftime("%Y-%m-%d")

                                            # Insert prescribed medicine into the medical_bill table
                                            c.execute("INSERT INTO medical_bill (report_id, username, medicine_prescribed, amount,bill_date) VALUES (%s,%s, %s, %s, %s)",
                                                      (report_id, username, medicine_prescribed, prescribed_amount,today))
                                            mydb.commit()
                                            st.success(f"Prescribed {medicine_prescribed} with amount {prescribed_amount} successfully.")

                            st.write("")  
                        else:
                            st.warning("Report ID not found for the specified patient.")
                else:
                    st.warning("No reports found for the specified patient.")
            else:
                st.warning("Please enter a Patient ID.")

            mydb.close()

        btn_logout_pharmacy = st.button("LOGOUT")
        if btn_logout_pharmacy:
            st.session_state.pharmacy_login = False

