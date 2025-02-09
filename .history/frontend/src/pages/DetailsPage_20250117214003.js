import React from 'react';
import { useLocation } from 'react-router-dom';
import './DetailsPage.css';

const DetailPage = () => {
  const location = useLocation();
  const { predictionData,result } = location.state;

  // Calculate BMI category
  const bmiCategory = () => {
    if (predictionData.bmi < 18.5) {
      return 'Underweight';
    } else if (predictionData.bmi >= 18.5 && predictionData.bmi < 25) {
      return 'Normal';
    } else if (predictionData.bmi >= 25 && predictionData.bmi < 30) {
      return 'Overweight';
    } else {
      return 'Obese';
    }
  };

  // Calculate age group
  const ageGroup = () => {
    if (predictionData.age < 18) {
      return 'Child/Adolescent';
    } else if (predictionData.age >= 18 && predictionData.age < 65) {
      return 'Adult';
    } else {
      return 'Senior';
    }
  };

  return (
    <div className="details-container">
      <h2>Medical Insurance Cost Prediction Details</h2>
      <p>Here's a breakdown of the factors that influenced your predicted insurance cost:</p>
      <ul>
        <li>Age: {predictionData.age} years old ({ageGroup()})</li>
        <li>Sex: {predictionData.sex === 0 ? 'Male' : 'Female'}</li>
        <li>BMI: {predictionData.bmi} ({bmiCategory()})</li>
        <li>Number of Children: {predictionData.children}</li>
        <li>Smoker: {predictionData.smoker === 1 ? 'Yes' : 'No'}</li>
        <li>Region: {predictionData.region === 0 ? 'Northeast' : predictionData.region === 1 ? 'Southeast' : predictionData.region === 2 ? 'Southwest' : 'Northwest'}</li>
      </ul>

      <div className="additional-insights">
        <h3>Additional Insights:</h3>
        <ul>
          <li>
            {predictionData.smoker === 1
              ? 'Smoking significantly increases the risk of various health conditions and can lead to higher insurance premiums.'
              : 'Not smoking is a positive health factor that can contribute to lower insurance costs.'}
          </li>
          <li>
            {bmiCategory() === 'Obese'
              ? 'Maintaining a healthy weight is crucial for overall health and can help reduce the risk of chronic diseases.'
              : ''}
          </li>
          <li>
            {ageGroup() === 'Senior'
              ? 'Seniors may have higher insurance costs due to increased health risks associated with aging.'
              : ''}
          </li>
        </ul>
      </div>

      <p>Predicted Insurance Cost: ${predictionData}</p>
    </div>
  );
};

export default DetailPage;
