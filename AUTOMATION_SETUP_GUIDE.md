# PlayStation Store Crawler - Daily Automation Setup Guide

## Overview
This guide will help you set up daily automatic runs of your PlayStation Store crawler at 9:00 AM every day, with email notifications on success/failure.

## Step 1: Setup Gmail App Password (REQUIRED)

Since you're using Gmail, you need to create an "App Password" for the crawler to send emails:

### 1.1 Enable 2-Step Verification (if not already enabled)
1. Go to your Google Account: https://myaccount.google.com/
2. Click "Security" on the left sidebar
3. Under "Signing in to Google", click "2-Step Verification"
4. Follow the prompts to enable it (you'll need your phone)

### 1.2 Generate App Password
1. Go back to Security settings: https://myaccount.google.com/security
2. Under "Signing in to Google", click "App passwords"
3. Select "Mail" from the dropdown
4. Select "Windows Computer" (or "Other" and type "PlayStation Crawler")
5. Click "Generate"
6. **COPY THE 16-CHARACTER PASSWORD** (it looks like: abcd efgh ijkl mnop)

## Step 2: Configure Email Settings

1. Open `config.py` in your crawler folder
2. Find the `EMAIL_CONFIG` section (at the bottom)
3. Replace the empty `'sender_password': ''` with your App Password:
   ```python
   'sender_password': 'abcd efgh ijkl mnop',  # Use your actual 16-character App Password
   ```
4. Save the file

## Step 3: Test Email Functionality (IMPORTANT)

Before setting up automation, let's test if email works:

1. Open Command Prompt
2. Navigate to your crawler folder:
   ```
   cd "C:\Users\user\Desktop\TX\PS Store Crawler"
   ```
3. Run a quick test:
   ```
   python -c "from main_crawler import PlayStationCrawler; c = PlayStationCrawler(); c.send_email_notification(True, 'Test email - setup working!')"
   ```
4. Check your email (zhanghan415@gmail.com) - you should receive a success notification

If you get an error, double-check your App Password in config.py.

## Step 4: Setup Windows Task Scheduler

### 4.1 Open Task Scheduler
1. Press `Windows + R`
2. Type `taskschd.msc` and press Enter
3. Task Scheduler will open

### 4.2 Create New Task
1. Click "Create Basic Task..." in the right panel
2. Name: `PlayStation Store Daily Crawler`
3. Description: `Automatically runs PlayStation Store crawler every morning at 9 AM`
4. Click "Next"

### 4.3 Set Trigger (When to run)
1. Select "Daily"
2. Click "Next"
3. Set Start date to tomorrow's date
4. Set Start time to `9:00:00 AM`
5. Set "Recur every: 1 days"
6. Click "Next"

### 4.4 Set Action (What to run)
1. Select "Start a program"
2. Click "Next"
3. In "Program/script" field, click "Browse"
4. Navigate to your crawler folder and select `run_daily_crawler.bat`
5. In "Start in" field, enter your crawler folder path:
   ```
   C:\Users\user\Desktop\TX\PS Store Crawler
   ```
6. Click "Next"

### 4.5 Review and Finish
1. Review all settings
2. Check "Open the Properties dialog for this task when I click Finish"
3. Click "Finish"

### 4.6 Configure Advanced Settings
1. In the Properties dialog that opens:
2. Go to "General" tab:
   - Check "Run whether user is logged on or not"
   - Check "Run with highest privileges"
3. Go to "Settings" tab:
   - Check "Allow task to be run on demand"
   - Check "Run task as soon as possible after a scheduled start is missed"
   - Under "If the task fails, restart every:", set to "10 minutes" and "Attempt to restart up to: 2 times"
4. Click "OK"
5. You may be prompted for your Windows password - enter it

## Step 5: Test the Automation

### 5.1 Manual Test
1. In Task Scheduler, find your task in the task list
2. Right-click on "PlayStation Store Daily Crawler"
3. Click "Run"
4. The task should execute immediately
5. Check your email for a notification

### 5.2 Check Task History
1. In Task Scheduler, click on your task
2. Click "History" tab at the bottom
3. You should see entries showing the task started and completed

## Step 6: Monitor and Troubleshoot

### Daily Monitoring
- You'll receive an email every morning after the crawler runs
- SUCCESS emails mean everything worked
- FAILURE emails mean something went wrong

### Log Files
- Check `crawler.log` in your folder for detailed information
- This file will show you exactly what happened during each run

### Common Issues
1. **No email received**: Check your App Password in config.py
2. **Task doesn't run**: Make sure your computer is on at 9 AM
3. **Python errors**: Check that all your Python packages are still installed

## Step 7: Future Maintenance

### If you restart your computer
- The scheduled task will continue working automatically
- No additional setup needed

### If you change your Gmail password
- You'll need to generate a new App Password and update config.py

### If you move the crawler folder
- Update the Task Scheduler paths in the task properties

## Congratulations! 🎉

Your PlayStation Store crawler will now run automatically every morning at 9:00 AM and send you email notifications. You don't need to manually run it anymore!

---

**Need Help?**
If you encounter any issues, check the `crawler.log` file and your email notifications for clues about what went wrong. 