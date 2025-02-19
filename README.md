# Medical Insurance Cost Prediction System

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Dataset](#dataset)
5. [How It Works](#how-it-works)
6. [Project Structure](#project-structure)
7. [Setup Instructions](#setup-instructions)
8. [Usage](#usage)
9. [Future Enhancements](#future-enhancements)
10. [Contributing](#contributing)
11. [License](#license)

---

## Overview

The **Medical Insurance Cost Prediction System** is a web-based application that predicts the medical insurance costs for users based on their demographic and lifestyle information. The system uses a Linear Regression model trained on a Kaggle dataset. The platform also includes features like PDF report generation, chatbot assistance for user queries, and a detailed insights section.

---

## Features

- Predict medical insurance costs based on user inputs (age, BMI, smoking habits, etc.).
- Generate downloadable reports in PDF format.
- Interactive chatbot for answering user queries (using Cosine Similarity).
- Admin functionality to add or delete details in the database.
- View additional insights and recommendations based on predictions.
- Simple and intuitive user interface.

---

## Technologies Used

### Frontend:
- React.js
- CSS (for styling)

### Backend:
- Django (Python)
- Django Rest Framework
- SQLite (Database)

### Machine Learning:
- Linear Regression (Model)
- Libraries: Scikit-learn, Pandas, NumPy

### Additional Tools:
- Cosine Similarity (for chatbot query matching)
- ReportLab (for PDF generation)

---

## Dataset

The dataset used for training the model is sourced from Kaggle and includes the following columns:
- `age`: Age of the individual
- `sex`: Gender of the individual
- `bmi`: Body Mass Index
- `children`: Number of dependents
- `smoker`: Smoking status (yes/no)
- `region`: Geographic region
- `charges`: Medical insurance costs (target variable)

Link to the dataset: [Medical Insurance Dataset](https://www.kaggle.com)

---

## How It Works

1. **Prediction Form**: Users input details such as age, BMI, smoking habits, etc.
2. **Prediction**: The system uses a trained Linear Regression model to calculate the estimated insurance cost.
3. **Recommendations**: Users can view additional insights and suggestions to reduce costs.
4. **Chatbot**: A chatbot answers FAQs using predefined questions and Cosine Similarity.
5. **PDF Report**: Users can download a detailed prediction report in PDF format.

---

## Project Structure

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/insurance-cost-prediction.git
   cd insurance-cost-prediction
2. **Bckend Setup**
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
3. **Frontend Setup**
cd react-frontend
npm install
npm start
4.**Start the Django Server**
python manage.py runserver

5. **Open your browser and navigate to http://127.0.0.1:8000/.**
**Usage**
Navigate to the home page.
Fill out the prediction form with your details.
Submit the form to view the predicted medical insurance cost.
Download the prediction report as a PDF.
Use the chatbot to get answers to common questions

**Future Enhancements**
Add user authentication for personalized dashboards.
Extend chatbot capabilities with NLP techniques.
Include data visualizations for user insights.
Support additional export formats (e.g., Excel).
Deploy the project using cloud platforms.

**Contributing**
Fork the repository.
Create a new branch: git checkout -b feature-name.
Commit your changes: git commit -m 'Add some feature'.
Push to the branch: git push origin feature-name.
Open a pull request.




