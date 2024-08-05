const fs = require('fs');
const { google } = require('googleapis');
const nodemailer = require('nodemailer');

const SCOPES = ['https://www.googleapis.com/auth/gmail.send'];
const TOKEN_PATH = 'token.json';
const CREDENTIALS_PATH = 'credentials.json';

async function authorize() {
    const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH));
    const { client_secret, client_id, redirect_uris } = credentials.installed;
    const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

    if (fs.existsSync(TOKEN_PATH)) {
        const token = fs.readFileSync(TOKEN_PATH);
        oAuth2Client.setCredentials(JSON.parse(token));
        return oAuth2Client;
    } else {
        return getNewToken(oAuth2Client);
    }
}

function getNewToken(oAuth2Client) {
    const authUrl = oAuth2Client.generateAuthUrl({
        access_type: 'offline',
        scope: SCOPES,
    });
    console.log('Authorize this app by visiting this url:', authUrl);
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });
    rl.question('Enter the code from that page here: ', (code) => {
        rl.close();
        oAuth2Client.getToken(code, (err, token) => {
            if (err) return console.error('Error retrieving access token', err);
            oAuth2Client.setCredentials(token);
            fs.writeFileSync(TOKEN_PATH, JSON.stringify(token));
            console.log('Token stored to', TOKEN_PATH);
        });
    });
}

async function sendMail(auth) {
    const gmail = google.gmail({ version: 'v1', auth });
    const transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            type: 'OAuth2',
            user: 'your-email@gmail.com',
            clientId: auth._clientId,
            clientSecret: auth._clientSecret,
            refreshToken: auth.credentials.refresh_token,
            accessToken: auth.credentials.access_token,
        },
    });

    const mailOptions = {
        from: 'your-email@gmail.com',
        to: 'recipient@example.com',
        subject: 'Test Gmail API',
        text: 'Hello from Gmail API!',
    };

    const result = await transporter.sendMail(mailOptions);
    console.log('Email sent:', result);
}

authorize().then(sendMail).catch(console.error);
