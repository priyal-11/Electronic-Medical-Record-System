import mysql.connector
from datetime import datetime

# Connect to the MySQL database
conn = mysql.connector.connect(
    user='root',
    password='Priyal@1101',
    host='localhost',
    database='outpatient_clinic'
)

# Create a cursor to execute SQL queries
cursor = conn.cursor(dictionary=True)
# Dummy data for registered doctors
doctors = {"john": {"password": "1234", "doctor_id": 2001}}
patient = {"priya": {"password": "abcd", "patient_id": 1007}}
patient = {"Mary": {"password": "abcd", "patient_id": 1001}}
# Dummy data for doctor's appointments
doctor_appointments = {2001: ["Appointment 1", "Appointment 2"]}

# Dummy data for doctor's medical history
medical_history = {2001: ["Medical Record 1", "Medical Record 2"]}

# Dummy data for doctor's prescriptions
prescriptions = {2000: ["Prescription 1", "Prescription 2"]}

# Function for doctor login
def doctor_login(username, password):
    if username in doctors and doctors[username]["password"] == password:
        return f"Doctor login successful. Doctor ID: {doctors[username]['doctor_id']}"
    else:
        return {"status": "error", "message": "Invalid credentials"}

def patient_login(username, password):
    if username in patient and patient[username]["password"] == password:
        return f"Patient login successful. Patient ID: {patient[username]['patient_id']}"
    else:
        return {"status": "error", "message": "Invalid credentials"}
    
 # Function for edit information of appointment   
def edit_appointment(appointment_id, appointment_date, reason):
    try:
        # Check if the appointment_id exists in the appointment table
        cursor.execute("SELECT * FROM appointment WHERE appointment_id = %s", (appointment_id,))
        appointment = cursor.fetchone()

        if not appointment:
            return "Appointment not found"

        # Update the appointment with new information
        cursor.execute(
            "UPDATE appointment SET appointment_date = %s, reason = %s WHERE appointment_id = %s",
            (appointment_date, reason, appointment_id)
        )
        conn.commit()

        return "Appointment updated successfully"
    except Exception as e:
        return f"Error: {str(e)}"

# Function to add new prescription 

def add_new_prescription(patient_id, medication_name, dosage, start_date, end_date):
    try:
        # Check if patient_id exists in the patient table
        cursor.execute("SELECT * FROM prescriptions WHERE patient_id = %s", (patient_id,))
        patient = cursor.fetchone()

        if not patient:
            return "Patient not found"

        # Add logic to insert a new record into the prescriptions table
        insert_query = "INSERT INTO prescriptions (patient_id, medication_name, dosage, start_date, end_date) VALUES (%s, %s, %s, %s, %s)"
        data = (patient_id, medication_name, dosage, start_date, end_date)
        cursor.execute(insert_query, data)
        conn.commit()

        return "Prescription added successfully"
    except Exception as e:
        return f"Error: {str(e)}"


# Function for medical history
def check_patient_medical_history(patient_id):
    cursor.execute("SELECT * FROM medical_history WHERE patient_id = %s", (patient_id,))
    medical_history_data = cursor.fetchall()
    return medical_history_data


# Function to edit prescription 
def edit_prescription(prescription_id, medication_name, dosage, start_date, end_date):
    try:
        # Check if the prescription_id exists in the prescriptions table
        cursor.execute("SELECT * FROM prescriptions WHERE prescription_id = %s", (prescription_id,))
        prescription = cursor.fetchone()

        if not prescription:
            return "Prescription not found"

        # Add logic to update the prescription in the prescriptions table
        update_query = "UPDATE prescriptions SET medication_name = %s, dosage = %s, start_date = %s, end_date = %s WHERE prescription_id = %s"
        data = (medication_name, dosage, start_date, end_date, prescription_id)
        cursor.execute(update_query, data)
        conn.commit()

        return "Prescription updated successfully"
    except Exception as e:
        return f"Error: {str(e)}"



# Function to delete prescription 

def delete_prescription(prescription_id):
    try:
        # Check if the prescription_id exists in the prescriptions table
        cursor.execute("SELECT * FROM prescriptions WHERE prescription_id = %s", (prescription_id,))
        prescription = cursor.fetchone()

        if not prescription:
            return "Prescription not found"

        # Add logic to delete the prescription from the prescriptions table
        delete_query = "DELETE FROM prescriptions WHERE prescription_id = %s"
        cursor.execute(delete_query, (prescription_id,))
        conn.commit()

        return "Prescription deleted successfully"
    except Exception as e:
        return f"Error: {str(e)}"

