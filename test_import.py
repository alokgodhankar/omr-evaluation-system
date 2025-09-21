#!/usr/bin/env python3
"""
Test Import Script for OMR Evaluation System
This script tests all required imports and dependencies
"""

import sys
import importlib
import subprocess
from pathlib import Path

def test_import(module_name, package_name=None):
    """Test if a module can be imported successfully"""
    try:
        if package_name:
            importlib.import_module(module_name, package=package_name)
        else:
            importlib.import_module(module_name)
        print(f"✅ {module_name} imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import {module_name}: {e}")
        return False

def test_python_version():
    """Test Python version compatibility"""
    print(f"Python version: {sys.version}")
    if sys.version_info >= (3, 7):
        print("✅ Python version is compatible (3.7+)")
        return True
    else:
        print("❌ Python version too old. Requires 3.7+")
        return False

def test_file_exists(file_path):
    """Test if required files exist"""
    path = Path(file_path)
    if path.exists():
        print(f"✅ {file_path} exists")
        return True
    else:
        print(f"❌ {file_path} not found")
        return False

def test_opencv_functionality():
    """Test OpenCV basic functionality"""
    try:
        import cv2
        # Test basic OpenCV operations
        import numpy as np
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        print("✅ OpenCV functionality test passed")
        return True
    except Exception as e:
        print(f"❌ OpenCV functionality test failed: {e}")
        return False

def test_streamlit_availability():
    """Test if Streamlit is available"""
    try:
        import streamlit as st
        print("✅ Streamlit is available")
        return True
    except ImportError as e:
        print(f"❌ Streamlit not available: {e}")
        return False

def test_pillow_functionality():
    """Test Pillow basic functionality"""
    try:
        from PIL import Image
        import numpy as np
        # Create test image
        test_array = np.random.randint(0, 255, (50, 50, 3), dtype=np.uint8)
        test_image = Image.fromarray(test_array)
        print("✅ Pillow functionality test passed")
        return True
    except Exception as e:
        print(f"❌ Pillow functionality test failed: {e}")
        return False

def test_custom_modules():
    """Test if custom modules can be imported"""
    modules_to_test = ['answer_keys', 'omr_processor']
    all_passed = True
    
    for module in modules_to_test:
        try:
            importlib.import_module(module)
            print(f"✅ {module}.py imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {module}.py: {e}")
            all_passed = False
    
    return all_passed

def test_dependencies():
    """Test all required dependencies"""
    print("🔍 Testing required dependencies...")
    print("=" * 50)
    
    dependencies = [
        ('cv2', 'opencv-python'),
        ('numpy', 'numpy'),
        ('PIL', 'Pillow'),
        ('streamlit', 'streamlit'),
    ]
    
    all_passed = True
    
    for module, package in dependencies:
        if not test_import(module):
            print(f"   💡 Install with: pip install {package}")
            all_passed = False
    
    return all_passed

def test_system_health():
    """Complete system health check"""
    print("🏥 Running OMR System Health Check")
    print("=" * 50)
    
    # Test Python version
    python_ok = test_python_version()
    print()
    
    # Test dependencies
    deps_ok = test_dependencies()
    print()
    
    # Test file existence
    print("📁 Testing required files...")
    required_files = ['web_app.py', 'omr_processor.py', 'answer_keys.py', 'test_answer_keys.py']
    files_ok = all(test_file_exists(f) for f in required_files)
    print()
    
    # Test custom modules
    print("🔧 Testing custom modules...")
    custom_ok = test_custom_modules()
    print()
    
    # Test functionality
    print("⚙️ Testing functionality...")
    opencv_ok = test_opencv_functionality()
    pillow_ok = test_pillow_functionality()
    streamlit_ok = test_streamlit_availability()
    print()
    
    # Summary
    print("📊 SUMMARY")
    print("=" * 50)
    
    all_tests_passed = all([
        python_ok,
        deps_ok,
        files_ok,
        custom_ok,
        opencv_ok,
        pillow_ok,
        streamlit_ok
    ])
    
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! System is ready to use.")
        print("\n🚀 To start the OMR system, run:")
        print("   streamlit run web_app.py")
        print("\n🧪 To run unit tests, run:")
        print("   python test_answer_keys.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n💡 Installation command for all dependencies:")
        print("   pip install streamlit opencv-python numpy Pillow")
    
    return all_tests_passed

def install_missing_dependencies():
    """Install missing dependencies"""
    print("📦 Installing missing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "streamlit", "opencv-python", "numpy", "Pillow"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

if __name__ == "__main__":
    print("🔬 OMR Evaluation System - Import Test")
    print("=" * 50)
    
    # Run health check
    system_healthy = test_system_health()
    
    if not system_healthy:
        print("\n" + "=" * 50)
        response = input("❌ Some dependencies are missing. Install them now? (y/n): ")
        if response.lower() in ['y', 'yes']:
            install_missing_dependencies()
            print("\n🔄 Re-running health check after installation...")
            print("=" * 50)
            test_system_health()