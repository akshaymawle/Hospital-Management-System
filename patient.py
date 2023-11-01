import streamlit as st
import pandas as pd
import mysql.connector
import datetime




def patient_login():
    st.title("Patient Login Page")
    
    
    if "patient_login" not in st.session_state: # i have separate session state for each module...that is separate for patient,doctor,admin etc.
        st.session_state.patient_login = False

    
    if not st.session_state.patient_login:
        username = st.text_input("Enter patient ID")
        password = st.text_input("Enter Your Password", type="password")
        btn = st.button("LOGIN")

        if btn:
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            c = mydb.cursor()
            c.execute("SELECT * FROM patients")
            
            login_successful = False

            for row in c:
                if row[1] == username and row[2] == password:
                    st.session_state.patient_login = True
                    st.session_state.patient_username = username  
                    login_successful = True
                    st.header("Patient Login Successful")
                    break

            if not login_successful:
                st.error("Incorrect ID or Password")
    if st.session_state.patient_login:
        choice2 = st.selectbox("Features", ("home", "View available doctors", "Book an appointment","Cancel Appointment", "View Report","View Test Report","Payment Status","View Medical Bill"))

        if choice2=="home":
            if st.session_state.patient_login:
                patient_name = st.session_state.patient_username  
                st.header(f"Welcome {patient_name}")
            st.image("https://www.shutterstock.com/image-photo/doctor-holding-card-text-welcome-260nw-1851536281.jpg")


        elif choice2 == "View available doctors":
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            c = mydb.cursor()
            c.execute("select * from doctors")
            mydata = []
            mycolumns = c.column_names
            for row in c:
                mydata.append(row)
            st.dataframe(pd.DataFrame(data=mydata, columns=mycolumns))

        elif choice2 == "Book an appointment":
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            c = mydb.cursor()
            c.execute("SELECT doctor_id, doctor_name, specialty, consultancy_fee FROM doctors")
            doctor_data = c.fetchall()
            doctor_options = [f"ID: {row[0]}, Name: {row[1]}, Specialty: {row[2]}, Fee: Rs{row[3]}" for row in doctor_data]
            selected_doctor_option = st.selectbox("Choose Doctor", doctor_options)
            selected_doctor_id = int(selected_doctor_option.split(',')[0].split(': ')[1])
            a_date = st.date_input("Select Appointment Date", min_value=datetime.date.today(), key="appointment_date")

            selected_doctor = None
            for row in doctor_data:
                if row[0] == selected_doctor_id:
                    selected_doctor = row
            if selected_doctor:
                st.write(f"Doctor ID: {selected_doctor[0]}")
                st.write(f"Doctor Name: {selected_doctor[1]}")
                st.write(f"Specialty: {selected_doctor[2]}")
                st.write(f"Consultancy Fee: Rs{selected_doctor[3]}",)

            username = st.session_state.patient_username
            appointment_datetime = st.date_input("Select Appointment Date", min_value=datetime.date.today(), key="appointment_date_2")
            appointment_time = st.time_input("Select Appointment Time")

            doctor_id = selected_doctor_id

            btn3 = st.button("Book an appointment")
            if btn3:
                if is_valid_appointment_time(appointment_time): # i have  created function for this....at the end of this code
                    mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
                    c = mydb.cursor()
                    appointment_time = datetime.datetime.combine(appointment_datetime, appointment_time)
                    appointment_id = str(datetime.datetime.now())
                    appointment_data = (appointment_id, doctor_id, username, appointment_time, a_date)  
                    c.execute("INSERT INTO appointment (appointment_id, doctor_id, username, appointment_time, a_date) VALUES (%s, %s, %s, %s, %s)", appointment_data)  # Add 'a_date' to the SQL query
                    mydb.commit()
                    st.header("Appointment Successful")
                else:
                    st.error("Appointment time must be between 10 AM and 8 PM")






        elif choice2 == "View Report":
            username = st.session_state.patient_username
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM report WHERE username = %s", (username,))
            report_data = cursor.fetchall()
            if report_data:
                st.subheader("Your Report")
                selected_report_id = st.selectbox("Select Report:", [row[0] for row in report_data])
                for row in report_data:
                    if row[0] == selected_report_id:
                        
                        st.write(f"Report ID: {row[0]}")
                        st.write(f"Doctor ID: {row[1]}")
                        st.write(f"Diagnosis: {row[3]}")
                        st.write(f"Prescription: {row[4]}")
                        st.write(f"Test Prescribed: {row[5]}")
                        st.write(f"Medicine Prescribed: {row[7]}")
                        st.write(f"report_date: {row[11]}")
            else:
                st.write("No report found for the given Patient ID")

        
        elif choice2 == "Payment Status":
            uid = st.session_state.patient_username
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            cursor = mydb.cursor()
            cursor.execute("SELECT report_id, doctor_id, doctor_fee,payment_status,fee_paid,report_date FROM report WHERE username = %s", (uid,))
            payment_data = cursor.fetchall()

            if payment_data:
                mydata = [list(row) for row in payment_data]
                mycolumns = ["Report ID", "Doctor ID", "Doctor Fee","payment_status","Fee Paid","Report Date"]
                st.dataframe(pd.DataFrame(data=mydata, columns=mycolumns))
                st.subheader("Payment Details")
            else:
                st.write("No payment information found for the logged-in patient")


        elif choice2 == "View Medical Bill":
            username = st.session_state.patient_username
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            cursor = mydb.cursor()
            cursor.execute("SELECT report_id, medicine_prescribed, amount,bill_date FROM medical_bill WHERE username = %s", (username,))
            bill_data = cursor.fetchall()

            if bill_data:
                mydata = [list(row) for row in bill_data]
                mycolumns = ["Report ID", "Medicine Prescribed", "Amount","Bill Date"]
                st.dataframe(pd.DataFrame(data=mydata, columns=mycolumns),width=1000)
                st.subheader("Medical Bill")
            else:
                st.write("No medical bill information found for the logged-in patient")


        elif choice2 == "Cancel Appointment":
            username = st.session_state.patient_username
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            cursor = mydb.cursor()
            current_datetime = datetime.datetime.now()
            cursor.execute("SELECT appointment_id, doctor_id, appointment_time FROM appointment WHERE username = %s AND appointment_time > %s", (username, current_datetime))


            appointment_data = cursor.fetchall()
    
            if appointment_data:
                st.subheader("Your Appointments")
                selected_appointment_id = st.selectbox("Select Appointment to Cancel:", [row[0] for row in appointment_data])
        
                for row in appointment_data:
                    if row[0] == selected_appointment_id:
                        st.write(f"Appointment ID: {row[0]}")
                        st.write(f"Doctor ID: {row[1]}")
                        st.write(f"Appointment Time: {row[2]}")
                
                btn_cancel = st.button("Cancel Appointment")
                if btn_cancel:
                    for row in appointment_data:
                        if row[0] == selected_appointment_id:
                            appointment_id_to_cancel = row[0]
                            doctor_id = row[1]
                            appointment_time = row[2]
                    
                    cursor.execute("DELETE FROM appointment WHERE appointment_id = %s", (appointment_id_to_cancel,))
                    mydb.commit()
                    st.success("Appointment Canceled")
            
            
            else:
                st.write("No appointments found for the logged-in patient")


        elif choice2 == "View Test Report":
            username = st.session_state.patient_username
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
            cursor = mydb.cursor()
            cursor.execute("SELECT test_id, report_id, prescribed_tests, result, billing_amount, test_date FROM lab_test WHERE patient_name = %s", (username,))
            test_report_data = cursor.fetchall()

            if test_report_data:
                st.subheader("Test Reports")
                selected_report_id = st.selectbox("Select Report ID:", [row[1] for row in test_report_data])

                for row in test_report_data:
                    if row[1] == selected_report_id:
                        st.write(f"report_id: {row[1]}")
                        st.write(f"Test ID: {row[0]}")
                        st.write(f"Test Date: {row[5]}")  
                        st.write(f"Prescribed Tests: {row[2] if row[2] is not None else 'N/A'}") 
                        st.write(f"Test Result: {row[3] if row[3] is not None else 'N/A'}")  
                        st.write(f"Billing Amount: ${row[4]:.2f}" if row[4] is not None else 'N/A')
                        break
            else:
                st.write("No test reports found for the logged-in patient")

         
        btn_logout = st.button("LOGOUT")
        if btn_logout:
            st.session_state.patient_login = False

def is_valid_appointment_time(appointment_time): # I created this function for appointments between 10 AM to 8PM
    start_time = datetime.time(10, 0)
    end_time = datetime.time(20, 0)
    
    if start_time <= appointment_time <= end_time:
        return True
    else:
        return False