def get_all_appointments():
    try:
        # Retrieve all appointments from the appointment table
        cursor.execute("SELECT * FROM appointment")
        all_appointments = cursor.fetchall()

        if all_appointments:
            appointments_info = []
            for appointment in all_appointments:
                appointment_info = (
                    f"Appointment ID: {appointment['appointment_id']}, "
                    f"Patient ID: {appointment['patient_id']}, "
                    f"Appointment Date: {appointment['appointment_date']}, "
                    f"Doctor ID: {appointment['doctor_id']}, "
                    f"Reason: {appointment['reason']}"
                )
                appointments_info.append(appointment_info)

            return {"all_appointments": appointments_info}
        else:
            return {"all_appointments": "No appointments found"}
    except Exception as e:
        return f"Error: {str(e)}"

def get_all_medical_history():
    try:
        # Retrieve all medical history from the medical_history table
        cursor.execute("SELECT * FROM medical_history")
        all_medical_history = cursor.fetchall()

        if all_medical_history:
            medical_history_info = []
            for record in all_medical_history:
                record_info = (
                    f"Medical History ID: {record['medical_history_id']}, "
                    f"Patient ID: {record['patient_id']}, "
                    f"Medical Condition: {record['medical_condition']}, "
                    f"Date Diagnosed: {record['date_diagnosed']}, "
                    f"Treatment: {record['treatment']}"
                )
                medical_history_info.append(record_info)

            return {"all_medical_history": medical_history_info}
        else:
            return {"all_medical_history": "No medical history found"}
    except Exception as e:
        return f"Error: {str(e)}"


# Function for doctor-specific actions
def doctor_actions_interface(doctor_id):
    print(f"Welcome, Doctor {doctor_id}!")
    print("Press 1 to check your appointments")
    print("Press 2 to edit your appointments")
    print("Press 3 to check patient medical history")
    print("Press 4 to add new prescription")
    print("Press 5 to edit prescription")
    print("Press 6 to delete prescription")
    print("Press 7 for all appointments")
    print("Press 8 for all medical history")
    print("Press q to go back to main menu")

    while True:
        action = input()

        if action == 'q':
            break

        if action == '1':
            # Retrieve appointments for the specified doctor_id
            cursor.execute("SELECT * FROM appointment WHERE doctor_id = %s", (doctor_id,))
            appointments = cursor.fetchall()
            if appointments:
                for appointment in appointments:
                    print(f"Appointment ID: {appointment['appointment_id']}")
                    print(f"Patient ID: {appointment['patient_id']}")
                    print(f"Appointment Date: {appointment['appointment_date']}")
                    print(f"Reason: {appointment['reason']}")
            else:
                print("No appointments found for the doctor.")
        elif action == '2':
        # Edit appointments
            appointment_id = input("Enter the Appointment ID to edit: ")
            appointment_date = input("Enter the new Appointment Date (YYYY-MM-DD HH:MM): ")
            reason = input("Enter the new Reason: ")

            response = edit_appointment(appointment_id, appointment_date, reason)
            print(response)
        
        elif action == '3':
            # Check patient medical history
            patient_id = input("Enter the Patient ID whose medical history you want to check: ")
            medical_history_data = check_patient_medical_history(patient_id)
            
            if medical_history_data:
                for record in medical_history_data:
                    print(f"Medical ID: {record['medical_history_id']}")
                    print(f"Patient ID: {record['patient_id']}")
                    print(f"Medical Condition: {record['medical_condition']}")
                    print(f"Date Diagnose: {record['date_diagnosed']}")
                    print(f"Treatment: {record['treatment']}")
            else:
                print("No medical history found for the patient.")
       
        elif action == '4':
         # Add new prescription
           # prescription_id = input("Enter Prescription ID: ")
            patient_id = input("Enter Patient ID: ")
            medication_name = input("Enter Medication Name: ")
            dosage = input("Enter Dosage: ")
            start_date = input("Enter Start Date (YYYY-MM-DD): ")
            end_date = input("Enter End Date (YYYY-MM-DD): ")

            response = add_new_prescription(patient_id, medication_name, dosage, start_date, end_date)
            print(response)

        elif action == '5':
            # Edit prescriptions 
            prescription_id = input("Enter the Prescription ID to edit: ")
            medication_name = input("Enter the new Medication Name: ")
            dosage = input("Enter the new Dosage: ")
            start_date = input("Enter the new Start Date (YYYY-MM-DD): ")
            end_date = input("Enter the new End Date (YYYY-MM-DD): ")

            response = edit_prescription(prescription_id, medication_name, dosage, start_date, end_date)
            print(response)

        elif action == '6':
            # delete prescription

            prescription_id_to_delete = input("Enter the Prescription ID to delete: ")

            response = delete_prescription(prescription_id_to_delete)
            print(response)

        # Inside the doctor_actions function
        elif action == '7':
            response = get_all_appointments()
            print(response)

        elif action == '8':
    # Retrieve all medical history
            response = get_all_medical_history()
            print(response)

