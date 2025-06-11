# Patient Management System

The **Patient Management System** is a web-based application designed to efficiently manage patient records. It provides a user-friendly interface for performing CRUD (Create, Read, Update, Delete) operations on patient data and includes features like sorting and viewing specific patient details.

## Features

- **Add Patient**: Add new patient records with details like name, city, age, gender, height, and weight.
- **View All Patients**: View a table of all patient records stored in the system.
- **View Specific Patient**: Fetch and display details of a specific patient by their ID.
- **Edit Patient**: Update the details of an existing patient.
- **Delete Patient**: Remove a patient record from the system.
- **Sort Patients**: Sort patient records by height, weight, or BMI in ascending or descending order.
- **BMI Calculation**: Automatically calculate and display the BMI and health verdict for each patient.

## Technologies Used

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Database**: JSON file (`patients.json`) for storing patient records
- **Python Libraries**: `pydantic`, `requests`, `uvicorn`

## Setup Instructions

### Prerequisites

- Python 3.8 or higher installed on your system
- `pip` package manager

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Patient-Management-System.git
   cd Patient-Management-System
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI backend:
   ```bash
   python app.py
   ```
   The backend will start at `http://127.0.0.1:8000`.

4. Run the Streamlit frontend:
   ```bash
   streamlit run streamlit.py
   ```
   The frontend will open in your default web browser.

### File Structure

```
Patient-Management-System/
├── app.py                # FastAPI backend
├── streamlit.py          # Streamlit frontend
├── patients.json         # JSON file for storing patient data
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── Image/
    └── Patient.jpg       # Image used on the home page
```

## API Endpoints

### Base URL: `http://127.0.0.1:8000`

- **GET `/view`**: View all patients.
- **GET `/patient/{patient_id}`**: View details of a specific patient.
- **POST `/create`**: Add a new patient.
- **PUT `/edit/{patient_id}`**: Update an existing patient's details.
- **DELETE `/delete/{patient_id}`**: Delete a patient record.
- **GET `/sort`**: Sort patients by height, weight, or BMI.

## Example Payloads

### Add Patient
```json
{
  "id": "P001",
  "name": "John Doe",
  "city": "New York",
  "age": 30,
  "gender": "male",
  "height": 1.75,
  "weight": 70.5
}
```

### Edit Patient
```json
{
  "name": "Jane Doe",
  "city": "Los Angeles",
  "age": 28,
  "gender": "female",
  "height": 1.65,
  "weight": 60.0
}
```

## Screenshots

### Home Page
![Home Page](Image/Patient.jpg)

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)