# 🚀 Deployment Guide - Streamlit Cloud

This guide will help you deploy the IPL AI Agents application to Streamlit Cloud via GitHub.

## 📋 Prerequisites

- GitHub account
- Anthropic API Key
- Git installed on your local machine

---

## 🔧 Step 1: Push Code to GitHub

### Initialize Git Repository (if not already done)

```bash
cd /Users/nakulpednekar/CascadeProjects/AI_Agents_New

# Initialize git
git init

# Add remote repository
git remote add origin https://github.com/mayurdhage31/IPL_aap_AI_Agents.git
```

### Add and Commit Files

```bash
# Add all files (excluding those in .gitignore)
git add .

# Check what will be committed
git status

# Create initial commit
git commit -m "Initial commit: IPL AI Agents Streamlit app"
```

### Push to GitHub

```bash
# Push to main branch
git push -u origin main

# If the above fails, try master branch:
# git push -u origin master
```

**Important:** The `.gitignore` file will automatically exclude:
- `.env` file (contains your local API key)
- `__pycache__/` directories
- `.streamlit/secrets.toml` (local secrets)
- Other temporary files

---

## ☁️ Step 2: Deploy to Streamlit Cloud

### 1. Go to Streamlit Cloud

Visit: [https://share.streamlit.io](https://share.streamlit.io)

### 2. Sign In

- Click **"Sign in"**
- Choose **"Continue with GitHub"**
- Authorize Streamlit Cloud to access your GitHub repositories

### 3. Create New App

- Click **"New app"** button
- You'll see a deployment form

### 4. Configure Deployment

Fill in the following details:

| Field | Value |
|-------|-------|
| **Repository** | `mayurdhage31/IPL_aap_AI_Agents` |
| **Branch** | `main` (or `master` if you used that) |
| **Main file path** | `app_enhanced.py` |
| **App URL** | (optional) Choose a custom subdomain or use auto-generated |

### 5. Add Secrets (IMPORTANT!)

Click on **"Advanced settings"** and then **"Secrets"**

Add the following in the secrets text area:

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-your-actual-api-key-here"
```

**Replace** `sk-ant-api03-your-actual-api-key-here` with your actual Anthropic API key.

### 6. Deploy!

- Click **"Deploy!"** button
- Streamlit Cloud will:
  - Clone your repository
  - Install dependencies from `requirements.txt`
  - Start your application
  - Provide you with a public URL

### 7. Wait for Deployment

- Initial deployment takes 2-5 minutes
- You'll see logs in real-time
- Once complete, your app will be live!

---

## 🔗 Access Your App

After successful deployment, you'll get a URL like:

```
https://your-app-name.streamlit.app
```

Share this URL with anyone - the app is now publicly accessible!

---

## 🔄 Updating Your App

Whenever you make changes to your code:

```bash
# Make your changes to the code
# Then commit and push

git add .
git commit -m "Description of changes"
git push origin main
```

**Streamlit Cloud will automatically redeploy** your app when it detects changes in the GitHub repository!

---

## 🛠️ Troubleshooting

### Issue: "Module not found" errors

**Solution:** Ensure all dependencies are listed in `requirements.txt`

### Issue: "API Key not found"

**Solution:** 
1. Go to your app settings in Streamlit Cloud
2. Click "Secrets" in the left sidebar
3. Verify your `ANTHROPIC_API_KEY` is correctly set
4. Reboot the app

### Issue: Data files not loading

**Solution:** 
- Verify all CSV files in the `data/` folder are pushed to GitHub
- Check file paths in your code are relative, not absolute

### Issue: App crashes on startup

**Solution:**
1. Check the logs in Streamlit Cloud dashboard
2. Look for Python errors
3. Verify all imports are available in `requirements.txt`

---

## 📊 Managing Your App

### View Logs
- Go to [share.streamlit.io](https://share.streamlit.io)
- Click on your app
- View real-time logs and errors

### Reboot App
- Click the "⋮" menu on your app
- Select "Reboot app"

### Delete App
- Click the "⋮" menu on your app
- Select "Delete app"

### Update Secrets
- Click on your app
- Go to "Settings" → "Secrets"
- Edit and save

---

## 🎯 Post-Deployment Checklist

- [ ] App is accessible via public URL
- [ ] All features work correctly
- [ ] AI Agent responds to queries (API key working)
- [ ] All data visualizations load
- [ ] Fantasy analysis generates correctly
- [ ] Betting preview works
- [ ] No errors in Streamlit Cloud logs

---

## 📝 Important Notes

✅ **Free Tier Limits:**
- Streamlit Cloud free tier is suitable for public apps
- Apps sleep after inactivity (wake up on first visit)
- Limited resources (1 GB RAM)

✅ **Security:**
- Never commit `.env` file to GitHub
- Always use Streamlit Cloud secrets for API keys
- The `.gitignore` file protects sensitive data

✅ **Performance:**
- First load may be slow (cold start)
- Subsequent loads are faster
- Consider caching for better performance

---

## 🆘 Support

- **Streamlit Docs:** [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum:** [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues:** Report issues on your repository

---

**Happy Deploying! 🎉**
