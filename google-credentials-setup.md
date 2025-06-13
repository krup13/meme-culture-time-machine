# Setting Up Google API Credentials

This guide walks you through setting up the necessary Google API credentials for MemeLord Chronos.

## 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Take note of your Project ID

## 2. Enable Required APIs

In your project, navigate to "APIs & Services" > "Library" and enable:

- Google Cloud Vision API
- Google Cloud Speech-to-Text API
- YouTube Data API v3

## 3. Create Service Account for Vision and Speech APIs

1. Navigate to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Name your service account (e.g., "memelord-chronos")
4. Grant the service account the following roles:
   - Cloud Vision API User
   - Cloud Speech-to-Text User
5. Click "Done"

## 4. Generate Service Account Key

1. Click on the service account you just created
2. Go to the "Keys" tab
3. Click "Add Key" > "Create new key"
4. Choose JSON format
5. Download the key file

## 5. Set Up YouTube API Key

1. Navigate to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "API key"
3. Copy your API key
4. (Optional) Restrict the API key to only work with YouTube Data API

## 6. Configure Your Application

1. Place the downloaded JSON key file in your project root as `google-credentials.json`
2. Add the file to your `.gitignore` to prevent uploading sensitive information
3. Update your `.env` file with:

