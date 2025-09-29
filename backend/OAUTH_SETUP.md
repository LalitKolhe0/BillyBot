# OAuth2 Social Authentication Setup Guide

This guide will help you set up Google, Facebook, and Apple OAuth2 authentication for BillyBot.

## 1. Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```env
# Database Configuration
DATABASE_URL=sqlite:///./billybot.db

# JWT Configuration
SECRET_KEY=your-secret-key-change-this-in-production

# Google OAuth2
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/callback/google

# Facebook OAuth2
FACEBOOK_CLIENT_ID=your-facebook-client-id
FACEBOOK_CLIENT_SECRET=your-facebook-client-secret
FACEBOOK_REDIRECT_URI=http://localhost:3000/auth/callback/facebook

# Apple OAuth2
APPLE_CLIENT_ID=your-apple-client-id
APPLE_CLIENT_SECRET=your-apple-client-secret
APPLE_REDIRECT_URI=http://localhost:3000/auth/callback/apple
```

## 2. Google OAuth2 Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Set application type to "Web application"
6. Add authorized redirect URIs:
   - `http://localhost:3000/auth/callback/google` (development)
   - `https://yourdomain.com/auth/callback/google` (production)
7. Copy the Client ID and Client Secret to your `.env` file

## 3. Facebook OAuth2 Setup

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app or select an existing one
3. Add "Facebook Login" product
4. Go to "Facebook Login" → "Settings"
5. Add valid OAuth redirect URIs:
   - `http://localhost:3000/auth/callback/facebook` (development)
   - `https://yourdomain.com/auth/callback/facebook` (production)
6. Copy the App ID and App Secret to your `.env` file

## 4. Apple OAuth2 Setup

1. Go to [Apple Developer Console](https://developer.apple.com/)
2. Create a new App ID
3. Create a new Service ID for web authentication
4. Configure the Service ID with your domain
5. Create a private key for the Service ID
6. Copy the Service ID and private key to your `.env` file

## 5. Frontend Setup

The frontend is already configured to handle OAuth2 callbacks. Make sure your React app is running on `http://localhost:3000` for development.

## 6. Testing

1. Start the backend server: `python main.py`
2. Start the frontend: `npm start`
3. Visit `http://localhost:3000`
4. Click on any social login button
5. Complete the OAuth2 flow
6. You should be redirected back to the app and logged in

## 7. Production Deployment

For production deployment:

1. Update all redirect URIs to use your production domain
2. Update the environment variables with production values
3. Ensure your domain is verified with all OAuth providers
4. Update CORS settings in `main.py` to allow your production domain

## 8. Security Notes

- Never commit your `.env` file to version control
- Use strong, unique secrets for production
- Regularly rotate your OAuth2 credentials
- Monitor OAuth2 usage and set up alerts for suspicious activity
- Use HTTPS in production for all OAuth2 redirects
