# Macadamia Disease and Pest Diagnostic Tool

This project is a simple knowledge-based system for diagnosing diseases and pests in macadamia trees. It provides a web-based graphical user interface (GUI) built with Streamlit to help users identify potential problems based on observed symptoms.

 ## Link to live app
 
[https://macadamia-health-gma5lufrokb3vtaewsecrk.streamlit.app/]

## Features

*   **Symptom-based diagnosis:** Select the symptoms you observe on your macadamia trees.
*   **Scored results:** The tool provides a scored list of possible diseases and pests, making it easy to see the most likely causes.
*   **Treatment suggestions:** For each diagnosed problem, the tool suggests potential treatments based on a knowledge base of pesticides and fungicides.
*   **Web-based GUI:** The user-friendly interface is built with Streamlit, making it easy to use and access.

## Project Structure

*   `macadamia_doctor.py`: The core Python script containing the diagnostic logic.
*   `macadamia_doctor_streamlit.py`: The Streamlit application that provides the web-based GUI.
*   `macadamia_facts.csv`: A CSV file containing the knowledge base of diseases, pests, and their symptoms.
*   `pesticides_fungicides.pl`: A Prolog-like file containing the knowledge base of treatments.
*   `venv/`: A virtual environment to manage the project's dependencies.

## Setup and Usage

### 1. Create and activate the virtual environment

First, create a virtual environment to manage the project's dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install the dependencies

Install the necessary Python libraries using pip.

```bash
pip install -r requirements.txt
```

*(Note: A `requirements.txt` file will be generated in the next step.)*

### 3. Run the application

To run the Streamlit application, use the following command:

```bash
streamlit run macadamia_doctor_streamlit.py
```

This will start a local web server and open the application in your web browser.

## How to Use

1.  **Select symptoms:** In the web interface, you will see a list of symptoms. Select the symptoms you have observed on your macadamia trees.
2.  **Click "Diagnose":** Once you have selected the symptoms, click the "Diagnose" button.
3.  **View the results:** The application will display a list of possible diseases and pests, ranked by how well they match the selected symptoms. For each result, you will see a match score, the causal agent, and suggested treatments.
