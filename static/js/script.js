async function predict() {
    // Get input values from the form
    const glucose = document.getElementById('glucose').value;
    const bloodPressure = document.getElementById('bloodPressure').value;
    const bmi = document.getElementById('bmi').value;

    try {
        // Send the input data to the server via POST request
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                Glucose: parseFloat(glucose),
                BloodPressure: parseFloat(bloodPressure),
                BMI: parseFloat(bmi),
            }),
        });

        // Parse the response JSON
        const data = await response.json();
        const resultElement = document.getElementById('result'); 

        if (data.error) {
            //Display
            resultElement.innerText = `Error: ${data.error}`;
            resultElement.className = 'result error';
        } else {
            resultElement.innerText = `Prediction: ${data.prediction}`;
            resultElement.className = data.prediction.includes('Negative')
                ? 'result success' 
                : 'result error';  
        }
    } catch (error) {
        const resultElement = document.getElementById('result');
        resultElement.innerText = `Error: ${error.message}`;
        resultElement.className = 'result error'; 
    }
}
