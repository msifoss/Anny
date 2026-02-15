# Service Account Setup Guide

How to configure Google service account credentials for Anny.

## Prerequisites

- A Google Cloud project (or permission to create one)
- Access to at least one of: GA4 property, Search Console site, GTM account
- `gcloud` CLI installed (optional but helpful)

## 1. Create or Select a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note the **Project ID** (you'll need it later)

## 2. Enable APIs

Enable all three APIs in your project:

1. [Analytics Data API](https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com) (GA4)
2. [Search Console API](https://console.cloud.google.com/apis/library/searchconsole.googleapis.com)
3. [Tag Manager API](https://console.cloud.google.com/apis/library/tagmanager.googleapis.com)

Or via CLI:

```bash
gcloud services enable analyticsdata.googleapis.com
gcloud services enable searchconsole.googleapis.com
gcloud services enable tagmanager.googleapis.com
```

## 3. Create a Service Account

1. Go to [IAM & Admin > Service Accounts](https://console.cloud.google.com/iam-admin/service-accounts)
2. Click **Create Service Account**
3. Name: `anny-reader` (or any name you prefer)
4. Description: "Read-only access for Anny analytics tool"
5. Click **Create and Continue**
6. Skip the optional role assignment (access is granted at the product level, not project level)
7. Click **Done**

### Download the JSON Key

1. Click on the service account you just created
2. Go to the **Keys** tab
3. Click **Add Key > Create new key**
4. Select **JSON** format
5. Download and save the file (e.g., `anny-service-account.json`)
6. Store it securely outside version control

> The `.gitignore` already blocks `*service-account*.json` and `*service_account*.json` patterns.

## 4. Grant Access to Each Service

### GA4 (Google Analytics 4)

1. Go to [Google Analytics](https://analytics.google.com/)
2. Navigate to **Admin > Property > Property Access Management**
3. Click the **+** button, then **Add users**
4. Enter the service account email (e.g., `anny-reader@your-project.iam.gserviceaccount.com`)
5. Set role to **Viewer** (read-only)
6. Click **Add**

**Find your Property ID:**
- In GA4, go to **Admin > Property > Property Details**
- Copy the **Property ID** (numeric, e.g., `123456789`)
- For the `.env` file, use the format: `properties/123456789`

### Search Console

1. Go to [Google Search Console](https://search.google.com/search-console/)
2. Select your property
3. Go to **Settings > Users and permissions**
4. Click **Add user**
5. Enter the service account email
6. Set permission to **Restricted** (read-only)
7. Click **Add**

**Find your Site URL:**
- Use exactly the URL shown in Search Console (e.g., `https://example.com/` or `sc-domain:example.com`)

### GTM (Google Tag Manager)

1. Go to [Google Tag Manager](https://tagmanager.google.com/)
2. Click on your account
3. Go to **Admin > Account > User Management**
4. Click the **+** button, then **Add users**
5. Enter the service account email
6. Set access to **Read** (at the account level to access all containers)
7. Click **Invite**

## 5. Configure Environment

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Path to your downloaded JSON key file
GOOGLE_SERVICE_ACCOUNT_KEY_PATH=path/to/anny-service-account.json

# GA4 Property ID (from Analytics Admin > Property Details)
GA4_PROPERTY_ID=properties/123456789

# Search Console Site URL (exactly as shown in Search Console)
SEARCH_CONSOLE_SITE_URL=https://example.com
```

## 6. Verify Setup

Run the smoke test to confirm everything works:

```bash
make smoke
```

Or run the automated e2e tests:

```bash
ANNY_E2E=1 make e2e
```

## Troubleshooting

### "Could not load credentials"
- Verify `GOOGLE_SERVICE_ACCOUNT_KEY_PATH` points to a valid JSON file
- Check the file contains `"type": "service_account"`

### 403 Forbidden on GA4
- Confirm the service account email is added as a Viewer in GA4 Admin
- Wait a few minutes after granting access (propagation delay)
- Verify `GA4_PROPERTY_ID` uses the `properties/` prefix

### 403 Forbidden on Search Console
- Confirm the service account email is added in Search Console Settings
- Verify `SEARCH_CONSOLE_SITE_URL` matches exactly (trailing slash matters)

### 403 Forbidden on GTM
- Confirm the service account has Read access at the account level
- Container-level access alone is not sufficient for listing accounts

### Empty results
- GA4 and Search Console may return empty results for new properties
- Try `last_28_days` date range for maximum data availability
- Search Console data has a ~3 day processing delay
