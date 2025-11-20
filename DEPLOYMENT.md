# 🚀 DoseSafe-AI Deployment Guide

## 📋 Quick Start (Recommended for Demo)

### Option 1: Local Production Deployment
```bash
# Windows
deploy.bat

# Linux/Mac
chmod +x deploy.sh
./deploy.sh

# Then start the system
python start_production.py
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r backend/requirements.txt
cd frontend && npm install

# 2. Train ML models
cd ml_models && python comprehensive_trainer_fixed.py

# 3. Set environment variables
cp .env.example .env
# Edit .env with your API keys

# 4. Start backend
cd backend && python app.py

# 5. Start frontend (new terminal)
cd frontend && npm start
```

## 🌐 Deployment Options

### 1. **Local Development** (Current Setup)
- **Use Case**: Development and testing
- **Requirements**: Python 3.13, Node.js, Tesseract
- **Command**: `python backend/app.py` + `npm start`
- **Access**: http://localhost:5000 (backend), http://localhost:3000 (frontend)

### 2. **Local Production**
- **Use Case**: Demo presentations, local deployment
- **Setup**: Run `deploy.bat` or `deploy.sh`
- **Command**: `python start_production.py`
- **Access**: http://localhost:5000

### 3. **Docker Deployment**
```bash
# Build and run with Docker
docker build -t dosesafe-ai .
docker run -p 5000:5000 -p 3000:3000 dosesafe-ai

# Or use Docker Compose
docker-compose up -d
```

### 4. **Heroku Cloud Deployment**
```bash
# Install Heroku CLI
heroku create your-dosesafe-app

# Set environment variables
heroku config:set GROQ_API_KEY=your_api_key

# Deploy
git push heroku main

# Open app
heroku open
```

### 5. **AWS/Azure/GCP Deployment**
- Use Docker container with cloud container services
- Configure load balancer for high availability
- Set up auto-scaling for traffic spikes
- Use managed databases for production data

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
FLASK_ENV=production
DEBUG=False
HOST=0.0.0.0
PORT=5000
```

### System Requirements
- **CPU**: 2+ cores (4+ recommended)
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB free space
- **OS**: Windows 10+, Ubuntu 18+, macOS 10.15+

## 🛡️ Security Considerations

### Production Security
- [ ] Change default secret keys
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable request logging
- [ ] Secure API keys
- [ ] Validate file uploads
- [ ] Enable CORS properly

### Healthcare Compliance
- [ ] HIPAA compliance review
- [ ] Data encryption at rest
- [ ] Audit logging
- [ ] Access controls
- [ ] Regular security updates

## 📊 Monitoring & Maintenance

### Health Checks
- **Backend**: http://localhost:5000/ai-capabilities
- **ML Models**: Check model loading logs
- **OCR**: Test with sample prescription
- **Database**: Verify interaction history

### Performance Monitoring
```python
# Add to backend for monitoring
import time
import psutil

@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': time.time(),
        'memory_usage': psutil.virtual_memory().percent,
        'cpu_usage': psutil.cpu_percent()
    }
```

## 🔄 Updates & Maintenance

### Regular Updates
1. **ML Models**: Retrain monthly with new data
2. **Dependencies**: Update packages quarterly
3. **Security**: Apply patches immediately
4. **Database**: Backup interaction history

### Scaling Considerations
- **Horizontal**: Deploy multiple instances
- **Vertical**: Increase server resources
- **Caching**: Add Redis for frequent requests
- **CDN**: Serve static files efficiently

## 🆘 Troubleshooting

### Common Issues
1. **Tesseract not found**: Install OCR engine
2. **ML models missing**: Run trainer script
3. **API key invalid**: Check environment variables
4. **Port conflicts**: Change ports in configuration
5. **Memory issues**: Increase system RAM

### Debug Commands
```bash
# Check Python environment
python --version
pip list

# Check Node.js environment
node --version
npm list

# Check Tesseract
tesseract --version

# Test ML models
python -c "from ml_models.ml_integration import get_ml_status; print(get_ml_status())"
```

## 🎯 Production Checklist

### Before Go-Live
- [ ] All dependencies installed
- [ ] ML models trained and tested
- [ ] Environment variables configured
- [ ] Security measures implemented
- [ ] Performance testing completed
- [ ] Backup procedures established
- [ ] Monitoring systems active
- [ ] Documentation updated

### Post-Deployment
- [ ] System health verified
- [ ] Performance metrics baseline
- [ ] User access testing
- [ ] Backup verification
- [ ] Incident response plan ready

## 📞 Support & Resources

### Documentation
- **API Docs**: http://localhost:5000/ai-capabilities
- **System Metrics**: http://localhost:5000/system-metrics
- **ML Status**: Check console logs

### For Issues
1. Check deployment logs
2. Verify environment configuration
3. Test individual components
4. Review error messages
5. Consult troubleshooting guide

---

**🎉 Your DoseSafe-AI system is now ready for deployment!**
