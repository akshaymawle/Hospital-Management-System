import streamlit as st
import pandas as pd
import mysql.connector
import datetime

#i have created different modules and imported those modules in this main file.
from patient import patient_login
from admin import admin_login
from registration import register
from doctor import doctor
from inpatient import inpatient_dept
from pharmacy import pharmacy_login
from lab import lab_login

st.sidebar.image("https://www.vhv.rs/dpng/d/87-872996_hospital-logo-black-and-white-hd-png-download.png")
st.markdown("""
    <div style="display: flex; align-items: center;">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmD4crfBaJNVyWzTklVw2u1zSqUPQ71BlhmQ&usqp=CAU" alt="Hospital Logo" style="width: 50px; height: 50px; margin-right: 10px;">
        <h1 style="color: green; font-style: italic; font-weight: bold;">Hospital Management System</h1>
    </div>
""", unsafe_allow_html=True)


    
if __name__ == "__main__":
    user_type = st.sidebar.selectbox("Select User Type", ("Home","Patient", "Admin","Doctor","In-patient dept","Pharmacy","Lab Section","Register"))
    if user_type == "Home":
        st.image("https://media.istockphoto.com/id/1064981344/photo/medical-technology-concept.jpg?s=612x612&w=0&k=20&c=fn3Al6PW_ud5vYkwnHxeyFtHabG1-wAjdhk9pCn0JKk=")
        st.markdown("<p style='color: green; font-family: cursive; font-size: 24px;'>Project By Akshay Mawle</p>", unsafe_allow_html=True)
        
    elif user_type == "Patient":
        patient_login()
    elif user_type == "Admin":
        admin_login()
    elif user_type == "Register":
        register()
    elif user_type == "Doctor":
        doctor()
    elif user_type == "In-patient dept":
        inpatient_dept()
        
    elif user_type == "Pharmacy":
        pharmacy_login()

    elif user_type == "Lab Section":
        lab_login()
