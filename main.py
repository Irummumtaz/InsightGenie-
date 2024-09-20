import os
import uuid
import pandas as pd
import streamlit as st
from fpdf import FPDF
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_openai import OpenAI
import plotly.graph_objects as go
import io
from PIL import Image
import base64
from preprocess import preprocess_data  # Import your preprocessing script
from dotenv import load_dotenv
from generate_pdf import generate_pdf_report
from visuals import generate_plot

load_dotenv()

# Set up environment variable for OpenAI API key


openai_api_key = ""


# Initialize OpenAI LLM
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

# Initialize session state for query history
if "query_history" not in st.session_state:
    st.session_state.query_history = []

# Function to generate a detailed summary of the response
def generate_detailed_response(agent_response, query):
    needs_visualization = query_needs_visualization(query)
    if needs_visualization:
        detailed_prompt = f"""
        Analyze the data based on the following query: {agent_response[:1000]}. 
        Provide a clear and relevant explanation related to the dataset, and include necessary visualizations to support your findings. 
        Make sure to include descriptions of the visualizations and explain how they address the query. 
        Limit your explanation to 350 words for clarity and focus.
        """
    else:
        detailed_prompt = f"""
        Analyze the data based on the following query: {agent_response[:1000]}. 
        Provide a clear and relevant explanation based on the dataset without including visualizations. 
        Focus on delivering insights and answering the query directly, while keeping your response to 350 words to maintain brevity.
        """
    detailed_response = llm(detailed_prompt)
    return detailed_response

# Function to detect if a visualization is required based on the query
def query_needs_visualization(query):
    visualization_keywords = ["visualize", "chart", "plot", "graph", "bar", "scatter", "histogram"]
    for keyword in visualization_keywords:
        if keyword in query.lower():
            return True
    return False

# Ensure the plots directory exists
if not os.path.exists("plots"):
    os.makedirs("plots")

# Load logo image
logo_path = r"C:\Users\irumj\OneDrive\Desktop\DS\langchain_report_generator\insightgenie.png"
logo = Image.open(logo_path)

# Set up the Streamlit app
st.set_page_config(page_title="InsightGenie", page_icon=logo, layout="centered")

# Apply dark theme
st.markdown(
    """
<style>
    /* Sidebar background color */
    .css-1d391kg {
        background-color: #304530;  /* Set sidebar to a lighter shade of black (dark gray) */
    }
    
    /* Main body background color and text */
    .css-18e3th9 {
        background-color: #000 !important;  /* Set main background to pure black */
        color: #fff;  /* Set main text color to white */
    }

    /* Secondary areas background (query input and file upload areas) */
    .css-1wr1km0 {
        background-color: #333 !important;  /* Set secondary containers (file upload, query areas) to dark gray */
        color: #fff;  /* Set secondary container text color to white */
    }

    /* Text color inside secondary containers */
    .css-1v3v5w6 {
        color: #fff;  /* Set secondary container text color to white */
    }

    /* Button styling */
    button {
        background-color: #444;  /* Set button background color to a dark gray */
        color: #fff;  /* Set button text color to white */
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    
    /* Button hover effect */
    button:hover {
        background-color: #555;  /* Set hover background to slightly lighter gray */
    }

    /* Table styles */
    table {
        border-collapse: collapse;
        width: 100%;
        color: #fff;  /* Set table text color to white */
    }

    /* Table header styles */
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        color: #fff;  /* Set table cell text color to white */
    }

    /* Header background for tables */
    th {
        background-color: #555;  /* Set table header background to dark gray */
        color: white;  /* Keep table header text white */
        font-size: 1.2em;
    }

    /* Row colors for tables */
    tr:nth-child(even) {
        background-color: #444;  /* Set even rows background color to dark gray */
    }
    tr:nth-child(odd) {
        background-color: #333;  /* Set odd rows background color to slightly lighter dark gray */
    }

    /* Main container background */
    .css-1n76m1d { 
        background-color: #000;  /* Set main container background to pure black */
        color: #fff;  /* Set main container text color to white */
    }
</style>
""",
unsafe_allow_html=True


)

