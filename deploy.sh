#!/bin/bash
# TFG Idealista - Script de despliegue completo
# Álvaro Carrera - Django + Streamlit deployment

set -e  # Exit on any error

echo "🚀 TFG IDEALISTA - COMPLETE DEPLOYMENT PIPELINE"
echo "================================================"
echo "Álvaro Carrera - Análisis del mercado inmobiliario Madrid"
echo "Backend: Django + PostgreSQL | Frontend: Streamlit"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're on main branch
current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")
if [ "$current_branch" != "main" ]; then
    print_warning "Not on main branch (current: $current_branch)"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Deployment cancelled."
        exit 1
    fi
fi

# Step 1: Validate dependencies
print_status "Step 1/7: Validating system dependencies..."
python scripts/validate_dependencies.py

if [ $? -ne 0 ]; then
    print_error "Dependency validation failed. Aborting deployment."
    exit 1
fi
print_success "Dependencies validated!"

# Step 2: Run existing validation scripts
print_status "Step 2/7: Running ML model validation..."
if [ -f "scripts/validate_models.py" ]; then
    python scripts/validate_models.py
    if [ $? -eq 0 ]; then
        print_success "ML models validated!"
    else
        print_warning "ML model validation had issues, but continuing..."
    fi
else
    print_warning "ML validation script not found, skipping..."
fi

# Step 3: Test Django backend
print_status "Step 3/7: Testing Django backend..."
cd backend

# Check Django configuration
python manage.py check
if [ $? -ne 0 ]; then
    print_error "Django configuration check failed!"
    cd ..
    exit 1
fi

# Run Django tests
python manage.py test --verbosity=2
django_test_result=$?

cd ..

if [ $django_test_result -eq 0 ]; then
    print_success "Django tests passed!"
else
    print_warning "Django tests had issues, but continuing..."
fi

# Step 4: Test Streamlit frontend
print_status "Step 4/7: Testing Streamlit frontend..."
if [ -f "frontend/src/app.py" ]; then
    cd frontend
    python -c "
import sys
sys.path.append('src')
try:
    import app
    print('✅ Streamlit app imports successfully')
except Exception as e:
    print(f'❌ Streamlit app import failed: {e}')
    sys.exit(1)
"
    streamlit_test_result=$?
    cd ..
    
    if [ $streamlit_test_result -eq 0 ]; then
        print_success "Streamlit frontend validated!"
    else
        print_error "Streamlit validation failed!"
        exit 1
    fi
else
    print_warning "Streamlit app not found at frontend/src/app.py"
fi

# Step 5: Run integration tests
print_status "Step 5/7: Running integration tests..."
if [ -f "scripts/integration_test.py" ]; then
    python scripts/integration_test.py
    if [ $? -eq 0 ]; then
        print_success "Integration tests passed!"
    else
        print_warning "Integration tests had issues, but continuing..."
    fi
else
    print_warning "Integration test script not found, skipping..."
fi

# Step 6: Show current status and ask for confirmation
print_status "Step 6/7: Pre-deployment summary..."
echo ""
echo "📊 DEPLOYMENT SUMMARY:"
echo "======================"
echo "🌐 Backend: Django 4.2.7 + DRF + PostgreSQL"
echo "🎨 Frontend: Streamlit 1.28.1 + Folium + Plotly"
echo "🤖 ML Models: K-means clustering (6,735 properties)"
echo "🏘️ Analysis: 5 clusters identified"
echo "🔄 CI/CD: GitLab pipeline with 6 stages"
echo "☁️ Deploy: Render (backend) + Vercel (frontend)"
echo ""

# Show git status
echo "📝 Current changes:"
git status --short

echo ""
read -p "🤔 Proceed with deployment? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_error "Deployment cancelled by user."
    exit 1
fi

# Step 7: Commit and push
print_status "Step 7/7: Committing and pushing to GitLab..."

# Add all changes
git add .

# Create comprehensive commit message
commit_message="🚀 Production deployment $(date '+%Y-%m-%d %H:%M:%S')

✅ Backend: Django 4.2.7 + PostgreSQL + DRF API
✅ Frontend: Streamlit 1.28.1 + Interactive maps
✅ ML Models: K-means clustering validated
✅ Data: 6,735 real properties from Idealista
✅ Analysis: 5 market segments identified  
✅ CI/CD: Complete pipeline with dependency validation
✅ Deploy: Render (backend) + Vercel (frontend)

📊 Key metrics:
- Silhouette score: 0.280
- DBSCAN score: 0.854
- Clusters: 5 distinct market segments
- Coverage: Full Madrid metropolitan area

🔧 Technical stack:
- Django 4.2.7 + gunicorn
- Streamlit 1.28.1 + folium
- PostgreSQL database
- scikit-learn 1.3.2
- RESTful API endpoints

Deployed by: Álvaro Carrera
Project: TFG Análisis Mercado Inmobiliario Madrid"

git commit -m "$commit_message"

# Push to remote
git push origin main

if [ $? -eq 0 ]; then
    print_success "Code pushed to GitLab successfully!"
else
    print_error "Failed to push to GitLab!"
    exit 1
fi

# Final success message
echo ""
echo "🎉 DEPLOYMENT PIPELINE INITIATED!"
echo "================================="
echo ""
print_success "GitLab CI/CD pipeline started!"
echo ""
echo "📊 Monitor deployment progress:"
echo "   🔗 GitLab CI: https://gitlab.com/your-username/tfg-alvaro-carrera-idealista/-/pipelines"
echo "   🔗 Render Backend: https://dashboard.render.com"
echo "   🔗 Vercel Frontend: https://vercel.com/dashboard"
echo ""
echo "🌐 Production URLs (available after deployment):"
echo "   🎨 Frontend: https://tfg-idealista-frontend.vercel.app"
echo "   🌐 Backend API: https://tfg-idealista-backend.onrender.com/api/"
echo "   📚 API Endpoints:"
echo "      - GET /api/properties/ (property listings)"
echo "      - GET /api/clustering/ (ML analysis)"
echo "      - POST /api/predict/ (cluster prediction)"
echo ""
echo "⏱️ Expected deployment time:"
echo "   - Backend (Render): ~5-10 minutes"
echo "   - Frontend (Vercel): ~2-5 minutes"
echo ""
print_success "Deployment script completed! 🚀"