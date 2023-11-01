import streamlit as st
import mysql.connector
import re

def register():
    st.header("Patient Registration page")
    mailid = st.text_input("Enter your email id")
    uid = st.text_input("Create User ID")
    pwd = st.text_input("Create a Password", type="password")
    confirm_pwd = st.text_input("Confirm Password", type="password")
    btn = st.button("Register")

    if btn:
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", mailid):
            st.warning("Please enter a valid email address.")
        elif not (any(char.isupper() for char in pwd) and any(char.islower() for char in pwd) and any(not char.isalnum() for char in pwd)):
            st.warning("Password must contain at least one capital letter, one lowercase letter, and one special character.")
        elif pwd != confirm_pwd:
            st.warning("Passwords do not match. Please re-enter the same password.")
        else:
            try:
                mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="hms")
                c = mydb.cursor()
                c.execute("insert into patients values(%s,%s,%s)", (mailid, uid, pwd))
                mydb.commit()
                st.header("User Added Successfully")
            except Exception as e:
                st.header(e)
