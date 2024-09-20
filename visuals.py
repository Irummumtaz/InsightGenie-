import plotly.express as px
import plotly.graph_objects as go

def generate_plot(query, df):
    """
    Dynamically generates a relevant Plotly plot based on the user's query.
    
    Parameters:
    query (str): The user's query.
    df (pd.DataFrame): The dataset.
    
    Returns:
    fig: Plotly figure object or a message if no plot is found.
    """
    query = query.lower()  # Normalize query for easier matching
    # Set default template for color plots
    px.defaults.template = "plotly"

    ### Average Bandwidth Requirement Queries ###
    if ("average bandwidth requirement" in query and "online gaming" in query) or \
       ("plot a bar chart of the average bandwidth requirement for online gaming" in query):
        avg_bandwidth = df[df['Application_Type'] == 'Online Gaming'].groupby('Application_Type')['Required_Bandwidth'].mean().reset_index()
        fig = px.bar(avg_bandwidth, x='Application_Type', y='Required_Bandwidth', 
                      title="Average Bandwidth Requirement for Online Gaming",
                      color_discrete_sequence=px.colors.sequential.Viridis)
        return fig

    ### Histogram Query ###
    elif "histogram" in query:
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df['Signal_Strength'], marker_color=px.colors.sequential.Viridis[0])) 
        fig.update_layout(title="Histogram of Signal Strength Distribution")
        return fig

    ### Latency Analysis Queries ###
    elif ("average latency" in query and "application" in query) or \
         ("applications using the highest latency" in query):
        avg_latency = df.groupby('Application_Type')['Latency'].mean().reset_index()
        fig = px.bar(avg_latency, x='Application_Type', y='Latency', 
                      title='Average Latency by Application Type',
                      color_discrete_sequence=px.colors.sequential.Viridis)
        return fig

    elif "maximum average latency" in query:
        max_latency_app = df.groupby('Application_Type')['Latency'].mean().idxmax()
        fig = px.bar(df[df['Application_Type'] == max_latency_app], x='Application_Type', y='Latency', 
                      title=f'Maximum Average Latency: {max_latency_app}',
                      color_discrete_sequence=px.colors.sequential.Viridis)
        return fig

    elif "latency distribution by application type" in query or "visualize latency by application type" in query:
        fig = px.box(df, x='Application_Type', y='Latency', 
                      title='Latency Distribution by Application Type',
                      color_discrete_sequence=px.colors.sequential.Viridis)
        return fig

    elif "top applications with high latency" in query or "applications using the highest latency" in query:
        top_apps = df.groupby('Application_Type')['Latency'].mean().nlargest(7).reset_index()
        fig = px.bar(top_apps, x='Application_Type', y='Latency', 
                      title='Top Applications with High Latency',
                      color_discrete_sequence=px.colors.sequential.Viridis)
        return fig

    ### Resource Allocation Queries ###
    elif "average resource allocation" in query and "application" in query:
        avg_resource_alloc = df.groupby('Application_Type')['Resource_Allocation'].mean().reset_index()
        fig = px.bar(avg_resource_alloc, x='Application_Type', y='Resource_Allocation', 
                      title='Average Resource Allocation by Application Type',
                      color_discrete_sequence=px.colors.sequential.Viridis)
        return fig

    elif "distribution of resource allocation" in query:
        fig = px.histogram(df, x='Resource_Allocation', title='Distribution of Resource Allocation',
                           color_discrete_sequence=px.colors.sequential.Viridis)
        return fig

    ### Signal Strength Queries ###
    elif "distribution of signal strength" in query:
        fig = px.histogram(df, x='Signal_Strength', nbins=20, title='Distribution of Signal Strength',
                           color_discrete_sequence=px.colors.sequential.Viridis)
        return fig

    elif "visualize signal strength by application type" in query:
        fig = px.scatter(df, x='Application_Type', y='Signal_Strength', title='Signal Strength by Application Type',
                         color_discrete_sequence=px.colors.sequential.Viridis)
        return fig

    ### Application Types Queries ###
    elif "distribution of application types" in query or "visualize distribution of application types" in query:
        app_counts = df['Application_Type'].value_counts().reset_index()
        app_counts.columns = ['Application_Type', 'Count']
        fig = px.bar(app_counts, x='Application_Type', y='Count', title='Distribution of Application Types',
                      color_discrete_sequence=px.colors.sequential.Viridis)
        return fig

    elif "most commonly used application types" in query:
        app_counts = df['Application_Type'].value_counts().reset_index()
        fig = px.bar(app_counts, x='Application_Type', y='Application_Type', 
                      title="Most Commonly Used Application Types",
                      color_discrete_sequence=px.colors.sequential.Viridis)
        return fig

    ### Bandwidth Relationships Queries ###
    elif "relationship between allocated and required bandwidth" in query or \
         "visualize the relationship between allocated bandwidth and required bandwidth" in query:
        fig = px.scatter(df, x='Required_Bandwidth', y='Allocated_Bandwidth', 
                         title="Relationship Between Allocated and Required Bandwidth",
                         color_discrete_sequence=px.colors.sequential.Viridis)
        return fig

    else:
        return "No relevant plot found for this query."
