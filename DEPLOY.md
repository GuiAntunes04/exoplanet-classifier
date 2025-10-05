# 🚀 Deployment Guide - Exoplanet Classifier

This guide explains how to deploy the application on different platforms.

## 📋 Prerequisites

- Python 3.9+
- GitHub account
- Account on the chosen deployment platform

## 🌐 Deploy on Streamlit Cloud (Recommended)

### 1. Prepare Repository
```bash
# Make sure all files are committed
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Login with your GitHub account
3. Click "New app"
4. Configure:
   - **Repository**: your-username/exoplanet-classifier
   - **Branch**: main
   - **Main file path**: app.py
   - **App URL**: exoplanet-classifier (or your preferred name)

### 3. Advanced Settings
- **Python version**: 3.9
- **Requirements file**: requirements.txt
- **Secrets**: Not necessary for this application

## 🐳 Deploy with Docker

### 1. Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. Build and Run
```bash
docker build -t exoplanet-classifier .
docker run -p 8501:8501 exoplanet-classifier
```

## ☁️ Deploy on Heroku

### 1. Create Procfile
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### 2. Deploy
```bash
heroku create exoplanet-classifier
git push heroku main
```

## 🔧 Local Deploy

### 1. Installation
```bash
git clone https://github.com/your-username/exoplanet-classifier.git
cd exoplanet-classifier
pip install -r requirements.txt
```

### 2. Execution
```bash
streamlit run app.py
```

## 📊 Monitoring

### Logs
- **Streamlit Cloud**: Automatic logs in interface
- **Docker**: `docker logs <container_id>`
- **Heroku**: `heroku logs --tail`

### Performance
- Monitor CPU and memory usage
- Configure downtime alerts
- Use tools like New Relic or DataDog

## 🔒 Security

### Recommendations
- Use HTTPS in production
- Configure CORS properly
- Monitor suspicious access attempts
- Keep dependencies updated

### Environment Variables
```bash
# For sensitive configurations
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_PORT=8501
```

## 🚨 Troubleshooting

### Common Issues

#### Dependency Error
```bash
# Update requirements.txt
pip freeze > requirements.txt
```

#### Port Error
```bash
# Check if port is in use
netstat -tulpn | grep :8501
```

#### Memory Error
- Reduce size of processed data
- Use cache for heavy operations
- Configure memory limits

### Debug Logs
```python
# Add to app.py for debug
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Optimizations

### Performance
- Use `@st.cache_data` for heavy operations
- Implement lazy loading
- Optimize data queries

### UX
- Add loading spinners
- Implement input validation
- Use visual feedback

## 🔄 CI/CD

### GitHub Actions
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Streamlit
        # Configure automatic deployment
```

## 📞 Support

For deployment issues:
1. Check application logs
2. Consult platform documentation
3. Open an issue on GitHub
4. Contact support

---

**Deployment completed successfully! 🎉**
