import streamlit as st
import requests

# Rename this file to avoid conflict with "streamlit.py"
# e.g., save as "streamlit_app.py"

BASE_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="Patient Management System", layout="wide")
st.title("🏥 Patient Management System")

# Sidebar menu
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "View Patients", "View Specific Patient", "Add Patient", "Edit Patient", "Delete Patient", "Sort Patients"]
)

def handle_api_request(method, endpoint, **kwargs):
    try:
        response = requests.request(method, f"{BASE_URL}{endpoint}", **kwargs)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)

# Home
if menu == "Home":
    st.header("Welcome to the Patient Management System")
    st.caption("Efficiently manage patient records with our system. Navigate through the menu to explore features.")
    st.image("Image/Patient.jpg", use_column_width=True)

# View All Patients
elif menu == "View Patients":
    st.header("👀 View All Patients")
    data, error = handle_api_request("GET", "/view")
    if error:
        st.error(f"Error: {error}")
    elif data:
        st.table(data)
    else:
        st.info("No patients found.")

# View Specific Patient
elif menu == "View Specific Patient":
    st.header("🔍 View Patient by ID")
    with st.form("view_form"):
        pid = st.text_input("Patient ID", "P001")
        submitted = st.form_submit_button("Fetch")
    if submitted:
        data, error = handle_api_request("GET", f"/patient/{pid}")
        if error:
            st.error(f"Error: {error}")
        elif data:
            st.json(data)
        else:
            st.info("Patient not found.")

# Add Patient
elif menu == "Add Patient":
    st.header("➕ Add a New Patient")
    st.caption("Example Payload: {'id': 'P001', 'name': 'John Doe', 'city': 'New York', 'age': 30, 'gender': 'male', 'height': 1.75, 'weight': 70.5}")
    with st.form("add_form"):
        id_ = st.text_input("Patient ID")
        name = st.text_input("Name")
        city = st.text_input("City")
        age = st.number_input("Age", 1, 120, step=1)
        gender = st.selectbox("Gender", ["male", "female", "others"])
        height = st.number_input("Height (m)", min_value=0.1, step=0.01)
        weight = st.number_input("Weight (kg)", min_value=0.1, step=0.1)
        submitted = st.form_submit_button("Add Patient")
    if submitted:
        payload = {"id": id_, "name": name, "city": city, "age": age, "gender": gender, "height": height, "weight": weight}
        _, error = handle_api_request("POST", "/create", json=payload)
        if error:
            st.error(f"Error: {error}")
        else:
            st.success("Patient added successfully.")

# Edit Patient
elif menu == "Edit Patient":
    st.header("✏️ Edit Patient Details")
    st.caption("Example Payload: {'name': 'John Doe', 'city': 'New York', 'age': 30, 'gender': 'male', 'height': 1.75, 'weight': 70.5}")
    with st.form("update_form_edit"):
        pid_edit = st.text_input("Patient ID to edit", placeholder="e.g., P001")
        name = st.text_input("Name", placeholder="e.g., John Doe")
        city = st.text_input("City", placeholder="e.g., New York")
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        gender = st.selectbox("Gender", ["male", "female", "others"])
        height = st.number_input("Height (m)", min_value=0.1, step=0.01)
        weight = st.number_input("Weight (kg)", min_value=0.1, step=0.1)
        update_submitted = st.form_submit_button("Update Patient")
    if update_submitted:
        if not pid_edit:
            st.error("Patient ID is required to update details.")
        else:
            # Prepare payload for the PUT request
            update_payload = {
                "name": name,
                "city": city,
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight,
            }
            # Ensure the PUT request is sent correctly
            response, error = handle_api_request("PUT", f"/edit/{pid_edit}", json=update_payload)
            if error:
                st.error(f"Update error: {error}")
            else:
                st.success("Patient updated successfully!")

# Delete Patient
elif menu == "Delete Patient":
    st.header("🗑️ Delete a Patient")
    with st.form("delete_form"):
        pid_del = st.text_input("Patient ID to delete")
        submitted = st.form_submit_button("Delete Patient")
    if submitted and pid_del:
        _, error = handle_api_request("DELETE", f"/delete/{pid_del}")
        if error:
            st.error(f"Error: {error}")
        else:
            st.success("Patient deleted successfully.")

# Sort Patients
elif menu == "Sort Patients":
    st.header("🔃 Sort Patients")
    with st.form("sort_form"):
        sort_by = st.selectbox("Sort By", ["height", "weight", "bmi"])
        order = st.radio("Order", ["asc", "desc"])
        submitted = st.form_submit_button("Sort")
    if submitted:
        data, error = handle_api_request("GET", "/sort", params={"sort_by": sort_by, "order": order})
        if error:
            st.error(f"Error: {error}")
        elif data:
            st.table(data)
        else:
            st.info("No patients to sort.")