# Sidebar with logo and button
with st.sidebar:
    st.image(logo, use_column_width=True)
    st.title("InsightGenie 🧠")
    st.markdown("**Transform Data Queries into Smart, Automated Reports with LangChain and OpenAI**")
    st.markdown("---")  # Divider for clarity
    

    if st.button("Generate PDF Report"):
        if st.session_state.query_history:
            output_filename = f"report_{str(uuid.uuid4())}.pdf"
            generate_pdf_report(
                query_history=st.session_state.query_history,
                output_filename=output_filename,
                plots_dir="plots"
            )
            st.success("PDF report generated successfully!")

            # Provide download link
            with open(output_filename, "rb") as file:
                st.download_button(
                    label="Download PDF Report",
                    data=file,
                    file_name=output_filename,
                    mime="application/pdf"
                )
        else:
            st.warning("No queries to include in the report.")
    
    if st.session_state.query_history:
        for i, (q, response, img) in enumerate(st.session_state.query_history):
            with st.expander(f"Query {i+1}"):
                st.write(f"**Query:** {q}")
                st.write(f"**Response:** {response}")
                if img:
                    st.image(img, caption=f"Visualization for Query {i+1}", use_column_width=True)

# Main content with headline
st.markdown(
    """
    <h2 style='text-align: center; color: #2c7a7b;'>📊 Transform Data Queries into Smart, Automated Reports with LangChain and OpenAI 🚀</h1>
    """,
    unsafe_allow_html=True
)

# File upload for CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    st.write("**Data Preview:**")
    st.dataframe(df.head(), use_container_width=True)

    # Preprocess the DataFrame before querying
    df = preprocess_data(df)
    st.write("**Data after Preprocessing:**")
    st.dataframe(df.head(), use_container_width=True)

    # Initialize Pandas DataFrame Agent
    agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True, max_iterations=200, timeout=600)

    # Ask the user for a query related to the dataset
    query = st.text_input("Enter your query for the data (e.g., 'Show the top 5 rows' or 'What are the basic statistics?'):").strip()

    if query:
        with st.container():
            st.write("**Query**:")
            st.write(query)
            
            # Use Pandas Agent to handle the query
            response = agent.run(query)
            
            # Generate a detailed response
            detailed_response = generate_detailed_response(response, query)
            
            st.write("**Detailed Response:**")
            st.markdown(detailed_response)

            # If the query or response suggests a visualization, generate the relevant plot
            if query_needs_visualization(query):
                st.write("**Generating Visual Based on Query:**")
                fig_plotly = generate_plot(query, df)  # This should now return only Plotly figures

                if isinstance(fig_plotly, go.Figure):  # Check if the returned value is a valid Plotly figure
                    # Save Plotly figure as PNG
                    fig_name = f"plot_{str(uuid.uuid4())}.png"
                    fig_path = os.path.join("plots", fig_name)
                    fig_plotly.write_image(fig_path)
                    
                    # Display Plotly chart
                    st.write("**Displaying Visualization:**")
                    st.image(fig_path, caption=f"Plotly Visualization for Query {len(st.session_state.query_history) + 1}", use_column_width=True)
                    
                    # Append to query history
                    st.session_state.query_history.append((query, detailed_response, fig_path))
                else:  # If no plot is generated
                    st.write("No visualization generated for the given query.")
            else:
                st.session_state.query_history.append((query, detailed_response, None))
    
    if st.session_state.query_history:
        st.subheader("Query History")
        for i, (q, response, img) in enumerate(st.session_state.query_history):
            with st.expander(f"Query {i+1}"):
                st.write(f"**Query:** {q}")
                st.write(f"**Response:** {response}")
                if img:
                    st.image(img, caption=f"Visualization for Query {i+1}", use_column_width=True)
