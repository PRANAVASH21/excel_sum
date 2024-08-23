from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def calculate_billing_sum(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    # Check if 'Billing' column exists
    if 'Billing' in df.columns:
        return df['Billing'].sum()
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    total_sum = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            total_sum = calculate_billing_sum(file_path)
            os.remove(file_path)  # Clean up the file after processing

    return render_template('index.html', total_sum=total_sum)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
