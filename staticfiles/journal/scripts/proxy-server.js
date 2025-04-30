// proxy-server.js
const express = require('express');
const request = require('request');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());

app.get('/proxy', (req, res) => {
    const url = req.query.url;
    if (!url) {
        return res.status(400).send('URL query parameter is required');
    }

    const allowedDomains = ['example.com', 'api.example.com'];
    let parsedUrl;
    try {
        parsedUrl = new URL(url);
    } catch (err) {
        return res.status(400).send('Invalid URL');
    }

    if (!allowedDomains.includes(parsedUrl.hostname)) {
        return res.status(403).send('URL is not allowed');
    }

    request({ url: parsedUrl.toString(), method: 'GET' }).pipe(res);
});

app.listen(PORT, () => {
    console.log(`Proxy server is running on port ${PORT}`);
});

