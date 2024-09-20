import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
def preprocess_data(df):
    # Check data types and missing values before processing
    print("\nData Types Before Processing:")
    print(df.info())
    
    # Separate numerical and categorical columns
    numerical_features = df.select_dtypes(include=['number']).columns
    categorical_features = df.select_dtypes(include=['object']).columns
    
    # Remove unwanted substrings and convert columns to numeric types
    try:
        print("Converting 'Signal_Strength', 'Latency', 'Resource_Allocation'")
        df['Signal_Strength'] = df['Signal_Strength'].str.replace(' dBm', '').astype('int')
        df['Latency'] = df['Latency'].str.replace(' ms', '').astype('int')
        df['Resource_Allocation'] = df['Resource_Allocation'].str.replace('%', '').astype('int')
    except Exception as e:
        print(f"Error converting 'Signal_Strength', 'Latency', or 'Resource_Allocation': {e}")
    
    # Print data types after conversion
    print("\nData Types After Conversion:")
    print(df.dtypes)
    
    # Convert 'Timestamp' to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    
    # Convert Mbps to Kbps in bandwidth columns
    def mbps_to_kbps(value):  
        if 'Mbps' in value:
            n = float(value.replace(' Mbps',''))
            return str(n * 1000) + ' Kbps'
        else:
            return value

    try:
        df['Required_Bandwidth'] = df['Required_Bandwidth'].map(mbps_to_kbps)
        df['Allocated_Bandwidth'] = df['Allocated_Bandwidth'].map(mbps_to_kbps)
        df['Required_Bandwidth'] = df['Required_Bandwidth'].str.replace(' Kbps', '').astype('float')
        df['Allocated_Bandwidth'] = df['Allocated_Bandwidth'].str.replace(' Kbps', '').astype('float')
    except Exception as e:
        print(f"Error in bandwidth conversion: {e}")
    
    # Print data types after bandwidth conversion
    print("\nData Types After Bandwidth Conversion:")
    print(df.dtypes)
    
    # Impute missing values for numerical and categorical features **after conversion**
    numerical_features = df.select_dtypes(include=['number']).columns
    categorical_features = df.select_dtypes(include=['object']).columns

    print("Numerical Features After Conversion: ", numerical_features)
    print("Categorical Features After Conversion: ", categorical_features)

   # Fill missing values using forward fill
    df.fillna(method='ffill', inplace=True)

# Fill remaining missing values using backward fill
    df.fillna(method='bfill', inplace=True)

# Impute missing values if forward/backward fill still leaves NaNs
    if df.isnull().sum().sum() > 0:  # Check if any NaNs remain
        if not df[numerical_features].empty:
            imputer_num = SimpleImputer(strategy='mean')
            df[numerical_features] = imputer_num.fit_transform(df[numerical_features])
    
        if not df[categorical_features].empty:
            imputer_cat = SimpleImputer(strategy='most_frequent')
            df[categorical_features] = imputer_cat.fit_transform(df[categorical_features])
    
    # Standardize numerical features
    scaler = StandardScaler()
    df[['Signal_Strength', 'Latency']] = scaler.fit_transform(df[['Signal_Strength', 'Latency']])
    
    # Create a new feature: Bandwidth Utilization Ratio
    df['Bandwidth_Utilization_Ratio'] = df['Allocated_Bandwidth'] / df['Required_Bandwidth']
    
    return df
 