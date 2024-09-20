# AI-Driven Report Generator

## Overview

This project allows users to upload a CSV file, preprocess the data, and query it using LangChain and OpenAI. The results, including visualizations, can be saved as a PDF report.

## Setup

1. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
2. Activate the virtual environment:
    - On Windows:
      ```bash
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up your OpenAI API key as an environment variable:
    ```bash
    export OPENAI_API_KEY='your_api_key'
    ```
5. Run the application:
    ```bash
    streamlit run main.py
    ```

## Usage

1. Upload a CSV file.
2. Enter a query related to the data.
3. View the results and generate a PDF report.

## License

This project is licensed under the MIT License.
