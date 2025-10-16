# 🗄️ Populate Render Database Guide

## 🎯 Problem: Empty Database on Render

Your local database has scraped data, but your Render database is empty. Here are 3 solutions:

## 🚀 Solution 1: Use Scraping Button (Easiest)

### Steps:
1. **Go to your Render dashboard**: `https://leadtool.onrender.com`
2. **Look at the left sidebar** - you should see "🕷️ Scraping Controls"
3. **Click "🚀 Run Scraper"** button
4. **Wait for completion** - you'll see a spinner and success message
5. **Dashboard refreshes** - data should appear

### What happens:
- ✅ Scraper runs on Render
- ✅ Data gets stored in Render's PostgreSQL database
- ✅ Dashboard shows the scraped data
- ✅ No need to transfer files

## 📤 Solution 2: Export/Import Data

### Step 1: Export from Local
```bash
# Run this on your local machine
python export_local_data.py
```

This creates a file like `leadtool_export_20241016_143022.json`

### Step 2: Upload to Render
1. **Go to your Render dashboard**
2. **Upload the JSON file** (if you have file upload capability)
3. **Or use the import script** on Render

### Step 3: Import to Render Database
```bash
# Run this on Render (if you have access)
python import_to_render.py
```

## 🔧 Solution 3: Manual Database Setup

### Option A: Use Render Database Tools
1. **Go to your Render dashboard**
2. **Find your PostgreSQL service**
3. **Click "Connect" or "Open in Browser"**
4. **Use the database interface** to manually add data

### Option B: Use Database Client
1. **Get your database connection string** from Render
2. **Use a tool like pgAdmin or DBeaver**
3. **Connect to your Render database**
4. **Import your local data**

## 🎯 Recommended Approach

**Use Solution 1 (Scraping Button)** because:
- ✅ **Easiest** - Just click a button
- ✅ **No file transfers** - Everything happens on Render
- ✅ **Fresh data** - Gets latest data from Google Maps
- ✅ **Automatic** - No manual steps

## 🔍 Troubleshooting

### If Scraping Button Doesn't Work:

1. **Check Render logs** for errors
2. **Verify database connection** - Check DATABASE_URL
3. **Check dependencies** - Make sure all packages are installed
4. **Try manual scraping** - Run `python run.py scraper` in Render console

### If No Data Shows:

1. **Check database connection** - Look for connection errors
2. **Verify data was scraped** - Check if scraping actually ran
3. **Check database tables** - Make sure data was stored
4. **Refresh dashboard** - Try reloading the page

## 📊 Expected Result

After successful data population, you should see:
- ✅ **Companies table** with business data
- ✅ **Monthly data** with scraping history
- ✅ **Charts and metrics** showing statistics
- ✅ **Scraping button** working properly

## 🎉 Success Indicators

You'll know it's working when:
- ✅ **Dashboard shows data** instead of "No data found"
- ✅ **Metrics show numbers** instead of 0
- ✅ **Tables display businesses** with names, addresses, etc.
- ✅ **Charts render** with actual data

## 🆘 Still Having Issues?

### Check These:
1. **Database connection** - Is DATABASE_URL set correctly?
2. **Scraping logs** - Did the scraper actually run?
3. **Database tables** - Are the tables created?
4. **Data format** - Is the data in the right format?

### Get Help:
1. **Check Render logs** for error messages
2. **Test database connection** locally first
3. **Verify all dependencies** are installed
4. **Check the scraping configuration** in `config/sites.yaml`

Your LeadTool should now show data on Render! 🚀
