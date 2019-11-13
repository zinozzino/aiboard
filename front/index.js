const express = require('express');
const request = require('request');
const bodyParser = require('body-parser');
const axios = require('axios');

const { APP_URI = 'http://112.150.189.246:5000', HOST = '0.0.0.0', PORT = '8000'} = process.env;

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.set('view engine', 'ejs')

app.get('/', (req, res) => {
    return res.status(200).render('./index')
})

app.post('/', async (req, res) => {
    const {question} = req.body;

    const { data } = await axios.post(`${APP_URI}/plugin/classify`, { question }, {headers: {'Content-Type': 'application/json'}})

    return res.status(201).json(data);
})

app.listen(parseInt(PORT, 10), HOST, () => console.log(`server running at ${HOST}:${PORT}`));
