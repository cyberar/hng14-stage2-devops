const express = require('express');
const axios = require('axios');
const path = require('path');
const http = require('http'); // required for socket.io for axios to keep the connection alive
const app = express();

const API_URL = "http://localhost:8000";

const httpAgent = new http.Agent({ keepAlive: true, maxSockets: 10 });
const apiClient = axios.create({
  baseURL: API_URL,
  httpAgent
});

app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));

app.post('/submit', async (req, res) => {
  try {
    const response = await apiClient.post('/jobs');  // Use the axios instance with keep-alive
    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: "something went wrong" });
  }
});

app.get('/status/:id', async (req, res) => {
  try {
    const response = await apiClient.get(`/jobs/${req.params.id}`);  // Use the axios instance with keep-alive
    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: "something went wrong" });
  }
});

app.listen(3000, () => {
  require('events').EventEmitter.defaultMaxListeners = 20;
  console.log('Frontend running on port 3000');
});
