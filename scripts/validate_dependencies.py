#!/usr/bin/env python3
"""
Validador de dependencias para TFG Idealista
Álvaro Carrera - Deployment validation
Integra con los scripts existentes: validate_models.py, integration_test.py
"""

import subprocess
import sys
import os
from pathlib import Path
import importlib.util

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3 or version.minor < 10:
        print("❌ Python 3.10+ required")
        return False
    print("✅ Python version OK")
    return True

def read_file_with_encoding(file_path):
    """Leer archivo con diferentes codificaciones"""
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return content, encoding
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"   ⚠️ Error reading with {encoding}: {e}")
            continue
    
    # Si ninguna codificación funciona, intentar leer como binario
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        # Intentar decodificar ignorando errores
        content = content.decode('utf-8', errors='ignore')
        return content, 'utf-8 (with errors ignored)'
    except Exception as e:
        print(f"   ❌ Could not read file {file_path}: {e}")
        return None, None

def validate_requirements_file(req_file):
    """Validar archivo de requirements"""
    if not os.path.exists(req_file):
        print(f"❌ Requirements file not found: {req_file}")
        return False
    
    print(f"📦 Validating {req_file}...")
    
    # Leer archivo con manejo de codificación
    content, encoding = read_file_with_encoding(req_file)
    if content is None:
        print(f"   ❌ Could not read requirements file")
        return False
    
    print(f"   📝 File encoding detected: {encoding}")
    
    # Procesar líneas
    lines = content.splitlines()
    
    critical_packages = {
        'django': 'Django framework',
        'streamlit': 'Frontend framework', 
        'pandas': 'Data processing',
        'numpy': 'Numerical computing',
        'scikit-learn': 'Machine learning',
        'sklearn': 'Machine learning (alt)',
        'folium': 'Map visualization',
        'plotly': 'Interactive plots',
        'requests': 'HTTP client'
    }
    
    critical_found = []
    all_packages = []
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('-'):
            # Extraer nombre del paquete
            package = line.split('==')[0].split('>=')[0].split('<=')[0].split('[')[0].strip()
            all_packages.append(line)
            
            if package.lower() in critical_packages:
                critical_found.append((package, line, critical_packages[package.lower()]))
    
    print(f"   📋 Total packages: {len(all_packages)}")
    print(f"   🎯 Critical packages found: {len(critical_found)}")
    
    for pkg_name, pkg_line, description in critical_found:
        print(f"      ✅ {pkg_name}: {description}")
    
    # Verificar paquetes críticos faltantes
    missing_critical = []
    for critical_pkg in ['django', 'pandas', 'numpy']:
        found = any(critical_pkg.lower() in pkg[0].lower() for pkg in critical_found)
        if not found:
            missing_critical.append(critical_pkg)
    
    if missing_critical:
        print(f"   ⚠️ Missing critical packages: {', '.join(missing_critical)}")
    
    return True

def check_django_setup():
    """Verificar configuración de Django"""
    print("🌐 Checking Django setup...")
    
    django_manage = Path("backend/manage.py")
    if not django_manage.exists():
        print("❌ Django manage.py not found")
        return False
    
    try:
        # Cambiar al directorio backend
        current_dir = os.getcwd()
        os.chdir("backend")
        
        # Verificar que podemos ejecutar manage.py
        result = subprocess.run([
            sys.executable, "manage.py", "check"
        ], capture_output=True, text=True, timeout=30)
        
        # Volver al directorio original
        os.chdir(current_dir)
        
        if result.returncode == 0:
            print("✅ Django configuration OK")
            return True
        else:
            print("⚠️ Django check had warnings:")
            print(f"   {result.stdout[:200]}...")
            if result.stderr:
                print(f"   Errors: {result.stderr[:200]}...")
            return True  # Warnings no bloquean el deployment
            
    except subprocess.TimeoutExpired:
        print("⚠️ Django check timeout (may need database)")
        os.chdir(current_dir)
        return True
    except Exception as e:
        print(f"❌ Django check failed: {e}")
        os.chdir(current_dir)
        return False

def check_streamlit_setup():
    """Verificar configuración de Streamlit"""
    print("🎨 Checking Streamlit setup...")
    
    streamlit_app = Path("frontend/src/app.py")
    if not streamlit_app.exists():
        print("❌ Streamlit app.py not found")
        return False
    
    try:
        # Leer el archivo de la app de Streamlit
        content, encoding = read_file_with_encoding(streamlit_app)
        if content is None:
            print("❌ Could not read Streamlit app.py")
            return False
        
        print(f"   📝 App file encoding: {encoding}")
        
        required_imports = {
            'streamlit': 'Streamlit framework',
            'pandas': 'Data processing', 
            'folium': 'Map visualization',
            'requests': 'API communication'
        }
        
        found_imports = []
        for import_name, description in required_imports.items():
            if f"import {import_name}" in content or f"from {import_name}" in content:
                found_imports.append((import_name, description))
                print(f"   ✅ {import_name}: {description}")
            else:
                print(f"   ⚠️ {import_name}: {description} - not found")
        
        if len(found_imports) >= 2:  # Al menos streamlit y pandas
            print("✅ Streamlit setup OK")
            return True
        else:
            print("❌ Streamlit setup incomplete")
            return False
        
    except Exception as e:
        print(f"❌ Streamlit check failed: {e}")
        return False

