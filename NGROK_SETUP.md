# Ngrok Setup Guide

Ngrok allows you to create a **public URL** that students can access from anywhere (not just your local network). This is essential for sharing quizzes with students who are not on the same WiFi network.

## Why Ngrok?

Without ngrok:
- Only accessible on `http://127.0.0.1:5000` (your computer only)
- Students must be on the same network

With ngrok:
- Get a public URL like `https://abc123.ngrok.io`
- Students can access from anywhere in the world
- Works on any device (phone, tablet, computer)

## Step-by-Step Setup

### 1. Create Free Ngrok Account

1. Go to https://dashboard.ngrok.com/signup
2. Sign up with email (free account)
3. Verify your email

### 2. Get Your Auth Token

1. Log into https://dashboard.ngrok.com/
2. Go to: **Your Authtoken** section
   - Direct link: https://dashboard.ngrok.com/get-started/your-authtoken
3. Copy your authtoken (looks like: `2abc123def456ghi789jkl012mno345pq`)

### 3. Set Environment Variable

#### Windows PowerShell (Temporary - This Session Only):
```powershell
$env:NGROK_AUTH_TOKEN = "your_authtoken_here"
```

#### Windows PowerShell (Permanent - All Sessions):
```powershell
[System.Environment]::SetEnvironmentVariable('NGROK_AUTH_TOKEN', 'your_authtoken_here', 'User')
```

Then restart your terminal/PowerShell.

#### Windows CMD (Temporary):
```cmd
set NGROK_AUTH_TOKEN=your_authtoken_here
```

#### Windows CMD (Permanent):
```cmd
setx NGROK_AUTH_TOKEN "your_authtoken_here"
```

Then close and reopen CMD.

### 4. Verify Setup

Check if the token is set:
```powershell
# PowerShell
echo $env:NGROK_AUTH_TOKEN

# CMD
echo %NGROK_AUTH_TOKEN%
```

You should see your token printed.

## How It Works

### When You Launch a Quiz:

1. **Click "Launch Quiz"** in the GUI
2. **Server starts** on `http://127.0.0.1:5000`
3. **Ngrok creates tunnel** → Public URL like `https://abc123.ngrok.io`
4. **Dialog shows** the public URL
5. **Share the URL** with students!

### Example Flow:

```
You: Click "Launch Quiz"
    ↓
Flask Server: Starts on http://127.0.0.1:5000
    ↓
Ngrok: Creates tunnel → https://xyz789.ngrok.io → http://127.0.0.1:5000
    ↓
Dialog: "Public URL: https://xyz789.ngrok.io"
    ↓
You: Share https://xyz789.ngrok.io with students
    ↓
Students: Open link on any device, anywhere
    ↓
All traffic → Ngrok → Your local server → Quiz interface
```

## Free Tier Limitations

**Without Auth Token:**
- ❌ Won't work (authentication required)
- ❌ 2-hour limit
- ❌ Random URLs each time

**With Free Account + Auth Token:**
- ✅ Unlimited tunnels
- ✅ URLs stay same (until server restarts)
- ✅ Basic features

**Paid Tier:**
- Custom domains (e.g., `quiz.yourschool.com`)
- Reserved URLs
- More features

## Troubleshooting

### "authentication failed" Error

**Problem**: Ngrok auth token not set or invalid

**Solution**:
1. Verify token is set: `echo $env:NGROK_AUTH_TOKEN` (PowerShell)
2. Re-set the token using methods above
3. Restart your terminal/PowerShell
4. Try launching quiz again

### "ngrok process errored"

**Problem**: Token might be expired or incorrect

**Solution**:
1. Log into ngrok dashboard
2. Generate a new authtoken
3. Update your environment variable
4. Restart terminal

### Server Works Locally But Ngrok Fails

**Good News**: The server still runs! Just locally.

**Options**:
1. **Fix ngrok** (recommended) - Follow steps above
2. **Use local network** - Students on same WiFi can access via your local IP:
   - Find your IP: `ipconfig` (Windows) → Look for IPv4 Address
   - Share: `http://YOUR_IP:5000` (e.g., `http://192.168.1.100:5000`)

## Alternative: Local Network Access

If ngrok is too complicated, you can share locally:

1. **Find your local IP address**:
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., `192.168.1.100`)

2. **Update Flask to accept external connections**:
   - Edit `run_server.py`
   - Change `host='127.0.0.1'` to `host='0.0.0.0'`
   - **Warning**: Less secure, only use on trusted networks

3. **Share**: `http://YOUR_IP:5000` with students on same WiFi

## Quick Start Checklist

- [ ] Created ngrok account at https://dashboard.ngrok.com/signup
- [ ] Got authtoken from dashboard
- [ ] Set `NGROK_AUTH_TOKEN` environment variable
- [ ] Verified with `echo $env:NGROK_AUTH_TOKEN`
- [ ] Launched quiz in GUI
- [ ] Copied public URL from dialog
- [ ] Shared URL with students
- [ ] Students can access quiz!

## Example Workflow

```
1. You: "I'll share a quiz link in 2 minutes"
2. Open Quiz Builder GUI
3. Load/Create quiz
4. Click "Launch Quiz"
5. Wait 3 seconds
6. Dialog appears: "Public URL: https://abc123.ngrok.io"
7. Copy URL
8. Share in chat/email: "Here's the quiz: https://abc123.ngrok.io"
9. Students click link → Quiz opens in browser
10. Students take quiz
11. Results saved automatically on your computer
```

## Security Note

⚠️ **Public URLs are accessible to anyone with the link**

- Don't share sensitive information
- Quiz URLs are temporary (change each launch)
- Results are stored locally on YOUR computer only
- No personal data is sent to ngrok

---

**Need Help?** Check the main README.md or review the ngrok documentation: https://ngrok.com/docs

