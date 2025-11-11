# Architecture Documentation for Impact Evaluator

## Overview
The Impact Evaluator is a web application designed to assess and visualize the effectiveness of various programs, particularly in the fields of MEAL (Monitoring, Evaluation, Accountability, and Learning), Protection, and Legal Aid. The application integrates with Google Sheets for data storage and retrieval, allowing users to input program data, calculate key performance indicators (KPIs), and generate reports.

## Components

### 1. Streamlit App
- **File**: `app/streamlit_app.py`
- **Description**: This is the main application file that contains the logic for the Streamlit web interface. It handles user input, processes data, calculates KPIs, and displays results. The app also generates PDF reports and saves data to Google Sheets.

### 2. Data
- **File**: `data/sample_data.csv`
- **Description**: This file is used to store sample data for testing and demonstration purposes. It can be utilized to simulate user input and validate the functionality of the application.

### 3. Scripts
- **File**: `scripts/run.sh`
- **Description**: This shell script is responsible for running the application. It may include commands to start the Streamlit server and perform any necessary setup tasks.

### 4. Tests
- **File**: `tests/test_streamlit_app.py`
- **Description**: This file contains unit tests for the Streamlit application. It ensures that the application logic functions correctly and that the KPIs are calculated accurately.

### 5. Development Container
- **Folder**: `.devcontainer`
  - **File**: `devcontainer.json`
    - **Description**: This file contains configuration settings for the development container, specifying the environment and tools needed for development.
  - **File**: `Dockerfile`
    - **Description**: This file defines the Docker image used for the development container, including the base image and any additional dependencies required.

### 6. Configuration
- **File**: `.gitignore`
- **Description**: This file specifies files and directories that should be ignored by Git, such as temporary files, logs, and environment configurations.

### 7. Dependencies
- **File**: `requirements.txt`
- **Description**: This file lists the Python dependencies required for the project, which can be installed using pip.

### 8. Google Credentials
- **File**: `google_credentials.example.json`
- **Description**: This file serves as an example for the Google credentials needed to connect to Google Sheets. It should be replaced with actual credentials for the application to function.

### 9. Documentation
- **File**: `README.md`
- **Description**: This file contains documentation for the project, including setup instructions, usage guidelines, and any other relevant information for users and developers.

## Interaction Flow
1. Users input program data through the Streamlit app.
2. The app calculates KPIs based on the input data.
3. Results are visualized within the app and can be exported as PDF reports.
4. Data is saved to Google Sheets for persistent storage and further analysis.
5. Unit tests ensure the reliability of the application logic.

## Conclusion
The architecture of the Impact Evaluator is designed to provide a seamless user experience while ensuring robust data handling and reporting capabilities. Each component plays a crucial role in the overall functionality of the application, making it a comprehensive tool for program evaluation.