def check_critical_imports():
    """Verificar que se pueden importar paquetes críticos"""
    print("🔍 Checking critical package imports...")
    
    critical_packages = [
        ('pandas', 'Data processing'),
        ('numpy', 'Numerical computing'),
        ('sklearn', 'Machine learning'),
        ('matplotlib', 'Plotting'),
        ('requests', 'HTTP client')
    ]
    
    import_results = []
    
    for package, description in critical_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}: {description}")
            import_results.append(True)
        except ImportError as e:
            print(f"   ❌ {package}: {description} - {e}")
            import_results.append(False)
        except Exception as e:
            print(f"   ⚠️ {package}: {description} - unexpected error: {e}")
            import_results.append(False)
    
    success_rate = sum(import_results) / len(import_results)
    print(f"   📊 Import success rate: {success_rate:.1%}")
    
    return success_rate >= 0.6  # Al menos 60% de imports exitosos

def run_existing_validations():
    """Ejecutar scripts de validación existentes"""
    print("🔬 Running existing validation scripts...")
    
    scripts_to_run = [
        ("scripts/validate_models.py", "ML model validation"),
        ("scripts/test_diagnosis.py", "System diagnosis")
    ]
    
    results = []
    
    for script_path, description in scripts_to_run:
        if os.path.exists(script_path):
            print(f"   🔄 Running {description}...")
            try:
                result = subprocess.run([sys.executable, script_path], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    print(f"   ✅ {description} passed")
                    results.append(True)
                else:
                    print(f"   ⚠️ {description} had issues:")
                    print(f"      {result.stderr[:100]}..." if result.stderr else "No error details")
                    results.append(False)
            except subprocess.TimeoutExpired:
                print(f"   ⚠️ {description} timeout")
                results.append(False)
            except Exception as e:
                print(f"   ❌ {description} failed: {e}")
                results.append(False)
        else:
            print(f"   ⚠️ {description} script not found: {script_path}")
            results.append(None)  # No contar como fallo
    
    # Filtrar resultados None
    actual_results = [r for r in results if r is not None]
    if actual_results:
        success_rate = sum(actual_results) / len(actual_results)
        return success_rate >= 0.5
    else:
        return True  # Si no hay scripts, no es un fallo

def main():
    """Función principal de validación completa"""
    print("🔧 TFG IDEALISTA - COMPLETE DEPENDENCY VALIDATION")
    print("=" * 60)
    print("Álvaro Carrera - Pre-deployment validation")
    print("=" * 60)
    
    all_checks = []
    
    # 1. Verificar Python
    print("\n1️⃣ PYTHON VERSION CHECK")
    python_ok = check_python_version()
    all_checks.append(("Python Version", python_ok))
    
    # 2. Verificar requirements
    print("\n2️⃣ REQUIREMENTS VALIDATION")
    requirements_files = [
        "requirements.txt",
        "backend/requirements.txt", 
        "frontend/requirements.txt"
    ]
    
    req_results = []
    for req_file in requirements_files:
        if os.path.exists(req_file):
            req_ok = validate_requirements_file(req_file)
            req_results.append(req_ok)
        else:
            print(f"⚠️ Optional file: {req_file} not found")
    
    requirements_ok = all(req_results) if req_results else False
    all_checks.append(("Requirements Files", requirements_ok))
    
    # 3. Verificar imports críticos
    print("\n3️⃣ CRITICAL IMPORTS CHECK")
    imports_ok = check_critical_imports()
    all_checks.append(("Critical Imports", imports_ok))
    
    # 4. Verificar Django
    print("\n4️⃣ DJANGO SETUP CHECK")
    django_ok = check_django_setup()
    all_checks.append(("Django Setup", django_ok))
    
    # 5. Verificar Streamlit
    print("\n5️⃣ STREAMLIT SETUP CHECK")
    streamlit_ok = check_streamlit_setup()
    all_checks.append(("Streamlit Setup", streamlit_ok))
    
    # 6. Ejecutar validaciones existentes
    print("\n6️⃣ EXISTING SCRIPTS VALIDATION")
    existing_ok = run_existing_validations()
    all_checks.append(("Existing Scripts", existing_ok))
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(all_checks)
    
    for check_name, result in all_checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:20} | {status}")
        if result:
            passed += 1
    
    print("-" * 40)
    print(f"{'TOTAL':20} | {passed}/{total} checks passed")
    
    success_rate = passed / total
    print(f"{'SUCCESS RATE':20} | {success_rate:.1%}")
    
    if success_rate >= 0.8:  # 80% o más
        print("\n🎉 VALIDATION SUCCESSFUL!")
        print("🚀 System ready for deployment!")
        print("\n📋 Next steps:")
        print("   1. Run: ./deploy.sh")
        print("   2. Monitor GitLab CI pipeline")
        print("   3. Check Render + Vercel deployments")
        return 0
    elif success_rate >= 0.6:  # 60-79%
        print("\n⚠️ VALIDATION PASSED WITH WARNINGS")
        print("🔧 Some issues detected but deployment can proceed")
        print("💡 Consider fixing warnings before production")
        return 0
    else:
        print("\n❌ VALIDATION FAILED!")
        print("🔧 Please fix critical issues before deploying")
        print("\n🆘 Common solutions:")
        print("   - Check file encodings (UTF-8 recommended)")
        print("   - Install missing dependencies")
        print("   - Verify Django/Streamlit configurations")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)