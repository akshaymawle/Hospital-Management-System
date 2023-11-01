import streamlit as st
import pandas as pd
import mysql.connector
import uuid
from datetime import date,datetime

def lab_login():
    st.title("Login Page")

    if "lab_login" not in st.session_state:
        st.session_state.lab_login = False

    if not st.session_state.lab_login:
        username = st.text_input("Enter lab ID")
        password = st.text_input("Enter Password", type="password")
        btn = st.button("LOGIN")

        if btn:
            with mysql.connector.connect(host="localhost", user="root", password="1234", database="hms") as mydb:
                with mydb.cursor() as c:
                    c.execute("SELECT * FROM lab")

                    login_successful = False

                    for row in c:
                        if row[0] == username and row[1] == password:
                            st.session_state.lab_login = True
                            st.session_state.lab_username = username
                            login_successful = True
                            st.header("Login Successful")
                            break

                    if not login_successful:
                        st.error("Incorrect ID or Password")

    if st.session_state.lab_login:
        choice = st.selectbox("Features", ("home", "Test_Report", "View Billing Amount"))

        if choice == "home":
            st.image("https://t4.ftcdn.net/jpg/02/11/04/53/360_F_211045328_HnemU2NVFNwDWnQtDi5JHeHVhMV1jTOr.jpg")

        elif choice == "Test_Report":
            st.header("View Reports")
            patient_id = st.text_input("Enter Patient ID to filter reports")

            if patient_id:
                with mysql.connector.connect(host="localhost", user="root", password="1234", database="hms") as mydb:
                    with mydb.cursor() as c:
                        c.execute("SELECT report_id, username, doctor_id, test_prescribed FROM report WHERE username = %s", (patient_id,))
                        reports = c.fetchall()

                        if not reports:
                            st.warning("No reports available for the entered Patient ID.")
                        else:
                            report_ids = [report[0] for report in reports]
                            selected_report_id = st.selectbox("Select Report", report_ids)

                            if selected_report_id:
                                for report in reports:
                                    if report[0] == selected_report_id:
                                        st.write(f"Report ID: {report[0]}")
                                        st.write(f"Patient Name: {report[1]}")
                                        st.write(f"Doctor Name: {report[2]}")
                                        st.write(f"Tests Prescribed: {report[3]}")

                                        # Checks if a result for this report ID exists
                                        c.execute("SELECT result FROM lab_test WHERE report_id = %s", (report[0],))
                                        existing_result = c.fetchone()

                                        if not existing_result:
                                            # If a result doesn't exist then  updating
                                            with mydb.cursor() as c_tests:
                                                c_tests.execute("SELECT test_name, billing_amount FROM tests WHERE test_name = %s", (report[3],))
                                                test_data = c_tests.fetchone()

                                            if test_data:
                                                selected_test_name = test_data[0]
                                                test_amount = test_data[1]
                                                text_area_key = f"text_area_{report[0]}"
                                                result = st.text_area(f"Result for {selected_test_name}", key=text_area_key)

                                                checkbox_key = f"checkbox_{report[0]}"
                                                payment_confirmed = st.checkbox("Confirm Payment", key=checkbox_key)

                                                update_button_key = f"update_button_{report[0]}"
                                                update_button = st.button("Update Result", key=update_button_key)

                                                if update_button and result and payment_confirmed:
                                                    test_id = str(uuid.uuid4())
                                                    patient_name = report[1]
                                                    test_date = date.today()

                                                    with mydb.cursor() as c_update:
                                                        c_update.execute("INSERT INTO lab_test (test_id, report_id, patient_name, prescribed_tests, result, billing_amount,test_date) VALUES (%s, %s, %s, %s, %s, %s,%s)",
                                                            (test_id, report[0], patient_name, report[3], result, test_amount,test_date))
                                                    mydb.commit()
                                                    st.success("Result updated and added to the database. Test ID: " + test_id)
                                                elif not result:
                                                    st.error("Please fill in the result.")
                                                elif not payment_confirmed:
                                                    st.error("Please confirm payment before updating the result.")

                                        else:
                                            st.write("Result for this report already exists and cannot be updated.")

        elif choice == "View Billing Amount": #displays billing amout for different test
            st.header("View Billing Amount")
            with mysql.connector.connect(host="localhost", user="root", password="1234", database="hms") as mydb:
                with mydb.cursor() as c:
                    c.execute("SELECT test_name, billing_amount FROM tests")
                    test_data = c.fetchall()

            billing_df = pd.DataFrame(test_data, columns=["Test Name", "Billing Amount"])

            st.dataframe(billing_df)

            btn_logout = st.button("LOGOUT")
            if btn_logout:
                st.session_state.lab_login = False


        btn_logout_lab = st.button("LOGOUT")
        if btn_logout_lab:
            st.session_state.lab_login = False

