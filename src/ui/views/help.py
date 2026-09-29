from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QScrollArea, QLabel
from PySide6.QtCore import Qt
from src.ui.components.collapsible import CollapsibleSection

class HelpView(QWidget):
    """
    Help and Documentation View.
    Renders the help sections as premium accordions.
    """
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        
        title = QLabel("Help Center")
        title.setProperty("class", "title")
        main_layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_content = QWidget()
        self.layout = QVBoxLayout(scroll_content)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(15)
        
        self._build_section("🚀 How to Use the App", self.get_usage_md())
        self._build_section("1. YouTube Data API v3 (Google Cloud)", self.get_yt_md())
        self._build_section("2. TikTok for Developers", self.get_tiktok_md())
        self._build_section("3. Instagram Graph API (Meta)", self.get_ig_md())
        self._build_section("4. Facebook Graph API (Meta)", self.get_fb_md())
        self._build_section("5. X (Twitter) API v2", self.get_x_md())
        self._build_section("6. Groq API (Cloud Transcription)", self.get_groq_md())
        self._build_section("7. Contact Norvi Support", self.get_support_md(), extra_widget=self.get_support_buttons())
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

    def _build_section(self, title: str, markdown_content: str, extra_widget=None):
        section = CollapsibleSection(title)
        
        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        # No hardcoded color — let the theme handle it so light mode works
        browser.setStyleSheet("""
            QTextBrowser {
                background-color: transparent;
                border: none;
                font-family: "Segoe UI", sans-serif;
                font-size: 14px;
            }
        """)
        lines = len(markdown_content.split("\n"))
        browser.setMinimumHeight(min(600, max(150, lines * 22)))
        browser.setMarkdown(markdown_content)
        
        section.addWidget(browser)
        
        if extra_widget:
            section.addWidget(extra_widget)
            
        self.layout.addWidget(section)

    # ── Section content ───────────────────────────────────────────────────────

    def get_usage_md(self):
        return """## Nexus — Workflow Overview

The app follows a 7-step autonomous pipeline:

**Step 1 — Dashboard**
Your command center. Check that the 🧠 AI Pipeline status shows **Active** and at least one platform is connected. If the AI Pipeline shows an error, restart Ollama or check your internet connection.

**Step 2 — Settings**
Before using the app, go to Settings and add your API keys for every platform you want to post to. Each platform has its own section. Read the matching guide below for step-by-step instructions.

**Step 3 — Discover**
Search for a trending video in your niche or paste a direct YouTube URL. Click **Select Source** on the video you want to clip.

**Step 4 — Clip Lab**
1. Check all three Fair Use boxes.
2. Select your maximum clip duration (30s / 60s / 90s / 120s / 180s).
3. Click **Analyze with AI**. The system will download the audio, transcribe it, and ask the AI to find the best viral moments.
4. Click **Preview Clip** to watch any clip before approving.
5. Click **Approve to Queue** to render and add it to the Publishing Queue.

**Step 5 — Publishing Queue**
1. Select a clip from the left panel.
2. Click **Generate Metadata (AI)** for an AI-written title and description.
3. Select your target platforms.
4. Set the publish date/time (defaults to 2 hours from now).
5. Toggle **Give Credits to Nexus** on or off.
6. Click **Schedule Upload**.

**Step 6 — Calendar**
View all your scheduled uploads. Select any row and click **Remove Selected** to cancel it.

**Step 7 — Analytics**
See your top videos, total clips extracted, videos scheduled, and published count."""

    def get_yt_md(self):
        return """## YouTube Data API v3 — Step-by-Step Setup

**What you need:** A Google account with a YouTube channel.

---

### Step 1 — Create a Google Cloud Project
1. Open [Google Cloud Console](https://console.cloud.google.com/) and sign in.
2. Click the project dropdown at the top → **New Project**.
3. Name it `Nexus` → Click **Create**.
4. Wait for the project to be created, then select it.

---

### Step 2 — Enable the YouTube API
1. In the left menu go to **APIs & Services → Library**.
2. Search for `YouTube Data API v3`.
3. Click on it and press **Enable**.

---

### Step 3 — Configure OAuth Consent Screen
1. Go to **APIs & Services → OAuth consent screen**.
2. Select **External** → Click **Create**.
3. Fill in:
   - **App name:** `Nexus`
   - **User support email:** your Google email
   - **Developer contact email:** your Google email
4. Click **Save and Continue** through Scopes (no changes needed).
5. On the **Test Users** page — click **Add Users** and add **the email of your YouTube channel** (this is critical — if you skip this, login will fail).
6. Click **Save and Continue** → **Back to Dashboard**.

---

### Step 4 — Create OAuth Credentials
1. Go to **APIs & Services → Credentials**.
2. Click **+ Create Credentials → OAuth client ID**.
3. Application type: **Desktop app**.
4. Name: `Nexus Desktop`.
5. Click **Create**.
6. A popup shows your **Client ID** and **Client Secret** — copy both.

---

### Step 5 — Add to Nexus Settings
1. Open **Settings** in the app.
2. Scroll to **YouTube** section.
3. Paste your **Client ID** and **Client Secret**.
4. Click **Save & Authenticate** — a browser window will open to log in with your Google account.

> ⚠️ **Important:** While your app is in Google's *Testing* mode, YouTube forces all API uploads to be **Private**. After upload, go to YouTube Studio and manually change visibility to Public/Unlisted. To remove this restriction, submit your app for Google verification (advanced — optional)."""

    def get_tiktok_md(self):
        return """## TikTok for Developers — Step-by-Step Setup

**What you need:** A TikTok account with a registered developer app.

---

### Step 1 — Register as a TikTok Developer
1. Go to [TikTok for Developers](https://developers.tiktok.com/) and sign in with your TikTok account.
2. Click **Manage Apps → Create an App**.
3. Choose **Web** as the platform (or **Mobile**).
4. Fill in your app name (e.g. `Nexus`) and description.

---

### Step 2 — Apply for Content Posting API
1. Inside your app, go to **Products**.
2. Find **Content Posting API** and click **Apply**.
3. Fill in the use-case form explaining you are building a social media scheduling tool.
4. Submit and wait for TikTok's approval (usually 1–7 business days).

---

### Step 3 — Get Your Keys
1. Once approved, go to your app's **Keys & Credentials** tab.
2. Copy your **Client Key** (also called App ID) and **Client Secret**.

---

### Step 4 — Add to Nexus Settings
1. Open **Settings** in the app.
2. Scroll to **TikTok** section.
3. Paste your **Client Key** and **Client Secret**.
4. Click **Save & Authenticate** — a browser window will open to authorize your TikTok account.

> 💡 TikTok requires a business/creator account for the Content Posting API. Personal accounts may be rejected."""

    def get_ig_md(self):
        return """## Instagram Graph API — Step-by-Step Setup

**What you need:** An Instagram Professional account (Creator or Business) linked to a Facebook Page.

---

### Step 1 — Convert to Professional Account
1. Open Instagram → Profile → ☰ Menu → **Settings and Privacy**.
2. Go to **Account → Switch to Professional Account**.
3. Choose **Creator** or **Business**.
4. Link it to a **Facebook Page** (required by Meta's API).

---

### Step 2 — Create a Meta Developer App
1. Go to [Meta for Developers](https://developers.facebook.com/) and log in.
2. Click **My Apps → Create App**.
3. Choose type: **Business**.
4. Fill in App name: `Nexus` and your contact email.
5. Click **Create App**.

---

### Step 3 — Add Instagram Graph API
1. Inside your app, click **Add Products**.
2. Find **Instagram Graph API** → Click **Set Up**.

---

### Step 4 — Generate a Long-Lived Access Token
1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/).
2. In the top-right dropdown, select your **Nexus** app.
3. Click **Generate Access Token** and log in with your Facebook account.
4. Add these permissions: `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`.
5. Click **Generate Access Token** again.
6. Copy the short-lived token, then exchange it for a long-lived token (60 days) by going to the **Access Token Debugger → Extend Access Token**.

---

### Step 5 — Find Your Instagram Business Account ID
1. In Graph API Explorer, call: `GET /me/accounts`
2. Find the page linked to your Instagram — copy the **Page ID**.
3. Then call: `GET /{page-id}?fields=instagram_business_account`
4. Copy the **Instagram Business Account ID**.

---

### Step 6 — Add to Nexus Settings
1. Open **Settings → Instagram**.
2. Paste: **App ID**, **App Secret**, **Access Token**, and **Instagram Account ID**.
3. Click **Save**.

> ⚠️ Access tokens expire after ~60 days. You will need to regenerate and repaste them periodically."""

    def get_fb_md(self):
        return """## Facebook Graph API — Step-by-Step Setup

**What you need:** A Facebook Page (not a personal profile) — pages are free to create.

---

### Step 1 — Create a Facebook Page (if you don't have one)
1. On Facebook, click **Pages → Create New Page**.
2. Give it a name and category relevant to your content.

---

### Step 2 — Use Your Existing Meta Developer App
1. Go to [Meta for Developers](https://developers.facebook.com/).
2. Open the **Nexus** app you created for Instagram (or create a new one).

---

### Step 3 — Add Required Permissions
1. Inside the app, go to **App Review → Permissions and Features**.
2. Request or enable these permissions:
   - `publish_video`
   - `pages_manage_posts`
   - `pages_read_engagement`

---

### Step 4 — Generate a Page Access Token
1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/).
2. Select your **Nexus** app.
3. Click **Generate Access Token** and log in.
4. From the dropdown that appears, select your **Facebook Page** (not "Me").
5. Add permissions: `publish_video`, `pages_manage_posts`.
6. Click **Generate Access Token**.
7. Extend to a long-lived token via **Access Token Debugger → Extend Access Token**.

---

### Step 5 — Find Your Page ID
1. Go to your Facebook Page.
2. Click **About** → scroll down to find **Page ID**.

---

### Step 6 — Add to Nexus Settings
1. Open **Settings → Facebook**.
2. Paste: **App ID**, **App Secret**, **Page Access Token**, and **Page ID**.
3. Click **Save**.

> 💡 Facebook and Instagram use the **same Meta App** — you only need to create one app for both platforms."""

    def get_x_md(self):
        return """## X (Twitter) API v2 — Step-by-Step Setup

**What you need:** An X (Twitter) account. A paid X Developer subscription is required for video upload (Basic plan — ~USD 100/month).

---

### Step 1 — Apply for X Developer Access
1. Go to [X Developer Portal](https://developer.twitter.com/en/portal/dashboard).
2. Sign in with your X account.
3. Apply for a **Developer account** — fill in the use-case form (social media automation tool).
4. Wait for approval (usually instant or within 24h).

---

### Step 2 — Create a Project and App
1. In the Developer Portal, click **+ Create Project**.
2. Name it `Nexus`.
3. Select use case: **Making a bot** or **Building tools for businesses**.
4. Inside the project, click **+ Add App**.
5. Name it `Nexus App`.

---

### Step 3 — Enable Read and Write Permissions
1. Inside your app, go to **Settings → User Authentication Settings**.
2. Click **Set Up**.
3. Set **App permissions** to **Read and Write**.
4. Set **Type of App** to **Native App**.
5. For **Callback URI**: enter `http://localhost:8080/callback`.
6. For **Website URL**: enter your website (or `https://nor-vi.in`).
7. Click **Save**.

---

### Step 4 — Generate API Keys
1. Go to your app's **Keys and Tokens** tab.
2. Under **Consumer Keys**, click **Regenerate** → copy **API Key** and **API Key Secret**.
3. Under **Authentication Tokens**, click **Generate** → copy **Access Token** and **Access Token Secret**.
4. Make sure the access token shows **Read and Write** permissions.

---

### Step 5 — Add to Nexus Settings
1. Open **Settings → X (Twitter)**.
2. Paste all 4 values:
   - **API Key** (Consumer Key)
   - **API Secret** (Consumer Secret)
   - **Access Token**
   - **Access Token Secret**
3. Click **Save**.

> ⚠️ X's free tier does **not** support video uploads. You need at least the **Basic** developer plan. Check [X Developer pricing](https://developer.twitter.com/en/portal/products)."""

    def get_groq_md(self):
        return """## Groq API — Cloud Transcription Setup

**What you need:** A free Groq account. Groq is 10–50x faster than local Whisper transcription.

---

### Step 1 — Create a Groq Account
1. Go to [Groq Cloud Console](https://console.groq.com/).
2. Click **Sign Up** and create a free account (no credit card required for the free tier).
3. Verify your email.

---

### Step 2 — Generate an API Key
1. After logging in, click **API Keys** in the left menu.
2. Click **Create API Key**.
3. Give it a name: `Nexus`.
4. Click **Submit** — the key is shown **only once**, so copy it immediately.
5. Store it somewhere safe (e.g. a password manager).

---

### Step 3 — Add to Nexus Settings
1. Open **Settings** in the app.
2. Scroll to **System Maintenance & Integrations**.
3. Find the **Groq API Key** field.
4. Paste your key and click **Save**.

---

### Step 4 — Switch Transcription Engine
1. In **Settings**, find the **Transcription Engine** selector.
2. Switch from **Local (Whisper)** to **Cloud (Groq API)**.
3. Select model: `whisper-large-v3-turbo` (recommended — fastest and most accurate).

---

### Free Tier Limits
| Metric | Free Limit |
|--------|-----------|
| Requests/minute | 20 |
| Audio duration/day | ~7 hours |
| Models available | whisper-large-v3, whisper-large-v3-turbo |

> 💡 For most content creators, the free tier is more than enough. If you hit limits, Groq's paid plans are very affordable."""

    def get_support_md(self):
        return """## Contact Norvi Agency Support

Having trouble setting up your API keys or need a custom automation workflow built for your agency?

Our expert team at Norvi Agency is here to help. Use the buttons below to:
- **Contact Norvi** — opens our official support page in your browser
- **Open Local Logs** — opens your log file so you can read error messages
- **Copy Recent Logs** — copies the last 200 lines to your clipboard to send to us
- **Clear Logs** — wipes the log file to free up disk space"""

    def get_support_buttons(self):
        from PySide6.QtWidgets import QHBoxLayout, QPushButton
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 10, 0, 10)
        
        btn_website = QPushButton("Contact Norvi Agency")
        btn_website.setStyleSheet("background-color: #3B82F6; color: white; border-radius: 6px; padding: 10px; font-weight: bold;")
        btn_website.clicked.connect(lambda: __import__("webbrowser").open("https://nor-vi.in/contact/"))
        
        btn_open_logs = QPushButton("Open Local Logs")
        btn_open_logs.setStyleSheet("background-color: #4B5563; color: white; border-radius: 6px; padding: 10px; font-weight: bold;")
        btn_open_logs.clicked.connect(self._open_logs)
        
        btn_copy_logs = QPushButton("Copy Recent Logs")
        btn_copy_logs.setStyleSheet("background-color: #4B5563; color: white; border-radius: 6px; padding: 10px; font-weight: bold;")
        btn_copy_logs.clicked.connect(self._copy_logs)
        
        btn_clear_logs = QPushButton("Clear Logs")
        btn_clear_logs.setStyleSheet("background-color: #EF4444; color: white; border-radius: 6px; padding: 10px; font-weight: bold;")
        btn_clear_logs.clicked.connect(self._clear_logs)
        
        layout.addWidget(btn_website)
        layout.addWidget(btn_open_logs)
        layout.addWidget(btn_copy_logs)
        layout.addWidget(btn_clear_logs)
        layout.addStretch()
        return container

    def _open_logs(self):
        from pathlib import Path
        from src.config.config import get_config
        import os
        log_file = Path(get_config().app_data_dir) / "logs" / "app.log"
        if log_file.exists():
            os.startfile(log_file)
            
    def _copy_logs(self):
        from pathlib import Path
        from src.config.config import get_config
        from PySide6.QtGui import QGuiApplication
        from PySide6.QtWidgets import QMessageBox
        log_file = Path(get_config().app_data_dir) / "logs" / "app.log"
        if log_file.exists():
            with open(log_file, "r") as f:
                lines = f.readlines()
                recent = "".join(lines[-200:])
                QGuiApplication.clipboard().setText(recent)
                
            msg = QMessageBox()
            msg.setWindowTitle("Logs Copied")
            msg.setText("The last 200 lines of your logs have been copied to your clipboard!")
            msg.exec()
            
    def _clear_logs(self):
        from pathlib import Path
        from src.config.config import get_config
        from PySide6.QtWidgets import QMessageBox
        log_file = Path(get_config().app_data_dir) / "logs" / "app.log"
        if log_file.exists():
            try:
                open(log_file, "w").close()
                msg = QMessageBox()
                msg.setWindowTitle("Logs Cleared")
                msg.setText("Your log file has been successfully cleared to free up memory.")
                msg.exec()
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Error")
                msg.setText(f"Could not clear logs: {e}")
                msg.exec()
