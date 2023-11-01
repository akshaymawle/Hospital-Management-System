import streamlit as st
import mysql.connector
import datetime
import uuid
import pandas as pd

def inpatient_dept():
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
        choice = st.selectbox("Admin Features", (" ", "Add to In-Patient Department", "View Admitted and Discharged Patients", "Discharge Patient", "Pay Patient Bill"))
        if choice == " ":
            st.header("ADMIN SECTION")
        elif choice == "Add to In-Patient Department":
            inpatientid = str(uuid.uuid4())
            username = st.text_input("Enter patient username")
            room_number = st.text_input("Enter a room number")
            admission_date = st.date_input("Admission Date")
            btn7 = st.button("ADD")
            if btn7:
                mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
                c = mydb.cursor()
                c.execute("SELECT * FROM in_patient WHERE room_number = %s AND discharge_date IS NULL", (room_number,))
                room_occupied = c.fetchone()
                c.execute("SELECT * FROM in_patient WHERE username = %s AND discharge_date IS NULL", (username,))
                patient_admitted = c.fetchone()
                if room_occupied:
                    st.error(f"Room {room_number} is already occupied. Please choose another room.")
                elif patient_admitted:
                    st.error(f"Patient {username} is already admitted. You cannot admit the same patient again.")
                else:
                    c.execute("INSERT INTO in_patient (inpatientid, username, room_number, admission_date, discharge_date, payment_status) VALUES (%s, %s, %s, %s, %s, %s)",
                              (inpatientid, username, room_number, admission_date, None, "Unpaid"))
                    mydb.commit()
                    st.header("Patient added to in-patient department")
                    st.write("Patient information added successfully.")

        elif choice == "Discharge Patient":
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            c = mydb.cursor()
            c.execute("SELECT username FROM in_patient WHERE discharge_date IS NULL")
            admitted_patients = [row[0] for row in c.fetchall()]

            selected_patient = st.selectbox("Select patient to discharge", admitted_patients)
            discharge_date = st.date_input("Discharge Date")
            btn_discharge = st.button("DISCHARGE")
            if btn_discharge:
                if selected_patient:
                    c.close()
                    c = mydb.cursor()
                    c.execute("SELECT admission_date FROM in_patient WHERE username = %s AND discharge_date IS NULL", (selected_patient,))
                    result = c.fetchone()
                    if result:
                        admission_date = result[0]
                        num_days = (discharge_date - admission_date).days
                        daily_rate = 2000
                        total_bill = num_days * daily_rate
                        c.close()
                        c = mydb.cursor()
                        c.execute("UPDATE in_patient SET discharge_date = %s WHERE username = %s AND discharge_date IS NULL", (discharge_date, selected_patient))
                        mydb.commit()
                        st.header("Patient discharged")
                        st.write(f"Patient {selected_patient} stayed for {num_days} days.")
                        st.write(f"Total bill: ₹{total_bill}")

                    else:
                        st.write("Patient not found, already discharged, or invalid input.")
                else:
                    st.write("Please select a patient to discharge.")

        elif choice == "Pay Patient Bill":
            st.subheader("Pay Patient Bill")
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            c = mydb.cursor()
            c.execute("SELECT username, admission_date, discharge_date, payment_status FROM in_patient WHERE payment_status = %s", ("Unpaid",))
            unpaid_bills = c.fetchall()
            if unpaid_bills:
                st.write("Unpaid Bills:")
                for bill in unpaid_bills:
                    username, admission_date, discharge_date, payment_status = bill
                    st.write(f"Patient: {username}, Admission Date: {admission_date}, Discharge Date: {discharge_date}")
                    payment_confirm = st.checkbox(f"Confirm payment for {username}")
                    if payment_confirm:
                        c.close()
                        c = mydb.cursor()
                        c.execute("UPDATE in_patient SET payment_status = %s WHERE username = %s AND admission_date = %s AND discharge_date = %s",
                                  ("Paid", username, admission_date, discharge_date))
                        mydb.commit()
                        st.success(f"Payment for {username} has been confirmed and marked as Paid.")
            else:
                st.write("No unpaid bills found.")

       

        elif choice == "View Admitted and Discharged Patients":
            st.subheader("View Admitted and Discharged Patients")
            view_option = st.selectbox("View Option", ["All Patients", "Admitted Patients", "Discharged Patients"])
            selected_date = st.date_input("Select a date")


            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            c = mydb.cursor()

            if view_option == "All Patients":
                c.execute("""
                    SELECT 
                        in_patient.username, 
                        in_patient.admission_date, 
                        in_patient.discharge_date,
                        in_patient.room_number,
                        in_patient.payment_status
                    FROM 
                        in_patient
                    WHERE 
                        in_patient.admission_date <= %s
                """, (selected_date,))
            elif view_option == "Admitted Patients":
                c.execute("""
                    SELECT 
                        in_patient.username, 
                        in_patient.admission_date, 
                        in_patient.discharge_date,
                        in_patient.room_number,
                        in_patient.payment_status
                    FROM 
                        in_patient
                    WHERE 
                        in_patient.admission_date <= %s
                        AND in_patient.discharge_date IS NULL
                """, (selected_date,))
            elif view_option == "Discharged Patients":
                c.execute("""
                    SELECT 
                        in_patient.username, 
                        in_patient.admission_date, 
                        in_patient.discharge_date,
                        in_patient.room_number,
                        in_patient.payment_status
                    FROM 
                        in_patient
                    WHERE 
                        in_patient.admission_date <= %s
                        AND in_patient.discharge_date IS NOT NULL
                """, (selected_date,))

            data = c.fetchall()
            df = pd.DataFrame(data, columns=["Patient Name", "Admission Date", "Discharge Date", "Room Number", "Payment Status"])
            st.dataframe(df, width=1000, height=500)











    btn_logout_admin = st.button("LOGOUT (Admin)")
    if btn_logout_admin:
        st.session_state.admin_login = False