def check_patient_appointments(patient_id):
    try:
        # Retrieve appointments for the specified patient_id
        cursor.execute("SELECT * FROM appointment WHERE patient_id = %s", (patient_id,))
        appointments = cursor.fetchall()
        
        if appointments:
                appointments_info = []
        for appointment in appointments:
            appointment_info = (
                f"Appointment ID: {appointment['appointment_id']}\n"
                f"Doctor ID: {appointment['doctor_id']}\n"
                f"Appointment Date: {appointment['appointment_date']}\n"
                f"Reason: {appointment['reason']}\n"
            )
            appointments_info.append(appointment_info)

            return {"appointments": appointments_info}
        else:
            return {"appointments": "No appointments found for the patient."}
    except Exception as e:
        print(f"Error: {str(e)}")
    return {"appointments": "An error occurred while retrieving appointments."}

def make_new_appointment(patient_id, doctor_id, appointment_date, reason):
    try:
        # Check if patient_id and doctor_id exist in the respective tables
        cursor.execute("SELECT * FROM patient WHERE patient_id = %s", (patient_id,))
        patient = cursor.fetchone()
        
        cursor.execute("SELECT * FROM doctor WHERE doctor_id = %s", (doctor_id,))
        doctor = cursor.fetchone()

        if not patient or not doctor:
            return "Patient or Doctor not found"

        # Add logic to insert a new appointment into the appointment table
        insert_query = "INSERT INTO appointment (patient_id, doctor_id, appointment_date, reason) VALUES (%s, %s, %s, %s)"
        data = (patient_id, doctor_id, appointment_date, reason)
        cursor.execute(insert_query, data)
        conn.commit()
       
        return "Appointment created successfully"
    except Exception as e:
        return f"Error: {str(e)}"
def delete_appointment(appointment_id):
    
        # Delete the appointment from the appointment table
        cursor.execute("DELETE FROM appointment WHERE appointment_id = %s", (appointment_id,))
        conn.commit()
        return f"Appointment successfully deleted."
    

    
def view_prescriptions(patient_id):
    try:
        # Retrieve patient prescriptions from the prescription table
        cursor.execute("SELECT * FROM prescriptions WHERE prescription_id = %s", (patient_id,))
        prescriptions = cursor.fetchall()

        if prescriptions:
            prescriptions_info = []
            for prescription in prescriptions:
                prescription_info = (
                    f"Prescription ID: {prescription['prescription_id']}\n"
                    f"medication_name: {prescription['medication_name']}\n"
                    f"dosage:{prescription['dosage']}\n"
                    f"start_date: {prescription['start_date']}\n"
                    f"end_date:{prescription['end_date']}\n"
                )
                prescriptions_info.append(prescription_info)

            return {"prescriptions": prescriptions_info}
        else:
            return f"No prescriptions found for the patient."

    except Exception as e:
        return  f"Error: {str(e)}"
    
def check_patient_info(patient_id):
    try:
        # Retrieve patient information from the patients table
        cursor.execute("SELECT * FROM patient WHERE patient_id = %s", (patient_id,))
        patient_info = cursor.fetchone()

        if patient_info:
            return {
                "patient_info": {
                    "Patient ID": patient_info['patient_id'],
                    "First Name": patient_info['first_name'],
                    "Last Name": patient_info['last_name'],
                    "Age": patient_info['age'],
                    "Gender":patient_info['gender'],
                    "Address": patient_info['address'],
                    "Contact Number":patient_info['phone_number']
                    
                }
            }
        else:
            return f"Patient information not found."

    except Exception as e:
        return  f"Error: {str(e)}"




def view_medical_history(patient_id):
    try:
        # Check if patient_id exists in the patient table
        cursor.execute("SELECT * FROM patient WHERE patient_id = %s", (patient_id,))
        patient = cursor.fetchone()

        if not patient:
            return f"Patient not found"

        # Retrieve medical history for the specified patient_id
        cursor.execute("SELECT * FROM medical_history WHERE patient_id = %s", (patient_id,))
        medical_history_data = cursor.fetchall()

        if medical_history_data:
            for history_entry in medical_history_data:
                print(f"Medical History ID: {history_entry['medical_history_id']}")
                print(f"Medical Condition: {history_entry['medical_condition']}")
                print(f"Date Diagnosed: {history_entry['date_diagnosed']}")
                print(f"Treatment: {history_entry['treatment']}")
                
        else:
            print("No medical history found for the patient.")
    except Exception as e:
        return {"status": "error", "message": str(e)}

