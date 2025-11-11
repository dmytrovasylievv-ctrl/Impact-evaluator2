# Impact Evaluator Project

## Overview
The Impact Evaluator is a web application built using Streamlit that allows users to evaluate programs in the areas of MEAL (Monitoring, Evaluation, Accountability, and Learning), Protection, and Legal Aid. The application integrates with Google Sheets to collect and store data, calculates key performance indicators (KPIs), visualizes results, and generates PDF reports.

## Project Structure
```
impact-evaluator
├── app
│   └── streamlit_app.py          # Main application logic for the Streamlit app
├── data
│   └── sample_data.csv           # Sample data for testing or demonstration
├── docs
│   └── architecture.md            # Documentation on the application's architecture
├── scripts
│   └── run.sh                    # Script to run the application
├── tests
│   └── test_streamlit_app.py      # Unit tests for the Streamlit app
├── .devcontainer
│   ├── devcontainer.json          # Development container configuration
│   └── Dockerfile                 # Docker image definition for the development container
├── .gitignore                     # Files and directories to ignore by Git
├── requirements.txt               # Python dependencies for the project
├── google_credentials.example.json # Example Google credentials for Sheets integration
└── README.md                      # Project documentation
```

## Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd impact-evaluator
   ```

2. **Install Dependencies**
   Ensure you have Python 3 and pip installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Google Sheets Integration**
   - Create a Google Cloud project and enable the Google Sheets API.
   - Create a service account and download the JSON credentials file.
   - Rename the downloaded file to `google_credentials.json` and place it in the project root.

4. **Run the Application**
   You can run the application using the provided script:
   ```bash
   ./scripts/run.sh
   ```

## Usage
- Open your web browser and navigate to `http://localhost:8501` to access the application.
- Input the required data for program evaluation and click on "Calculate Score" to view the results.

## Testing
To run the unit tests for the application, use:
```bash
pytest tests/test_streamlit_app.py
```

## Contribution
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.