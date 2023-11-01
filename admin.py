import streamlit as st
import pandas as pd
import mysql.connector
import datetime



def admin_login():
    st.title("Admin Login Page")

    if "admin_login" not in st.session_state:
        st.session_state.admin_login = False

    if not st.session_state.admin_login:
        admin_id = st.text_input("Enter Admin ID")
        password = st.text_input("Enter Admin Password", type="password")
        btn = st.button("LOGIN")

        if btn:
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            c = mydb.cursor()
            c.execute("SELECT * FROM admins")

            login_successful = False

            for row in c:
                if row[0] == admin_id and row[1] == password:
                    st.session_state.admin_login = True
                    login_successful = True
                    st.header("Admin Login Successful")
                    break

            if not login_successful:
                st.error("Incorrect Admin ID or Password")

    if st.session_state.admin_login:
        choice = st.selectbox("Admin Features", (" ", "View Appointments", "View Appointments by Patient", "View Appointments by Doctor","Doctor Payments","Medical Payments","Lab Payments"))
        if choice == " ":
            st.header("ADMIN SECTION")
        elif choice == "View Appointments":
            selected_date = st.date_input("Select a Date", datetime.date.today())
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            c = mydb.cursor()
            c.execute(
                """
                SELECT appointment.appointment_id, appointment.doctor_id, appointment.username, appointment.appointment_time, appointment.a_date, 
                appointment.status
                FROM appointment
                WHERE appointment.a_date = %s
                """,
                (selected_date,),
            )






            appointment_data = c.fetchall()
            if appointment_data:
                df = pd.DataFrame(appointment_data, columns=[i[0] for i in c.description])

                df['appointment_time'] = pd.to_datetime(df['appointment_time'])
                df = df.sort_values(by='appointment_time')
                st.dataframe(df)
                

            else:
                st.write("No appointments found for the selected date.")

        elif choice == "View Appointments by Patient":
            selected_patient = st.text_input("Enter patient username to view appointments")
            selected_date = st.date_input("Select a Date", datetime.date.today())
            if selected_patient:
                mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
                c = mydb.cursor()
                c.execute("SELECT * FROM appointment WHERE username = %s AND DATE(appointment_time) = %s", (selected_patient, selected_date))
                appointment_data = c.fetchall()
                if appointment_data:
                    df = pd.DataFrame(appointment_data, columns=c.column_names)
                    df['appointment_time'] = pd.to_datetime(df['appointment_time'])
                    df = df.sort_values(by='appointment_time')
                    st.dataframe(df)
                else:
                    st.write(f"No appointments found for patient {selected_patient} on the selected date.")
            else:
                st.write("Please enter the patient's username.")

        elif choice == "View Appointments by Doctor":
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            c = mydb.cursor()
            c.execute("SELECT doctor_id, doctor_name FROM doctors")
            

            doctor_data = c.fetchall()
            doctor_ids_and_names = {f"{row[0]} - {row[1]}": row[0] for row in doctor_data}

            selected_doctor = st.selectbox("Select Doctor", list(doctor_ids_and_names.keys()))

            if selected_doctor:
                selected_doctor_id = doctor_ids_and_names[selected_doctor]
                selected_date = st.date_input("Select a Date", datetime.date.today())
                mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
                c = mydb.cursor()
                c.execute(
                    """
                    SELECT appointment.appointment_id, appointment.doctor_id, appointment.username, appointment.appointment_time, appointment.a_date, 
                    appointment.status
                    FROM appointment
                    WHERE appointment.doctor_id = %s AND appointment.a_date = %s
                    """,
                    (selected_doctor_id, selected_date),
                )


                appointment_data = c.fetchall()
                if appointment_data:
                    df = pd.DataFrame(appointment_data, columns=c.column_names)
                    df['appointment_time'] = pd.to_datetime(df['appointment_time'])
                    df = df.sort_values(by='appointment_time')
                    st.dataframe(df)
                else:
                    st.write(f"No appointments found for doctor {selected_doctor_id} on the selected date.")

        




        elif choice == "Medical Payments":
            st.subheader("Medical Payments")

            selected_month = st.text_input("Enter the month (YYYY-MM) to view Medical Payments")

            if selected_month:
                mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
                c = mydb.cursor()
                c.execute(
                    """
                    SELECT 
                        DATE_FORMAT(bill_date, '%Y-%m') AS month,
                        username,
                        SUM(amount) AS total_amount
                    FROM medical_bill
                    WHERE DATE_FORMAT(bill_date, '%Y-%m') = %s
                    GROUP BY month, username
                    """,
                    (selected_month,)
                )

                medical_payment_data = c.fetchall()
                if medical_payment_data:
                    st.write(f"Medical Payments for {selected_month}")

                    df = pd.DataFrame(medical_payment_data, columns=["Month", "Patient Name", "Total Amount"])

                    df["Total Amount"] = df["Total Amount"].apply(lambda x: "{:.2f}".format(x))

                    st.dataframe(df)

                    # Calculate and display the aggregate of all medical payments for the selected month
                    total_monthly_payments = sum(medical_payment_data[i][2] for i in range(len(medical_payment_data)))
                    formatted_total_monthly_payments = "{:.2f}".format(total_monthly_payments)
                    st.write(f"Aggregate Medical Payments for {selected_month}: Rs{formatted_total_monthly_payments}")

                else:
                    st.write(f"No medical payment data found for {selected_month}.")

                mydb.close()
            else:
                st.warning("Please enter the month (YYYY-MM) to view Medical Payments.")



        elif choice == "Doctor Payments":
            st.subheader("Doctor Payments")

            selected_month = st.text_input("Enter the month (YYYY-MM) to view Doctor Payments")

            if selected_month:
                mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
                c = mydb.cursor()
                c.execute(
                    """
                    SELECT 
                        DATE_FORMAT(report.report_date, '%Y-%m') AS month,
                        doctors.doctor_name,
                        SUM(report.fee_paid) AS total_fee_paid
                    FROM report
                    LEFT JOIN doctors ON report.doctor_id = doctors.doctor_id
                    WHERE DATE_FORMAT(report.report_date, '%Y-%m') = %s
                    GROUP BY month, doctors.doctor_name
                    """,
                    (selected_month,)
                )

                doctor_payment_data = c.fetchall()
                if doctor_payment_data:
                    st.write(f"Doctor Payments for {selected_month}")

                    df = pd.DataFrame(doctor_payment_data, columns=["Month", "Doctor Name", "Total Fee Paid"])

                    df["Total Fee Paid"] = df["Total Fee Paid"].apply(lambda x: "{:.2f}".format(x))

                    st.dataframe(df)

                    # Calculate and display the aggregate of all doctor payments for the selected month
                    total_doctor_payments = sum(doctor_payment_data[i][2] for i in range(len(doctor_payment_data)))
                    formatted_total_doctor_payments = "{:.2f}".format(total_doctor_payments)
                    st.write(f"Aggregate Doctor Payments for {selected_month}: Rs{formatted_total_doctor_payments}")

                else:
                    st.write(f"No doctor payment data found for {selected_month}.")

                mydb.close()
            else:
                st.warning("Please enter the month (YYYY-MM) to view Doctor Payments.")



        elif choice == "Lab Payments":
            st.subheader("Lab Payments")

            selected_month = st.text_input("Enter the month (YYYY-MM) to view Lab Payments")

            if selected_month:
                mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
                c = mydb.cursor()
                c.execute(
                    """
                    SELECT 
                        DATE_FORMAT(lab_test.test_date, '%Y-%m') AS month,
                        lab_test.patient_name,
                        lab_test.prescribed_tests,
                        SUM(lab_test.billing_amount) AS total_billing_amount
                    FROM lab_test
                    WHERE DATE_FORMAT(lab_test.test_date, '%Y-%m') = %s
                    GROUP BY month, lab_test.patient_name, lab_test.prescribed_tests
                    """,
                    (selected_month,)
                )

                lab_payment_data = c.fetchall()
                if lab_payment_data:
                    st.write(f"Lab Payments for {selected_month}")

                    df = pd.DataFrame(lab_payment_data, columns=["Month", "Patient Name", "Prescribed Tests", "Total Billing Amount"])

                    df["Total Billing Amount"] = df["Total Billing Amount"].apply(lambda x: "{:.2f}".format(x))

                    st.dataframe(df)

                    # Calculate and display the aggregate of all lab test payments for the selected month
                    total_lab_payments = sum(lab_payment_data[i][3] for i in range(len(lab_payment_data)))
                    formatted_total_lab_payments = "{:.2f}".format(total_lab_payments)
                    st.write(f"Aggregate Lab Payments for {selected_month}: Rs{formatted_total_lab_payments}")

                else:
                    st.write(f"No lab payment data found for {selected_month}.")

                mydb.close()
            else:
                st.warning("Please enter the month (YYYY-MM) to view Lab Payments.")






        btn_logout_admin = st.button("LOGOUT (Admin)")
        if btn_logout_admin:
            st.session_state.admin_login = False
