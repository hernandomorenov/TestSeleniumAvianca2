import subprocess
import os
import sys
import time
from datetime import datetime

def print_banner():
    """Imprimir banner del proyecto"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                 AVIANCA AUTOMATION SUITE                ║
    ║                  Complete Test Runner                   ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def run_parallel_tests():
    """Ejecutar pruebas en paralelo"""
    print("\n" + "="*70)
    print("🚀 EJECUCIÓN PARALELA DE TODOS LOS TESTS")
    print("="*70)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Comando base optimizado
    base_cmd = [
        "pytest",
        "tests/",
        "-v",
        "--tb=short",
        f"--alluredir=reports/allure-results",
        "--html=reports/html-report.html",
        "--self-contained-html",
        "-n", "auto",  # Automático según CPUs
        "--dist=loadscope",
        "--disable-warnings",
        "--capture=no",
        "--headless",  # Para mayor velocidad
        f"--browser=chrome"  # Puedes cambiar esto
    ]
    
    print(f"\n📋 Comando: {' '.join(base_cmd)}")
    print(f"🕐 Inicio: {datetime.now().strftime('%H:%M:%S')}")
    print("-"*70)
    
    start_time = time.time()
    
    try:
        # Ejecutar pruebas
        result = subprocess.run(base_cmd, check=False, capture_output=True, text=True)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n{'='*70}")
        print("📊 RESULTADOS DE LA EJECUCIÓN")
        print(f"{'='*70}")
        
        # Extraer estadísticas
        output = result.stdout
        
        # Buscar líneas de resumen
        for line in output.split('\n'):
            if "passed" in line and "failed" in line and "skipped" in line:
                print(f"📈 {line}")
            elif "ERROR" in line or "FAILED" in line:
                if "short test summary info" not in line:
                    print(f"❌ {line}")
        
        print(f"\n⏱️  Duración total: {duration:.2f} segundos")
        print(f"🕐 Fin: {datetime.now().strftime('%H:%M:%S')}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error ejecutando pruebas: {e}")
        return False

def run_specific_test(test_number, browser="chrome"):
    """Ejecutar un test específico"""
    test_files = {
        "1": "test_case_1_one_way.py",
        "2": "test_case_2_round_trip.py",
        "3": "test_case_3_login.py",
        "4": "test_case_4_language.py",
        "5": "test_case_5_pos.py",
        "6": "test_case_6_header_redirects.py",
        "7": "test_case_7_footer_redirects.py"
    }
    
    if test_number not in test_files:
        print(f"❌ Test {test_number} no válido. Opciones: 1-7")
        return False
    
    test_file = f"tests/{test_files[test_number]}"
    
    print(f"\n🎯 Ejecutando Test Case {test_number} en {browser.upper()}")
    print("-"*50)
    
    cmd = [
        "pytest",
        test_file,
        "-v",
        f"--browser={browser}",
        "--tb=short",
        "--capture=no"
    ]
    
    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        print(result.stdout)
        
        if result.stderr:
            print(f"⚠️  Errores: {result.stderr}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_browsers():
    """Ejecutar todos los tests en todos los navegadores"""
    browsers = ["chrome", "firefox", "edge"]
    results = {}
    
    print("\n" + "="*70)
    print("🌐 EJECUCIÓN EN TODOS LOS NAVEGADORES")
    print("="*70)
    
    for browser in browsers:
        print(f"\n🔧 Ejecutando en {browser.upper()}...")
        print("-"*50)
        
        cmd = [
            "pytest",
            "tests/",
            "-v",
            f"--browser={browser}",
            "--headless",
            "--tb=short",
            "-q"  # Modo quiet para resumen
        ]
        
        try:
            result = subprocess.run(cmd, check=False, capture_output=True, text=True)
            
            # Extraer resultado
            for line in result.stdout.split('\n'):
                if "passed" in line and "failed" in line:
                    results[browser] = line
                    print(f"✅ {browser.upper()}: {line}")
                    break
            else:
                results[browser] = "Error"
                print(f"❌ {browser.upper()}: Error en ejecución")
                
        except Exception as e:
            results[browser] = f"Error: {e}"
            print(f"❌ {browser.upper()}: {e}")
    
    # Mostrar resumen
    print("\n" + "="*70)
    print("📋 RESUMEN MULTI-NAVEGADOR")
    print("="*70)
    
    for browser, result in results.items():
        print(f"{browser.upper():10} {result}")
    
    return all("failed: 0" in str(r) for r in results.values())

def generate_allure_report():
    """Generar reporte Allure"""
    print("\n📊 Generando reporte Allure...")
    
    if not os.path.exists("reports/allure-results"):
        print("❌ No hay resultados de Allure para generar reporte")
        return False
    
    try:
        result = subprocess.run([
            "allure", "generate", "reports/allure-results",
            "--clean", "-o", "reports/allure-report"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Reporte Allure generado exitosamente")
        print("📁 Ubicación: reports/allure-report/index.html")
        
        # Preguntar si abrir el reporte
        if sys.platform == "darwin":  # macOS
            open_cmd = "open"
        elif sys.platform == "win32":  # Windows
            open_cmd = "start"
        else:  # Linux
            open_cmd = "xdg-open"
        
        choice = input("\n¿Abrir reporte Allure en el navegador? (s/n): ").lower()
        if choice == 's':
            subprocess.run([open_cmd, "reports/allure-report/index.html"])
        
        return True
        
    except Exception as e:
        print(f"❌ Error generando reporte Allure: {e}")
        print("\n💡 Para instalar Allure:")
        print("  macOS: brew install allure")
        print("  Windows: choco install allure")
        print("  Linux: sudo apt-get install allure")
        return False

def main():
    """Función principal"""
    print_banner()
    
    print("Opciones de ejecución:")
    print("1. ✅ Ejecutar TODOS los tests en paralelo (recomendado)")
    print("2. 🌐 Ejecutar en TODOS los navegadores")
    print("3. 🎯 Ejecutar test específico (1-7)")
    print("4. 📊 Generar reporte Allure")
    print("5. 🚪 Salir")
    
    choice = input("\nSeleccione una opción (1-5): ").strip()
    
    if choice == "1":
        success = run_parallel_tests()
        if success:
            generate_allure_report()
        
    elif choice == "2":
        success = run_all_browsers()
        if success:
            generate_allure_report()
        
    elif choice == "3":
        test_num = input("Número de test (1-7): ").strip()
        browser = input("Navegador (chrome/firefox/edge) [chrome]: ").strip() or "chrome"
        run_specific_test(test_num, browser)
        
    elif choice == "4":
        generate_allure_report()
        
    elif choice == "5":
        print("\n👋 ¡Hasta luego!")
        sys.exit(0)
        
    else:
        print("❌ Opción no válida")

if __name__ == "__main__":
    # Crear directorios necesarios
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("videos", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("drivers", exist_ok=True)
    
    main()