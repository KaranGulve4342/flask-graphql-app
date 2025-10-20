# Deployment Guide - Render

## 🚀 Deploy to Render

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:

   **Name:** `flask-graphql-server` (or your choice)
   
   **Environment:** `Docker`
   
   **Region:** Choose closest to your users
   
   **Branch:** `main`
   
   **Instance Type:** `Free` (or paid for production)

### 3. Add Environment Variables

In Render dashboard, add these environment variables:

```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
DEBUG=False
HOST=0.0.0.0
PORT=5000
DB_NAME=graphql
COLLECTION_NAME=users
```

**Important:** Never commit `.env` file with credentials!

### 4. Deploy

Click **"Create Web Service"** and Render will:
- Build the Docker image
- Deploy your application
- Provide a URL like: `https://flask-graphql-server.onrender.com`

### 5. Test Deployment

```bash
curl https://your-app.onrender.com/health
```

## 📝 GraphQL Query Example

```bash
curl -X POST https://your-app.onrender.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { id name age } }"}'
```

## 🔧 Custom Domain (Optional)

1. Go to your service settings
2. Add custom domain
3. Update DNS records

## 📊 Monitoring

- **Logs:** Available in Render dashboard
- **Metrics:** CPU, Memory usage visible
- **Health Check:** Use `/health` endpoint

## 🔄 Auto-Deploy

Render automatically deploys when you push to `main` branch:

```bash
git add .
git commit -m "Update schema"
git push origin main
```

## 💡 Production Tips

1. **Use Paid Instance:** Free tier sleeps after inactivity
2. **Enable Health Checks:** Render → Settings → Health Check Path: `/health`
3. **Set Auto-Deploy:** Enable in settings for CI/CD
4. **Monitor Logs:** Check for errors regularly
5. **Database Backups:** Enable MongoDB backups

## 🐳 Local Docker Testing

```bash
# Build image
docker build -t flask-graphql-app .

# Run container
docker run -p 5000:5000 --env-file .env flask-graphql-app

# Test
curl http://localhost:5000/health
```

## 🚨 Troubleshooting

**Issue:** Application not starting
- Check logs in Render dashboard
- Verify environment variables are set
- Ensure MongoDB connection string is correct

**Issue:** Port binding error
- Render uses PORT env variable automatically
- Don't hardcode port in application

**Issue:** Slow cold starts (Free tier)
- Free instances sleep after 15 minutes
- First request takes ~30 seconds to wake
- Use paid tier for production
