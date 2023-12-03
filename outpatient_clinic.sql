create database Outpatient_Clinic;
use Outpatient_Clinic;

#Outpatient clinic

CREATE TABLE patient (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    age INT NOT NULL,
    gender CHAR(1) NOT NULL CHECK (gender IN ('M', 'F', 'O')),
    address VARCHAR(100) NOT NULL,
    phone_number VARCHAR(25) NOT NULL,
    INDEX(patient_id)
    
)AUTO_INCREMENT = 1000;

CREATE TABLE doctor (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    specialty VARCHAR(30) NOT NULL,
    INDEX(doctor_id)
)AUTO_INCREMENT = 2000;

CREATE TABLE insurance (
    insurance_id INT PRIMARY KEY AUTO_INCREMENT,
    provider_id INT NOT NULL,
    provider_name VARCHAR(40),
    policy_number VARCHAR(50),
    INDEX(insurance_id)
    -- CONSTRAINT constraint_insurance_provider_id FOREIGN KEY (provider_id) REFERENCES provider(provider_id) ON DELETE CASCADE ON UPDATE CASCADE
)AUTO_INCREMENT = 3000;

CREATE TABLE patient_insurance (
    patient_id INT NOT NULL,
    insurance_id INT NOT NULL,
    PRIMARY KEY (patient_id, insurance_id),
    INDEX(patient_id,insurance_id),
    CONSTRAINT constraint_patient_insurance_patient_id FOREIGN KEY (patient_id) REFERENCES patient(patient_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT constraint_patient_insurance_insurance_id FOREIGN KEY (insurance_id) REFERENCES insurance(insurance_id) ON DELETE CASCADE ON UPDATE CASCADE
    
)AUTO_INCREMENT = 4000;


CREATE TABLE prescriptions (
    prescription_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    medication_name VARCHAR(50) NOT NULL,
    dosage VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    INDEX(prescription_id),
    CONSTRAINT constraint_prescriptions_patient_id FOREIGN KEY (patient_id) REFERENCES patient(patient_id) ON DELETE CASCADE ON UPDATE CASCADE
)AUTO_INCREMENT = 5000;

CREATE TABLE appointment (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    appointment_date DATETIME NOT NULL,
    doctor_id INT NOT NULL,
    reason VARCHAR(300) NOT NULL,
    INDEX(appointment_id),
    CONSTRAINT constraint_appointment_patient_id FOREIGN KEY (patient_id) REFERENCES patient(patient_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT constraint_appointment_doctor_id FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id) ON DELETE CASCADE ON UPDATE CASCADE
)AUTO_INCREMENT = 6000;

CREATE TABLE medical_history (
    medical_history_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    medical_condition VARCHAR(300) NOT NULL,
    date_diagnosed DATE NOT NULL,
    treatment VARCHAR(300) NOT NULL,
    INDEX(medical_history_id),
    CONSTRAINT constraint_medical_history_patient_id FOREIGN KEY (patient_id) REFERENCES patient(patient_id) ON DELETE CASCADE ON UPDATE CASCADE
)AUTO_INCREMENT = 7000;

CREATE TABLE billing (
    billing_id INT PRIMARY KEY AUTO_INCREMENT,
    appointment_id INT NOT NULL,
    amount DECIMAL(11, 2) NOT NULL,
    payment_date DATETIME NOT NULL,
    INDEX(billing_id),
    CONSTRAINT constraint_billing_appointment_id FOREIGN KEY (appointment_id) REFERENCES appointment(appointment_id) ON DELETE CASCADE ON UPDATE CASCADE
)AUTO_INCREMENT = 8000;

CREATE TABLE user(
	username varchar(20),
	userpassword varchar(100),
	user_is varchar(20) NOT NULL CHECK (user_is IN ('DOCTOR','PATIENT')),
    user_id INT,
    INDEX(user_id)
);
DELIMITER //
CREATE PROCEDURE getuser_id(IN userid INT)
BEGIN
    DECLARE uid INT DEFAULT -1;
    
    -- set the value of uid
    SET uid = userid;
    
    -- select the value of uid as a result set
    SELECT uid;
END //
DELIMITER ;



# function 

DELIMITER //

CREATE PROCEDURE list_patients_by_diagnosis(
    IN diagnosis VARCHAR(300)
)
BEGIN
    SELECT p.first_name, p.last_name, p.age, p.gender, p.address, p.phone_number
    FROM patient p
    JOIN medical_history mh ON p.patient_id = mh.patient_id
    WHERE mh.medical_condition LIKE CONCAT('%', diagnosis, '%');
END //

DELIMITER ;

call list_patients_by_diagnosis('Hypertension');


DELIMITER //

CREATE PROCEDURE patients_visited_on_days(
    IN start_date DATE,
    IN end_date DATE
)
BEGIN
    SELECT *
    FROM patient
    WHERE patient_id IN (
        SELECT DISTINCT appointment.patient_id
        FROM appointment
        WHERE appointment_date BETWEEN start_date AND end_date
    );
END //

DELIMITER ;
call patients_visited_on_days('2023-01-15','2023-03-10');

DELIMITER //

CREATE PROCEDURE patients_seen_by_doctor(
    IN doctor_name VARCHAR(40)
)
BEGIN
    SELECT *
    FROM patient
    WHERE patient_id IN (
        SELECT DISTINCT appointment.patient_id
        FROM appointment
        INNER JOIN doctor ON appointment.doctor_id = doctor.doctor_id
        WHERE doctor.last_name = doctor_name
    );
END //

DELIMITER ;
call patients_seen_by_doctor('Williams');


DELIMITER //

CREATE PROCEDURE diagnoses_of_patients_visited_shortinterval (IN duration INT)
BEGIN
	SELECT distinct p.first_name, p.last_name, m.medical_condition
	FROM patient p
	INNER JOIN appointment a1 ON p.patient_id = a1.patient_id
	INNER JOIN appointment a2 ON p.patient_id = a2.patient_id AND a1.appointment_id != a2.appointment_id
	INNER JOIN medical_history m ON p.patient_id = m.patient_id
	WHERE DATEDIFF(a2.appointment_date,a1.appointment_date) <= duration
	and a1.appointment_date <= a2.appointment_date
	ORDER BY p.last_name, p.first_name;
END //
DELIMITER ;

CALL diagnoses_of_patients_visited_shortinterval(180);#in days










