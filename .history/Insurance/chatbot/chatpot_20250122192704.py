# chatbot/chatbot.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample FAQ dataset (questions and their corresponding answers)
faq_data = {
    "How do I calculate my insurance cost?": "Insurance cost is calculated based on factors like age, sex, BMI, children, smoker status, and region.",
    "What factors affect my insurance cost?": "Age, sex, BMI, number of children, smoking habits, and region.",
    "How can I update my profile?": "You can update your profile details by logging into your account and editing your personal information.",
    "What is BMI and how does it affect my insurance cost?": "BMI stands for Body Mass Index, and a higher BMI may increase your insurance premium."
}

# Initialize the vectorizer
vectorizer = TfidfVectorizer()

# Convert the questions into a TF-IDF matrix
questions = list(faq_data.keys())
answers = list(faq_data.values())
tfidf_matrix = vectorizer.fit_transform(questions)

def chatbot_response(user_input):
    """Function to generate a response based on cosine similarity"""
    # Vectorize the user input
    user_input_vec = vectorizer.transform([user_input])
    
    # Calculate cosine similarity between user input and predefined questions
    cosine_sim = cosine_similarity(user_input_vec, tfidf_matrix)
    
    # Find the most similar question and return the corresponding answer
    most_similar_index = np.argmax(cosine_sim)
    return answers[most_similar_index]
