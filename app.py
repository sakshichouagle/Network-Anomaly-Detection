import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# Load the pre-trained model
def load_model(model_path):
    return joblib.load(model_path)

# Function to make predictions using the loaded model
def predict(model, data):
    # Assuming your model takes a DataFrame as input
    predictions = model.predict(data)
    return predictions

# Function to display security measures based on predictions
def security_measures(predictions):
    # Your logic to determine security measures based on predictions
    # This is just a placeholder
    if any(predictions == 1):
        measures = [
            "1. Change all system passwords immediately.",
            "2. Disconnect the system from the network.",
            "3. Run a thorough antivirus scan."
        ]
    else:
        measures = ["No immediate security measures needed. System appears secure."]
    return measures

def main():
    st.title('Network Security Check')

    uploaded_test_file = st.file_uploader("Upload Test Data", type=["csv"])
    model_path = st.file_uploader("Upload Model File", type=["pkl"])

    if uploaded_test_file is not None and model_path is not None:
        test_data = pd.read_csv(uploaded_test_file)
        model = load_model(model_path)

        # Encode categorical variables
        label_encoders = {}
        for column in ['protocol_type', 'flag']:
            label_encoders[column] = LabelEncoder()
            test_data[column] = label_encoders[column].fit_transform(test_data[column])

        if st.button('Scan'):
            # Select only the relevant features
            selected_features = ['protocol_type', 'flag', 'src_bytes', 'dst_bytes', 'count', 'same_srv_rate', 'diff_srv_rate', 'dst_host_srv_count', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate']
            test_data_selected = test_data[selected_features]

            predictions = predict(model, test_data_selected)
            measures = security_measures(predictions)
            st.write("Your Network is Compromised")
            st.write("Security Measures:")
            for measure in measures:
                
                st.write(measure)

if __name__ == '__main__':
    main()
