# Master Guide: Generating Developer API Keys

To allow the Nexus to automatically upload videos to your accounts, you must generate secure Developer API keys. This acts as a secure backdoor, ensuring the app never needs to know your actual passwords.

---

## 🟥 1. YouTube (YouTube Data API v3)

1. **Go to Google Cloud Console:** Navigate to [console.cloud.google.com](https://console.cloud.google.com/).
2. **Create a Project:** Click the dropdown in the top left and click **New Project**. Name it `Nexus`.
3. **Enable the API:** In the left sidebar, go to **APIs & Services** > **Library**. Search for "YouTube Data API v3" and click **Enable**.
4. **Configure Consent Screen:** Go to **APIs & Services** > **OAuth consent screen**. Select **External**. Fill in your email and app name. 
5. **Verify Your Email (CRITICAL STEP):** In the left sidebar, click on **Audience** (under Google Auth Platform). Scroll down to the **Test Users** section. You MUST click "+ Add Users" and type in your exact YouTube email address. If you skip this, Google will throw an "Error 403: Access Denied" when you try to log in!
6. **Generate Keys:** Go to **APIs & Services** > **Credentials**. Click **+ Create Credentials** at the top and select **OAuth client ID**.
7. **Application Type:** Select **Desktop app**.
8. **Copy Keys:** Google will provide your **Client ID** and **Client Secret**. Copy these into the Nexus Settings tab.

---

## 🎵 2. TikTok (TikTok Content Posting API)

**Privacy Note:** Unlike YouTube, TikTok does not strictly force videos to be Private for test users, but it often sends API-uploaded videos directly to your **Drafts** or Inbox for final approval depending on your developer scope. 

1. **Go to the Developer Portal:** Navigate to [developers.tiktok.com](https://developers.tiktok.com/).
2. **Log In:** Log in with the TikTok account you want the agent to post to.
3. **Create an App:** Click **My Apps** in the top right, then **+ Connect a new app**.
4. **App Details:** Name it `Nexus`, upload a logo, and set the platform to "Web" or "Desktop".
5. **Request Permissions:** You need to request access to the **"Video Publishing"** scope. In the description, simply state: *"This is a private, personal tool to help me schedule and upload my own content to my own account."*
6. **Authentication Flow:** Similar to YouTube, TikTok uses an OAuth flow. Once you paste your Client Key and Secret into Nexus, clicking "Authenticate" will pop open a TikTok login page for you to grant access.
7. **Copy Keys:** Once approved, click on your app to view the dashboard. Copy your **Client Key** and **Client Secret** into the Nexus.

---

## 📸 3. Instagram & Facebook (Meta for Developers)
*(Note: You will use the exact same App ID and Secret for both Facebook and Instagram in the Nexus Settings).*

**Privacy Note:** Meta's Graph API allows you to post **Publicly** even in Testing Mode (Standard Access) as long as the Facebook Page or Instagram Account you are posting to is owned by the same admin account that created the Developer App!

1. **Go to Meta for Developers:** Navigate to [developers.facebook.com](https://developers.facebook.com/).
2. **Create an App:** Log in, go to **My Apps**, and click **Create App**.
3. **App Type:** Select **"Other"** -> **"Business"**. Name it `Nexus`.
4. **Link Instagram & Facebook:** In the App Dashboard, scroll down to "Add products to your app" and set up the **Instagram Graph API** and **Facebook Graph API**.
5. **Generate the Token (Manual Auth):** Meta is slightly different. Instead of a browser pop-up in the app, you generate a long-lived Access Token directly in their dashboard.
   - Go to **Tools** > **Graph API Explorer** (in the top menu).
   - In the "Permissions" dropdown, add: `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement`, and `pages_manage_posts`.
   - Click **Generate Access Token**.
6. **Copy Keys:** Go back to your App Dashboard -> Settings -> Basic to find your **App ID** and **App Secret**. Copy those, along with the **Access Token** you just generated, into the Nexus.

---

## 🐦 4. X / Twitter (X API v2)

1. **Go to the Developer Portal:** Navigate to [developer.x.com](https://developer.x.com/).
2. **Sign Up:** Log in with your X account and sign up for the **Free Tier**.
3. **Create a Project & App:** Click **+ Create Project**. Name it `Nexus`.
4. **Change App Permissions:** By default, apps are "Read-Only". You MUST go to your App Settings, click **User authentication settings**, enable OAuth 1.0a, and change the permissions to **"Read and Write"**. (Use `http://127.0.0.1` for the callback URL).
5. **Generate Keys:** Go to the **Keys and Tokens** tab. 
6. **Copy Keys:** You will need to generate and copy four things into the Nexus:
   - **API Key** (Consumer Key)
   - **API Key Secret**
   - **Access Token**
   - **Access Token Secret**
