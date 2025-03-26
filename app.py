import os
from flask import Flask, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt

# Initialize Flask app
app = Flask(__name__)

# Load dataset
DATASET_PATH = 'Superstore.csv'
df = pd.read_csv(DATASET_PATH, encoding='latin1')

# Create static plots folder if not exists
PLOTS_FOLDER = './static/plots'
if not os.path.exists(PLOTS_FOLDER):
    os.makedirs(PLOTS_FOLDER)

# Helper function to generate visualizations
def generate_visualizations():
    # Sales by Category (Bar Chart)
    category_sales = df.groupby('Category')['Sales'].sum()
    category_sales.plot(kind='bar', color=['skyblue', 'orange', 'green'])
    plt.title('Total Sales by Category')
    plt.savefig(f'{PLOTS_FOLDER}/category_sales.png')
    plt.clf()

    # Sales Distribution (Histogram)
    plt.hist(df['Sales'], bins=20, color='purple', alpha=0.7)
    plt.title('Sales Distribution')
    plt.savefig(f'{PLOTS_FOLDER}/sales_distribution.png')
    plt.clf()

    # Profit by Region (Pie Chart)
    region_profit = df.groupby('Region')['Profit'].sum()
    region_profit.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['gold', 'lightcoral', 'lightgreen', 'skyblue'])
    plt.title('Profit Distribution by Region')
    plt.savefig(f'{PLOTS_FOLDER}/region_profit.png')
    plt.clf()

    # Sales vs Profit (Scatter Plot)
    plt.scatter(df['Sales'], df['Profit'], alpha=0.6, c='blue')
    plt.title('Sales vs Profit')
    plt.xlabel('Sales')
    plt.ylabel('Profit')
    plt.savefig(f'{PLOTS_FOLDER}/sales_vs_profit.png')
    plt.clf()

# Generate visualizations on startup
generate_visualizations()

# Route for Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Route for Data Analysis and Visualizations
@app.route('/analysis')
def analysis():
    # Basic dataset summary
    head = df.head().to_html(classes='table table-striped')
    description = df.describe().to_html(classes='table table-striped')

    return render_template('analysis.html', head=head, description=description)

# Route to Download Cleaned Dataset
@app.route('/download')
def download():
    cleaned_file = './static/cleaned_superstore_sales.csv'
    df.to_csv(cleaned_file, index=False)
    return send_file(cleaned_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
