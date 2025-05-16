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

    try {
        const parsedUrl = new URL(url);
        const allowedDomains = ['example.com', 'api.example.com']; // Add trusted domains here
        const allowedProtocol = 'https:';

        // Validate protocol
        if (parsedUrl.protocol !== allowedProtocol) {
            return res.status(403).send('Forbidden: Only HTTPS protocol is allowed');
        }

        // Validate hostname
        if (!allowedDomains.includes(parsedUrl.hostname)) {
            return res.status(403).send('Forbidden: URL is not allowed');
        }

        // Construct the URL using trusted components
        const trustedUrl = `${allowedProtocol}//${parsedUrl.hostname}${parsedUrl.pathname}`;

        // Make the request
        request({ url: trustedUrl, method: 'GET', qs: parsedUrl.searchParams }).pipe(res);
    } catch (err) {
        return res.status(400).send('Invalid URL');
    }
});

app.listen(PORT, () => {
    console.log(`Proxy server is running on port ${PORT}`);
});

