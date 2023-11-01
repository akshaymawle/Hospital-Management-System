import streamlit as st
import pandas as pd
import mysql.connector
import datetime

#  function to create a database connection
def create_db_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="hms"
    )
    return mydb

# Function to get a list of doctor IDs
def get_doctor_ids():
    mydb = create_db_connection()
    c = mydb.cursor()
    c.execute("SELECT doctor_id FROM doctor_table")
    doctor_ids = [row[0] for row in c.fetchall()]
    mydb.close()
    return doctor_ids

# Function to mark an appointment as complete
def mark_appointment_complete(appointment_id):
    mydb = create_db_connection()
    c = mydb.cursor()
    c.execute("UPDATE appointment SET status = 'complete' WHERE appointment_id = %s", (appointment_id,))
    mydb.commit()
    mydb.close()

# Function to get the doctor's consultation fee
def get_doctor_fee(doctor_id, default_fee=0):
    mydb = create_db_connection()
    c = mydb.cursor()
    c.execute("SELECT consultancy_fee FROM doctors WHERE doctor_id = %s", (doctor_id,))
    doctor_fee = c.fetchone()
    mydb.close()
    return doctor_fee[0] if doctor_fee else default_fee

def doctor():
    st.title("Doctor Login Page")

    #session state for the doctor's login
    if "doctor_login" not in st.session_state:
        st.session_state.doctor_login = {"login": False}

    username = st.text_input("Enter Doctor ID")
    pwd = st.text_input("Enter Password", type="password")

    btn = st.button("LOGIN")

    if btn:
        mydb = create_db_connection()
        c = mydb.cursor()
        c.execute("SELECT * FROM doctor_table")

        for row in c:
            if row[1] == username and row[2] == pwd:
                st.session_state.doctor_login['login'] = True
                st.session_state.doctor_login['doctor_id'] = row[0]
                st.success("Login Successful")
                break
        if not st.session_state.doctor_login['login']:
            st.error("Incorrect ID or Password")

    if st.session_state.doctor_login['login']:
        doctor_id = st.session_state.doctor_login['doctor_id']
        choice = st.selectbox("Features", ["home", "View Appointments", "Prescription and Report", "View Past Report of Patient", "View Test Report"])
        if choice == "home":
            st.header("Welcome")

        elif choice == "View Appointments":
            doctor_id = st.session_state.doctor_login['doctor_id']
            doctor_fee = get_doctor_fee(doctor_id, 0)  
            st.write(f"Your Fee: ₹{doctor_fee}")

            mydb = create_db_connection()
            c = mydb.cursor()

            pending_query = "SELECT * FROM appointment WHERE doctor_id = %s AND status = 'pending'"
            c.execute(pending_query, (doctor_id,))
            pending_appointments_data = []
            pending_columns = [column[0] for column in c.description]

            for row in c:
                pending_appointments_data.append(row)

            if st.checkbox("View Completed Appointments"):
                selected_date = st.date_input("Select a Date", datetime.date.today())  

                completed_query = "SELECT * FROM appointment WHERE doctor_id = %s AND status = 'complete' AND DATE(appointment_time) = %s"
                c.execute(completed_query, (doctor_id, selected_date))
                completed_appointments_data = []
                completed_columns = [column[0] for column in c.description]

                for row in c:
                    completed_appointments_data.append(row)

                if completed_appointments_data:
                    st.subheader("Completed Appointments:")
                    completed_df = pd.DataFrame(data=completed_appointments_data, columns=completed_columns)
                    st.dataframe(completed_df)
                else:
                    st.write("No completed appointments found for the specified doctor on the selected date")

            if pending_appointments_data:
                st.subheader("Pending Appointments:")
                pending_df = pd.DataFrame(data=pending_appointments_data, columns=pending_columns)
                pending_df['Mark Complete'] = [st.checkbox(f"Complete {row[0]}", key=f"complete-{row[0]}") for row in pending_appointments_data]

                marked_appointments = []  

                for index, row in pending_df.iterrows():
                    if row['Mark Complete']:
                        mark_appointment_complete(row[0])
                        marked_appointments.append(row[0])

                if marked_appointments:
                    st.success(f"Marked appointments {', '.join(map(str, marked_appointments))} as complete.")
                else:
                    st.info("No appointments were marked as complete")
            else:
                st.write("No pending appointments found for the specified doctor")


        elif choice == "Prescription and Report":
            if st.session_state.doctor_login['login']:
                st.write(f"Logged-in Doctor ID: {doctor_id}")
                mydb = create_db_connection()
                c = mydb.cursor()
                pending_query = "SELECT * FROM appointment WHERE doctor_id = %s AND status = 'pending'"
                c.execute(pending_query, (doctor_id,))
                pending_appointments_data = []

                try:
                    for row in c:
                        pending_appointments_data.append(row)

                    if not pending_appointments_data:
                        st.warning("No pending appointments found for the specified doctor.")
                    else:
                        st.write("Select a pending appointment from the dropdown:")
                        selected_appointment_id = st.selectbox("Pending Appointments", [f"Appointment ID: {row[0]}" for row in pending_appointments_data])

                        
                        selected_appointment = None
                        selected_appointment_id = selected_appointment_id.split(": ")[1]  

                        for row in pending_appointments_data:
                            if row[0] == selected_appointment_id:
                                selected_appointment = row

                        if selected_appointment:
                            st.write(f"Selected Appointment ID: {selected_appointment_id}")
                            st.write(f"Patient ID: {selected_appointment[2]}")

                            # Payment confirmation
                            payment_confirmed = st.checkbox("Payment Confirmed")

                            if payment_confirmed:
                                diagnosis = st.text_input("Diagnosis by doctor")

                                # Fetching the list of medicines from the "Medicines" table in the my sql database
                                mydb = create_db_connection()
                                c = mydb.cursor()
                                c.execute("SELECT MedicineName FROM Medicines")
                                medicines_data = c.fetchall()
                                medicines_list = [med[0] for med in medicines_data]

                                #  multi-select dropdown menu for selecting medicines
                                selected_medicines = st.multiselect("Select Medicines:", medicines_list)

                                
                                quantity_prescribed_dict = {}
                                for medicine in selected_medicines:
                                    quantity = st.number_input(f"Quantity for {medicine}", min_value=1, step=1)
                                    quantity_prescribed_dict[medicine] = quantity

                                # Fetching the list of tests from the "tests" table
                                c.execute("SELECT test_name FROM tests")
                                tests_data = c.fetchall()
                                tests_list = [test[0] for test in tests_data]

                                #  "None" as an option to the tests_list
                                tests_list.append("None")

                                selected_test = st.selectbox("Select Test Prescribed:", tests_list)

                                prescription = st.text_input("Additional prescription notes")

                                btn3 = st.button("Confirm Payment and Update Report")
                                if btn3:
                                    try:
                                        
                                        if not diagnosis or not selected_medicines or not selected_test:
                                            st.error("Please fill in all prescription details before confirming the payment.")
                                        else:
                                            mydb = create_db_connection()
                                            c = mydb.cursor()
                                            report_id = str(datetime.datetime.now())

                                            
                                            medicines_prescribed = "\n".join([f"{medicine}: {quantity}" for medicine, quantity in quantity_prescribed_dict.items()])
                                            
                                            
                                            doctor_fee = get_doctor_fee(doctor_id, 0)
                                            total_fee = doctor_fee
                                            report_date = datetime.date.today()


                                            c.execute("INSERT INTO report (report_id, doctor_id, username, diagnosis, prescription, test_prescribed, doctor_fee, medicine_prescribed, payment_status, fee_paid,report_date) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                                      (report_id, doctor_id, selected_appointment[2], diagnosis, prescription, selected_test, doctor_fee, medicines_prescribed, "confirmed", total_fee,report_date))
                                            mydb.commit()
                                            st.success("Prescription and Report Created")
                                            mark_appointment_complete(selected_appointment_id)
                                    except Exception as e:
                                        st.error(f"An error occurred while updating the report: {str(e)}")
                except IndexError:
                    st.warning("No pending appointments found for the specified doctor.")
            else:
                st.warning("Please log in as a doctor to access this feature")

        elif choice == "View Past Report of Patient":
            if st.session_state.doctor_login['login']:
                doctor_id = st.session_state.doctor_login['doctor_id']
                patient_name = st.text_input("Enter Patient's Name")

                if st.button("View Report"):
                    if patient_name:
                        mydb = create_db_connection()
                        c = mydb.cursor()
                        completed_query = "SELECT * FROM report WHERE doctor_id = %s AND username = %s"
                        c.execute(completed_query, (doctor_id, patient_name))
                        completed_reports_data = []
                        completed_columns = [column[0] for column in c.description]

                        for row in c:
                            completed_reports_data.append(row)

                        if completed_reports_data:
                            st.subheader(f"Completed Reports for {patient_name}:")
                            completed_reports_df = pd.DataFrame(data=completed_reports_data, columns=completed_columns)
                            st.dataframe(completed_reports_df)
                        else:
                            st.warning(f"No completed reports found for {patient_name}.")
                    else:
                        st.warning("Please enter the patient's name.")
            else:
                st.warning("Please log in as a doctor to access this feature")

        elif choice == "View Test Report":
            st.subheader("View Test Report")
            patient_username = st.text_input("Enter Patient Username")

            if st.button("View Report"):
                if patient_username:
                    mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
                    cursor = mydb.cursor()
                    cursor.execute("SELECT test_id, report_id, prescribed_tests, result, billing_amount FROM lab_test WHERE patient_name = %s", (patient_username,))
                    test_report_data = cursor.fetchall()

                    if test_report_data:
                        st.subheader("Test Reports")

                        for row in test_report_data:
                            st.write(f"report_id: {row[1]}")
                            st.write(f"Test ID: {row[0]}")
                            st.write(f"Prescribed Tests: {row[2] if row[2] is not None else 'N/A'}")
                            st.write(f"Test Result: {row[3] if row[3] is not None else 'N/A'}")
                            st.write(f"Billing Amount: ${row[4]:.2f}" if row[4] is not None else 'N/A')
                            st.write("-" * 50)
                    else:
                        st.write("No test reports found for the specified patient username")
                else:
                    st.write("Please enter a patient username.")

    btn2 = st.button("LOGOUT")

    if btn2:
        st.session_state.doctor_login['login'] = False

