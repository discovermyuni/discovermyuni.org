#!/usr/bin/env python3
"""
Build script for DiscoverMyUni project
Compiles Tailwind CSS and prepares static assets
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description="Running command"):
    """Run a shell command and handle errors"""
    print(f"🔨 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, cwd=Path(__file__).parent)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with error: {e}")
        return False

def compile_tailwind():
    """Compile Tailwind CSS"""
    input_css = "discovermyuni/static/css/tailwind.css"
    output_css = "discovermyuni/static/css/tailwind.build.css"
    config_file = "tailwind.config.cjs"
    
    # Check if input file exists
    if not Path(input_css).exists():
        print(f"❌ Input file {input_css} not found")
        return False
        
    # Check if config file exists
    if not Path(config_file).exists():
        print(f"❌ Config file {config_file} not found")
        return False
    
    # Try multiple ways to run Tailwind
    commands = [
        f"npx tailwindcss -i {input_css} -o {output_css} --minify",
        f"tailwindcss -i {input_css} -o {output_css} --minify",
        f"node_modules\\.bin\\tailwindcss -i {input_css} -o {output_css} --minify"
    ]
    
    for cmd in commands:
        if run_command(cmd, f"Compiling Tailwind CSS with: {cmd}"):
            return True
    
    print("❌ Could not compile Tailwind CSS with any method")
    return False

def collect_static():
    """Collect Django static files"""
    return run_command("python manage.py collectstatic --noinput", "Collecting Django static files")

def main():
    """Main build process"""
    print("🚀 Starting DiscoverMyUni build process...")
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    success = True
    
    # Step 1: Compile Tailwind CSS
    if not compile_tailwind():
        success = False
    
    # Step 2: Collect static files (if Django is set up)
    if Path("manage.py").exists():
        if not collect_static():
            print("⚠️  Django static collection failed, but continuing...")
    else:
        print("ℹ️  No manage.py found, skipping Django static collection")
    
    if success:
        print("🎉 Build completed successfully!")
        print("📁 Check discovermyuni/static/css/tailwind.build.css for compiled CSS")
    else:
        print("💥 Build failed - check errors above")
        sys.exit(1)

if __name__ == "__main__":
    main()