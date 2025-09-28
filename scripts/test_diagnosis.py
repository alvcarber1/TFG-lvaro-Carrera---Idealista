#!/usr/bin/env python3
"""
Script de diagnóstico para verificar el entorno antes de ejecutar tests
"""

import sys
import os
import importlib
from pathlib import Path

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python version should be 3.8+")
        return False

def check_dependencies():
    """Verificar dependencias críticas"""
    critical_deps = {
        'pandas': 'Data manipulation',
        'numpy': 'Numerical computing',
        'pytest': 'Testing framework',
        'sklearn': 'Machine learning (as scikit-learn)',
        'pathlib': 'Path handling'
    }
    
    optional_deps = {
        'matplotlib': 'Plotting',
        'seaborn': 'Statistical visualization',
        'folium': 'Map visualization',
        'joblib': 'Model serialization'
    }
    
    print("\n📦 Checking critical dependencies...")
    missing_critical = []
    
    for dep, description in critical_deps.items():
        try:
            if dep == 'sklearn':
                module = importlib.import_module('sklearn')
            else:
                module = importlib.import_module(dep)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {dep}: {version} ({description})")
        except ImportError:
            print(f"❌ {dep}: NOT FOUND ({description})")
            missing_critical.append(dep)
    
    print("\n📦 Checking optional dependencies...")
    missing_optional = []
    
    for dep, description in optional_deps.items():
        try:
            module = importlib.import_module(dep)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {dep}: {version} ({description})")
        except ImportError:
            print(f"⚠️ {dep}: NOT FOUND ({description}) - optional")
            missing_optional.append(dep)
    
    return len(missing_critical) == 0, missing_critical, missing_optional

def check_file_structure():
    """Verificar estructura de archivos"""
    print("\n📁 Checking file structure...")
    
    required_structure = {
        'tests/': 'Tests directory',
        'scripts/': 'Scripts directory',
        'requirements.txt': 'Dependencies file',
        '.gitlab-ci.yml': 'GitLab CI configuration'
    }
    
    optional_structure = {
        'backend/': 'Backend code',
        'frontend/': 'Frontend code',
        'backend/data/': 'Data directory',
        'backend/notebooks/': 'Jupyter notebooks'
    }
    
    missing_required = []
    
    print("Required files/directories:")
    for path, description in required_structure.items():
        if Path(path).exists():
            print(f"✅ {path} ({description})")
        else:
            print(f"❌ {path} ({description})")
            missing_required.append(path)
    
    print("\nOptional files/directories:")
    for path, description in optional_structure.items():
        if Path(path).exists():
            print(f"✅ {path} ({description})")
        else:
            print(f"⚠️ {path} ({description}) - optional")
    
    return len(missing_required) == 0, missing_required

def check_test_files():
    """Verificar archivos de test específicos"""
    print("\n🧪 Checking test files...")
    
    expected_tests = {
        'tests/test_clustering.py': 'Clustering analysis tests',
        'tests/test_data_processing.py': 'Data processing tests',
        'tests/test_backend_api.py': 'Backend API tests',
        'tests/test_model_simple.py': 'Simple model tests'
    }
    
    missing_tests = []
    
    for test_file, description in expected_tests.items():
        if Path(test_file).exists():
            print(f"✅ {test_file} ({description})")
        else:
            print(f"❌ {test_file} ({description})")
            missing_tests.append(test_file)
    
    return len(missing_tests) == 0, missing_tests

def check_script_files():
    """Verificar archivos de scripts"""
    print("\n📜 Checking script files...")
    
    expected_scripts = {
        'scripts/validate_models.py': 'Model validation script',
        'scripts/integration_test.py': 'Integration test script',
        'scripts/get_districts_neighborhoods.py': 'Districts/neighborhoods script'
    }
    
    missing_scripts = []
    
    for script_file, description in expected_scripts.items():
        if Path(script_file).exists():
            print(f"✅ {script_file} ({description})")
        else:
            print(f"❌ {script_file} ({description})")
            missing_scripts.append(script_file)
    
    return len(missing_scripts) == 0, missing_scripts

def test_basic_imports():
    """Probar imports básicos que usan los tests"""
    print("\n🔬 Testing critical imports...")
    
    test_imports = [
        ('import pandas as pd', 'pandas'),
        ('import numpy as np', 'numpy'),
        ('import pytest', 'pytest'),
        ('from pathlib import Path', 'pathlib'),
        ('import sys, os', 'system modules'),
    ]
    
    optional_imports = [
        ('from sklearn.cluster import KMeans', 'sklearn.cluster'),
        ('from sklearn.preprocessing import StandardScaler', 'sklearn.preprocessing'),
        ('from sklearn.metrics import silhouette_score', 'sklearn.metrics'),
        ('import joblib', 'joblib'),
    ]
    
    failed_critical = []
    failed_optional = []
    
    print("Critical imports:")
    for import_statement, lib_name in test_imports:
        try:
            exec(import_statement)
            print(f"✅ {lib_name}")
        except Exception as e:
            print(f"❌ {lib_name}: {e}")
            failed_critical.append(lib_name)
    
    print("\nOptional imports:")
    for import_statement, lib_name in optional_imports:
        try:
            exec(import_statement)
            print(f"✅ {lib_name}")
        except Exception as e:
            print(f"⚠️ {lib_name}: {e}")
            failed_optional.append(lib_name)
    
    return len(failed_critical) == 0, failed_critical, failed_optional

def main():
    """Función principal de diagnóstico"""
    print("="*70)
    print("🔍 PRE-TEST DIAGNOSTIC REPORT")
    print("="*70)
    
    # Ejecutar todos los checks
    python_ok = check_python_version()
    deps_ok, missing_critical, missing_optional = check_dependencies()
    structure_ok, missing_required = check_file_structure()
    tests_ok, missing_tests = check_test_files()
    scripts_ok, missing_scripts = check_script_files()
    imports_ok, failed_critical, failed_optional = test_basic_imports()
    
    # Resumen
    print("\n" + "="*70)
    print("📊 DIAGNOSTIC SUMMARY")
    print("="*70)
    
    checks = [
        ("Python Version", python_ok),
        ("Critical Dependencies", deps_ok),
        ("File Structure", structure_ok),
        ("Test Files", tests_ok),
        ("Script Files", scripts_ok),
        ("Critical Imports", imports_ok),
    ]
    
    passed = 0
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:25} | {status}")
        if result:
            passed += 1
    
    total = len(checks)
    print("-" * 70)
    print(f"{'TOTAL':25} | {passed}/{total} checks passed")
    
    # Recomendaciones
    print("\n" + "="*70)
    print("💡 RECOMMENDATIONS")
    print("="*70)
    
    if passed == total:
        print("🎉 Environment is ready for testing!")
        print("\n🚀 Next steps:")
        print("1. Run individual tests: python -m pytest tests/test_data_processing.py -v")
        print("2. Run all tests: python -m pytest tests/ -v")
        print("3. Run with coverage: python -m pytest tests/ --cov=. -v")
    else:
        print("🛠️ Issues found. Please address them:")
        
        if missing_critical:
            print(f"\n📦 Install missing dependencies:")
            print(f"   pip install {' '.join(missing_critical)}")
        
        if missing_required:
            print(f"\n📁 Create missing files/directories:")
            for item in missing_required:
                print(f"   - {item}")
        
        if failed_critical:
            print(f"\n🔬 Fix import issues:")
            for item in failed_critical:
                print(f"   - {item}")
    
    if missing_optional:
        print(f"\n⚠️ Optional dependencies missing (tests may be limited):")
        for dep in missing_optional:
            print(f"   - {dep}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)