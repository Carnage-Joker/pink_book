const fs = require('fs');
const { google } = require('googleapis');
const http = require('http');
const url = require('url');
const opn = require('open');
const destroyer = require('server-destroy');

const SCOPES = ['https://www.googleapis.com/auth/gmail.send'];
const TOKEN_PATH = 'token.json';

// Load client secrets from a local file.
fs.readFile('credentials.json', (err, content) => {
    if (err) return console.log('Error loading client secret file:', err);
    authorize(JSON.parse(content), sendEmail);
});

function authorize(credentials, callback) {
    const { client_secret, client_id, redirect_uris } = credentials.web;
    const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

    fs.readFile(TOKEN_PATH, (err, token) => {
        if (err) return getAccessToken(oAuth2Client, callback);
        oAuth2Client.setCredentials(JSON.parse(token));
        callback(oAuth2Client);
    });
}

function getAccessToken(oAuth2Client, callback) {
    const authUrl = oAuth2Client.generateAuthUrl({
        access_type: 'offline',
        scope: SCOPES,
    });
    console.log('Authorize this app by visiting this url:', authUrl);
    opn(authUrl);

    const server = http.createServer((req, res) => {
        if (req.url.indexOf('/oauth2callback') > -1) {
            const qs = new url.URL(req.url, 'http://localhost:3000').searchParams;
            res.end('Authentication successful! Please return to the console.');
            server.destroy();
            const code = qs.get('code');
            oAuth2Client.getToken(code, (err, token) => {
                if (err) return console.error('Error retrieving access token', err);
                oAuth2Client.setCredentials(token);
                fs.writeFile(TOKEN_PATH, JSON.stringify(token), (err) => {
                    if (err) return console.error(err);
                    console.log('Token stored to', TOKEN_PATH);
                });
                callback(oAuth2Client);
            });
        }
    }).listen(3000, () => {
        console.log('Server listening on http://localhost:3000');
    });
    destroyer(server);
}

function sendEmail(auth) {
    const gmail = google.gmail({ version: 'v1', auth });
    const raw = makeBody('recipient@example.com', 'sender@example.com', 'Subject', 'Message text');
    gmail.users.messages.send({
        userId: 'me',
        resource: { raw: raw },
    }, (err, res) => {
        if (err) return console.log('The API returned an error: ' + err);
        console.log('Email sent:', res.data);
    });
}

function makeBody(to, from, subject, message) {
    const str = [
        'Content-Type: text/plain; charset="UTF-8"\n',
        'MIME-Version: 1.0\n',
        'Content-Transfer-Encoding: 7bit\n',
        `to: ${to}\n`,
        `from: ${from}\n`,
        `subject: ${subject}\n\n`,
        message,
    ].join('');

    return Buffer.from(str)
        .toString('base64')
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');
}
