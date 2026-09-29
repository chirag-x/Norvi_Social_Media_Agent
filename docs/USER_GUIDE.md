# Nexus - User Guide & Setup

Welcome to the **Nexus**, your autonomous pipeline for discovering, creating, and publishing viral content.

## 🚀 How to Use the App

The Nexus is designed to be a fully autonomous workflow. Here is how you use it:

1. **Dashboard:** Your central command center. Ensure that the 🧠 Brain (AI Engine and Model) is connected and ready.
2. **Settings:** First, head to Settings and authenticate your Social Media accounts (like YouTube). This gives the agent permission to upload videos on your behalf.
3. **Discover:** Go to the Discover tab to search for trending videos in your niche. When you find a video you like, click **Select Source**.
4. **Clip Lab:** The AI will automatically scan the transcript of your selected video and find the most viral segments. Click **Preview Clip** to watch the segment. Click **Approve to Queue** to physically cut and render the video.
5. **Publishing Queue:** All rendered videos end up here. The AI will automatically generate a viral title and description. You can select the platforms (YouTube Shorts, TikTok, Reels) and click **Schedule Upload**.
6. **Calendar:** View all your scheduled posts.
7. **Analytics:** View the performance of your uploaded videos (views, likes, comments).

---

## 🔑 API Keys & Authentication Setup

To allow the Nexus to publish content automatically, you need to set up developer accounts for each platform. 

### 1. YouTube Data API v3 (Google Cloud)
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new Project named `Nexus`.
3. Search for **YouTube Data API v3** and click **Enable**.
4. Go to **APIs & Services > OAuth consent screen**.
   - Choose **External** user type.
   - Fill in the required app information (App name, User support email).
   - Under **Test users**, add the email address of the YouTube channel you want to upload to. **(IMPORTANT: If you don't add your email here, you cannot log in).**
5. Go to **Credentials > Create Credentials > OAuth client ID**.
   - Application type: **Desktop app**.
   - Click Create. Download the JSON file.
6. Rename the file to `client_secret.json` and place it in the `E:\Nexus_Social_Media_Agent\app_data\` folder.
7. Go to the **Settings** tab in the Nexus app and click **Save & Authenticate**.

**Note on Privacy:** Because your app is in "Testing" mode on Google Cloud, YouTube forces all API uploads to be **Private**. You must manually make them Public in YouTube Studio until you verify your app with Google.

### 2. TikTok API (Coming Soon)
1. Go to the TikTok for Developers portal.
2. Register a new App and apply for the **Content Posting API**.
3. Once approved, copy your `Client Key` and `Client Secret` into the Settings tab.

### 3. Instagram Graph API (Coming Soon)
1. Go to the Meta for Developers portal.
2. Create an App with the **Business** type.
3. Add the **Instagram Graph API** product.
4. Generate a Long-Lived Access Token for your linked Instagram Professional account and paste it into the Settings tab.
