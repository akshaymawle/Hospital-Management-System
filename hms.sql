create database hms;
use hms;

create table patients(mailid varchar (255),
username varchar (255),
passwordd varchar (255),
primary key (username));

select * from patients;
delete from patients where username='amol03';
delete from patients where username='Kajal14';


create table doctors(doctor_id varchar (255),
doctor_name varchar (255),
qualification varchar(255),
specialty varchar (255),
consultancy_fee int,
primary key (doctor_id));
drop table doctors;

create table doctor_table(doctor_id varchar (255),
username varchar (255),
passwordd varchar (255),
primary key (doctor_id));
drop table doctor_table;

insert into doctor_table values("2000","Shubhash2000","Shubhash@2000");
insert into doctor_table values("2001","Juber2001","Juber@2001");
insert into doctor_table values("2002","Rushikesh2002","Rushikesh@2002");
insert into doctor_table values("2003","Rutuja2003","Rutuja@2003");
insert into doctor_table values("2004","Priyanka2004","Priyanka@2004");
insert into doctor_table values("2005","Karthik2005","Karthik@2005");
insert into doctor_table values("2006","Muskan2006","Muskan@2006");
insert into doctor_table values("2007","Kiran2007","Kiran@2007");

insert into doctors values("2000","Dr.Shubhash","BHMS","GeneralPhysician",1000);
insert into doctors values("2001","Dr.Juber","MBBS","Dermatologist",1000);
insert into doctors values("2002","Dr.Rushikesh","MD","Opthamologist",1000);
insert into doctors values("2003","Dr.Rutuja","MD","Gynacologist",1000);
insert into doctors values("2004","Dr.Priyanka","MD","Neurosurgeon",1000);
insert into  doctors values("2005","Dr.Karthik","MD","ENT",1000);
insert into doctors values("2006","Dr.Muskan","BDS","Dentist",1000);
insert into doctors  values("2007","Dr.Kiran","MD","Ortho",1000);

CREATE TABLE appointment (
    appointment_id VARCHAR(255) PRIMARY KEY,
    doctor_id VARCHAR(255),
    username VARCHAR(255),
    FOREIGN KEY (username) REFERENCES patients(username)
);
select * from appointment;
drop table appointment;



create table report(
report_id varchar (255) primary key,
doctor_id varchar (255),
username varchar (255),
diagnosis varchar(255),
prescription varchar(255),
test_prescribed varchar(255)
);
ALTER TABLE report ADD COLUMN doctor_fee DECIMAL(10, 2);
alter table report add column fee_paid int;
ALTER TABLE report add column payment_status BOOLEAN;
ALTER TABLE report MODIFY payment_status VARCHAR(255);


select * from report;
drop table report;


CREATE TABLE appointment (
    appointment_id varchar(255) PRIMARY KEY,
    doctor_id varchar(255),
    username varchar(255),
    appointment_date DATE,
    status ENUM('pending', 'complete') DEFAULT 'pending'
);
drop table appointment;
CREATE TABLE appointment (
    appointment_id VARCHAR(255) PRIMARY KEY,
    doctor_id INT,
    username VARCHAR(255),
    appointment_time DATETIME,
    a_date date,
	status ENUM('pending', 'complete') DEFAULT 'pending'
);
ALTER TABLE appointment
ADD a_date DATE;
ALTER TABLE appointment
MODIFY appointment_time DATETIME;

drop table appointment;
select * from appointment;

CREATE TABLE admins (
    admin_id VARCHAR(255) primary key,
    pwd VARCHAR(255));

INSERT INTO admins  VALUES ('Meera', 'Meera@07');
INSERT INTO admins  VALUES ('Shubham21', 'Shubham@21');

CREATE TABLE in_patient (
    inpatientid varchar(255)primary key,
    username varchar(255),
    room_number varchar(255),
    admission_date date ,
    discharge_date date,
    payment_status varchar(255)
);
ALTER TABLE in_patient
ADD CONSTRAINT fk_username
FOREIGN KEY (username)
REFERENCES patients(username);



select * from in_patient;
drop table in_patient;
CREATE TABLE doctor_fee (
    doctor_id varchar(255) PRIMARY KEY,
    fee INT
);
insert into doctor_fee values("2000","1000")
select * from doctor_fee;
drop table doctor_fee;
CREATE TABLE billing (
    billing_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    admission_date DATE,
    discharge_date DATE,
    total_bill DECIMAL(10, 2),
    payment_status BOOLEAN
);
select * from billing;
drop table billing;

create table pharmacy(
	username varchar (255),
    pwd varchar(255)
);
insert into pharmacy values ("Ganesh09","Ganesh@09")

CREATE TABLE Medicines (
    MedicineID INT PRIMARY KEY,
    MedicineName VARCHAR(255),
    Manufacturer VARCHAR(255),
    ExpiryDate DATE,
    Quantity INT,
    UnitPrice DECIMAL(10, 2)
);

select * from Medicines;
INSERT INTO Medicines (MedicineID, MedicineName, Manufacturer, ExpiryDate,Quantity, UnitPrice) VALUES
(1, 'Aspirin', 'Bayer', '2024-12-31', 100, 5.99),
(2, 'Ibuprofen', 'Advil', '2024-10-15', 75, 6.49),
(3, 'Lipitor', 'Pfizer', '2025-05-20', 60, 15.99),
(4, 'Amoxicillin', 'Generic', '2023-08-01', 50, 7.99),
(5, 'Paracetamol', 'Tylenol', '2024-09-30', 120, 4.99),
(6, 'Omeprazole', 'AstraZeneca', '2025-03-15', 90, 9.99),
(7, 'Ventolin', 'GlaxoSmithKline', '2024-11-10', 40, 12.99),
(8, 'Zyrtec', 'Johnson & Johnson', '2024-07-05', 70, 8.99),
(9, 'Insulin', 'Novo Nordisk', '2023-12-20', 30, 25.99),
(10, 'Atorvastatin', 'Lupin', '2024-08-25', 55, 13.99);

CREATE TABLE report (
    report_id VARCHAR(255) PRIMARY KEY,
    doctor_id VARCHAR(255),
    username VARCHAR(255),
    diagnosis VARCHAR(255),
    prescription VARCHAR(255),
    test_prescribed VARCHAR(255),
    doctor_fee DECIMAL(10, 2),
    medicine_prescribed VARCHAR(255),
    quantity_prescribed INT,
    INDEX idx_report_id (report_id),
    INDEX idx_username (username),
    INDEX idx_test_prescribed (test_prescribed)
);
ALTER TABLE report
ADD report_date DATE;

ALTER TABLE report
ADD COLUMN fee_paid INT;

ALTER TABLE report
MODIFY payment_status BOOLEAN;
ALTER TABLE report
Add column payment_status VARCHAR(255);

select * from report;
drop table report;


CREATE TABLE tests (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    test_name VARCHAR(255),
    test_date DATE,
    doctor_id INT,
    technician_id INT,
    test_result VARCHAR(50),
    test_notes TEXT,
    billing_amount DECIMAL(10, 2)
);


INSERT INTO tests (patient_id, test_name, test_date, doctor_id, technician_id, test_result, test_notes, billing_amount) VALUES
(1, 'Blood Test', '2023-10-01', 3, 5, 'Normal', 'Complete blood count.', 150.00),
(2, 'X-Ray', '2023-10-02', 2, 6, 'Abnormal', 'Fractured wrist.', 250.00),
(3, 'MRI', '2023-10-03', 1, 4, 'Positive', 'Brain tumor detected.', 500.00),
(4, 'Ultrasound', '2023-10-04', 3, 5, 'Normal', 'Pregnancy scan.', 200.00),
(5, 'EKG', '2023-10-05', 2, 6, 'Abnormal', 'Irregular heartbeat.', 180.00),
(6, 'CT Scan', '2023-10-06', 1, 4, 'Normal', 'Lung scan.', 300.00),
(7, 'Urinalysis', '2023-10-07', 4, 7, 'Normal', 'Routine test.', 80.00),
(8, 'Colonoscopy', '2023-10-08', 2, 5, 'Abnormal', 'Polyp detected.', 400.00),
(9, 'Mammogram', '2023-10-09', 3, 6, 'Normal', 'Breast scan.', 160.00),
(10, 'Stress Test', '2023-10-10', 1, 4, 'Normal', 'Heart evaluation.', 220.00);

CREATE TABLE medical_bill AS
SELECT report_id, username, medicine_prescribed, NULL AS amount
FROM report;

select* from medical_bill;
drop table medical_bill;
CREATE TABLE medical_bill (
    report_id varchar(255),
    username VARCHAR(255),
    medicine_prescribed VARCHAR(255),
    amount DECIMAL(10,2),
    bill_date date
);
ALTER TABLE medical_bill
ADD bill_date DATE;

select * from medical_bill;
create table lab(
	username varchar(255),
	pwd varchar(255)
);
insert into lab values ("Safiya","Safiya@02")
    
select * from lab;


CREATE TABLE lab_test (
    test_id varchar(255) AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(255),
    prescribed_tests TEXT,
    result TEXT
);
drop table lab_test;
CREATE TABLE lab_test (
    test_id VARCHAR(255) PRIMARY KEY,
    report_id varchar(255),
    patient_name VARCHAR(255),
    prescribed_tests varchar(255),
    result TEXT,
    billing_amount decimal(10,2)
);
ALTER TABLE lab_test MODIFY test_id VARCHAR(255) NOT NULL DEFAULT 'N/A';
ALTER TABLE lab_test ADD billing_amount DECIMAL(10, 2);
ALTER TABLE lab_test
ADD test_date DATE;
select * from lab_test;
drop table lab_test;