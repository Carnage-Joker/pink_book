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

    const allowedDomains = {
        'example.com': 'https://example.com',
        'api.example.com': 'https://api.example.com'
    };
    let parsedUrl;
    try {
        parsedUrl = new URL(url);
    } catch (err) {
        return res.status(400).send('Invalid URL');
    }

    const baseUrl = allowedDomains[parsedUrl.hostname];
    if (!baseUrl) {
        return res.status(403).send('URL is not allowed');
    }

    // Prevent path traversal
    const sanitizedPath = parsedUrl.pathname.replace(/(\.\.[/\\])/g, '');
    const finalUrl = new URL(sanitizedPath + parsedUrl.search, baseUrl);

    request({ url: finalUrl.toString(), method: 'GET' }).pipe(res);
});

app.listen(PORT, () => {
    console.log(`Proxy server is running on port ${PORT}`);
});

