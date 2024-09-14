//Get the data from ThingsBoard 
const express = require('express');
const axios = require('axios');

const app = express();
const port = 3000;

app.use(express.json());

//to get all devices tokens
app.get('/telemetry/:deviceAccessToken', async (req, res) => {
  const deviceAccessToken = req.params.deviceAccessToken;
  const thingsboardUrl = `https://demo.thingsboard.io/api/v1/${deviceAccessToken}/telemetry`;

  try {
    const response = await axios.get(thingsboardUrl);
    res.json(response.data);
  } catch (error) {
    res.status(error.response ? error.response.status : 500).json({
      message: 'Error fetching telemetry data',
      error: error.response ? error.response.data : error.message
    });
  }
});

app.get('/devices', async (req, res) => {
  const jwtToken = 'your_jwt_token'; // Replace with our JWT token
  const thingsboardUrl = 'https://demo.thingsboard.io/api/admin/devices';

  try {
    const response = await axios.get(thingsboardUrl, {
      headers: {
        'X-Authorization': `Bearer ${jwtToken}`
      }
    });
    res.json(response.data);
  } catch (error) {
    res.status(error.response ? error.response.status : 500).json({
      message: 'Error listing devices',
      error: error.response ? error.response.data : error.message
    });
  }
});


app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