def register_doctor(first_name,last_name, specialty):
        cursor.execute("INSERT INTO doctor (first_name,last_name, specialty) VALUES (%s, %s, %s)",
                       (first_name,last_name, specialty))
        conn.commit()
    
        return f"Doctor registration successful."

def register_patient(first_name, last_name,age,gender, address,phone_number):
    
        # Insert the new patient into the patients table
        cursor.execute("INSERT INTO patient (first_name, last_name,age,gender, address,phone_number) "
                       "VALUES (%s, %s, %s, %s, %s, %s)",
                       (first_name, last_name,age,gender, address,phone_number))
        conn.commit()
        return f"Patient registration successful."


# Function for patient-specific actions
def patient_actions_interface(patient_id):
    print(f"Welcome, Patient {patient_id}!")
    print("Press 1 to check your appointment ")
    print("Press 2 to make new appointment ")
    print("Press 3 to cancel your appointment")
    print("Press 4 to view prescriptions")
    print("Press 5 to check your info")
    print("Press 6 to viewing medical history")
    print("Press q to go back to the main menu")

    while True:
        action = input()

        if action == 'q':
            break
        
        if action == '1':
            try:
                # Retrieve patient appointments from the appointment table
                cursor.execute("SELECT * FROM appointment WHERE patient_id = %s", (patient_id,))
                appointments = cursor.fetchall()

                if appointments:
                    appointments_info = []
                    for appointment in appointments:
                        appointment_info = (
                            f"Appointment ID: {appointment['appointment_id']}"
                            f"Doctor ID: {appointment['doctor_id']}"
                            f"Appointment Date: {appointment['appointment_date']}"
                            f"Reason: {appointment['reason']}"
                        )
                        appointments_info.append(appointment_info)

                    print({"appointments": appointments_info})
                else:
                    print({"appointments": "No appointments found for the patient."})
            except Exception as e:
                print(f"Error: {str(e)}")
        elif action == '2':
            print("Make a new appointment")
            doctor_id = input("Enter Doctor ID: ")
            appointment_date = input("Enter Appointment Date (YYYY-MM-DD HH:MM): ")
            reason = input("Enter Reason for Appointment: ")

            response = make_new_appointment(patient_id, doctor_id, appointment_date, reason)
            print(response)
        elif action == '3':
            print("Cancel your appointment")
            appointment_id = input("Enter Appointment ID:")
            response = delete_appointment(appointment_id)
            print(response)

        elif action == '4':
            print("View prescriptions")
            prescription_id = input("Enter prescription ID:")
            response = view_prescriptions(prescription_id)
            print(response)
        
        elif action == '5':
            print("Check your info:")
            patient_id = input("Enter Patient ID:")
            response = check_patient_info(patient_id)
            print(response)
        
        elif action == '6':
            print("View medical history")
            patient_id = input("Enter Patient ID:")
            response = view_medical_history(patient_id)
            print(response)

if __name__ == '__main__':
    print("Welcome to the Outpatient Clinic Database!")
    print("Press 1 for Doctor login")
    print("Press 2 for Patient login")
    print("Press 3 for New registration")
    print("Press q to quit")

    while True:
        choice = input()

        if choice == '1':
            print("Doctor check page")
            username = input("Enter username: ")
            password = input("Enter password: ")

            response = doctor_login(username, password)
            print(response)

            if "status" not in response:
                doctor_id = doctors[username]["doctor_id"]
                doctor_actions_interface(str(doctor_id))

        elif choice == '2':
            print("Patient check page")
            username = input("Enter username: ")
            password = input("Enter password: ")

            response = patient_login(username, password)
            print(response)

            if "status" not in response:
                 patient_id = patient[username]["patient_id"]
                 patient_actions_interface(patient_id)


        elif choice == '3':
            # New registration
            role = input("Enter role (doctor/patient): ")
            #username = input("Enter username: ")
           #password = input("Enter password: ")

            if role == 'doctor':
                first_name = input("Enter doctor's first_name: ")
                last_name = input("Enter doctor's last_name: ")
                specialty = input("Enter doctor's specialization: ")

                response = register_doctor(first_name,last_name,specialty)

            elif role == 'patient':

                first_name = input("Enter patient's first name: ")
                last_name = input("Enter patient's last name: ")
                age = input("Enter patient's age: ")
                gender = input("Enter patient's gender: ")
                address = input("Enter patient's address: ")
                phone_number = input("Enter patient's Contact Number: ")

                response = register_patient(first_name, last_name,age,gender,address,phone_number)
            else:
                response = f"Invalid role. Please enter 'doctor' or 'patient'."

            print(response)

        
           


        elif choice == 'q':
            break

        else:
            print("Invalid choice. Please try again.")
