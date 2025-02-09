import React, { useState } from 'react';

import axios from 'axios';

import { useNavigate } from 'react-router-dom';

import './GetPrediction.css';



const InsuranceForm = () => {

  const [formData, setFormData] = useState({

    age: '',

    sex: 'male',

    bmi: '',

    children: '',

    smoker: 'no',

    region: 'northeast'

  });

  const [result, setResult] = useState(null);

  const [error, setError] = useState(null);

  const [loading, setLoading] = useState(false);

  const [formattedData, setFormattedData] = useState(null);

  const navigate = useNavigate();



  const handleChange = (event) => {

    setFormData({

      ...formData,

      [event.target.name]: event.target.value

    });

  };



  const handleViewDetails = () => {

    if (formattedData && result) {

      navigate('/details', {

        state: {

          predictionData: formattedData,

          result: result

        }

      });

    }

  };



  const handleSubmit = async (event) => {

    event.preventDefault();

    setError(null);

    setLoading(true);



    // Basic form validation

    if (!formData.age || !formData.bmi || !formData.children) {

      setError('Please fill in all required fields.');

      setLoading(false);

      return;

    }



    const formatted = {

      age: Number(formData.age),

      sex: formData.sex === 'male' ? 0 : 1,

      bmi: parseFloat(formData.bmi),

      children: Number(formData.children),

      smoker: formData.smoker === 'no' ? 1 : 0,

      region: (() => {

        switch (formData.region) {

          case 'northeast': return 0;

          case 'southeast': return 1;

          case 'southwest': return 2;

          case 'northwest': return 3;

          default: return -1;

        }

      })()

    };



    try {

      const response = await axios.post('http://127.0.0.1:8000/api/predict/', formatted);

      if (response.status === 200) {

        setResult(response.data.prediction.toFixed(2));

        setFormattedData(formatted); // Store formatted data for details page

      } else {

        throw new Error('An error occurred while fetching the prediction.');

      }

    } catch (error) {

      console.error('Error:', error);

      setError('An error occurred. Please try again later.');

    } finally {

      setLoading(false);

    }

  };



  return (

    <div className="insurance-form-container">

      <h2>Medical Insurance Cost Prediction</h2>

      <form onSubmit={handleSubmit}>

        <div>

          <label>Age:</label>

          <input

            type="number"

            name="age"

            value={formData.age}

            onChange={handleChange}

            min="0"

            max="120"

          />

        </div>

        <div>

          <label>Sex:</label>

          <select name="sex" value={formData.sex} onChange={handleChange}>

            <option value="male">Male</option>

            <option value="female">Female</option>

          </select>

        </div>

        <div>

          <label>BMI:</label>

          <input

            type="number"

            name="bmi"

            value={formData.bmi}

            onChange={handleChange}

            step="0.1"

            min="10"

            max="50"

          />

        </div>

        <div>

          <label>Children:</label>

          <input

            type="number"

            name="children"

            value={formData.children}

            onChange={handleChange}

            min="0"

            max="10"

          />

        </div>

        <div>

          <label>Smoker:</label>

          <select name="smoker" value={formData.smoker} onChange={handleChange}>

            <option value="no">No</option>

            <option value="yes">Yes</option>

          </select>

        </div>

        <div>

          <label>Region:</label>

          <select name="region" value={formData.region} onChange={handleChange}>

            <option value="northeast">Northeast</option>

            <option value="southeast">Southeast</option>

            <option value="southwest">Southwest</option>

            <option value="northwest">Northwest</option>

          </select>

        </div>

        <button type="submit" disabled={loading}>

          {loading ? 'Loading...' : 'Get Prediction'}

        </button>

      </form>



      {error && <p className="error">{error}</p>}

      {result && (

        <>

          <p>Predicted Insurance Cost: ${result}</p>

          <button className="view-details-btn" onClick={handleViewDetails}>

            View Details

          </button>

        </>

      )}

    </div>

  );

};



export default InsuranceForm;