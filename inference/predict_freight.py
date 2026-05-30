import joblib
import pandas as pd
import os

#MODEL_PATH = r"models\predict_freight_model.pkl"
# Build an absolute path dynamically
# 1. Find the exact folder this script lives in (the 'inference' folder)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up one level (..), then into the 'models' folder, then to the file
MODEL_PATH = os.path.join(current_dir, "..", "models", "predict_freight_model.pkl")

def load_model(model_path: str = MODEL_PATH):
    """
    Load trained freight cost prediction model.
    """
    with open(model_path, "rb") as f:
        model = joblib.load(f)
    return model


def predict_freight_cost(input_data):
    """
    Predict freight cost for new vendor invoices.
    
    Parameters
    ----------
    input_data : dict
    
    Returns
    -------
    pd.DataFrame with predicted freight cost
    """    
    model = load_model()
    input_df = pd.DataFrame(input_data)
   
    
    # 4. Output the EXACT column name Streamlit is trying to read
    
    input_df['Predicted_Freight'] = model.predict(input_df).round()
    return input_df

if __name__ == "__main__":
    
    # Example inference run (local testing)
    sample_data = {
       
        "Dollars": [18500, 9000, 15000]  # Match the exact DB column name
    }
    prediction = predict_freight_cost(sample_data)
    print(prediction)
