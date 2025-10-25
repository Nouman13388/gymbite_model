#!/usr/bin/env python3
"""
Gymbite Deployment Helper Script
Helps deploy Gymbite to various platforms
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description=""):
    """Run a shell command and handle errors."""
    if description:
        print(f"\n📦 {description}")
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Error running: {cmd}")
        sys.exit(1)
    return result


def deploy_docker_local():
    """Deploy locally using Docker."""
    print("\n🐳 Deploying to Local Docker...")
    run_command("docker build -t gymbite_model:local .", "Building Docker image")
    run_command(
        'docker run --rm -p 7860:7860 -v "${PWD}:/app" --name gymbite_local gymbite_model:local',
        "Starting container on port 7860"
    )
    print("\n✅ App running at http://localhost:7860")
    print("   Health check: curl http://localhost:7860/health")


def deploy_docker_hub():
    """Deploy to Docker Hub."""
    print("\n🐳 Preparing Docker Hub deployment...")
    
    username = input("Enter your Docker Hub username: ").strip()
    if not username:
        print("❌ Docker Hub username required")
        return
    
    run_command("docker login", "Login to Docker Hub")
    run_command(f"docker build -t {username}/gymbite-model:latest .", "Building image")
    run_command(f"docker push {username}/gymbite-model:latest", "Pushing to Docker Hub")
    
    print(f"\n✅ Image pushed to: docker.io/{username}/gymbite-model:latest")
    print(f"   Run with: docker run -p 7860:7860 {username}/gymbite-model:latest")


def deploy_hugging_face():
    """Deploy to Hugging Face Spaces."""
    print("\n🤗 Preparing Hugging Face Spaces deployment...")
    print("\n📋 Steps:")
    print("1. Go to https://huggingface.co/spaces/new")
    print("2. Create a new Space with:")
    print("   - Name: gymbite-model")
    print("   - License: MIT (or your choice)")
    print("   - Space SDK: Docker")
    print("")
    
    username = input("Enter your Hugging Face username: ").strip()
    if not username:
        print("❌ Username required")
        return
    
    hf_url = f"https://huggingface.co/spaces/{username}/gymbite-model"
    
    print(f"\n3. After creating the Space, run these commands:")
    print(f"   git remote add hf https://huggingface.co/spaces/{username}/gymbite-model")
    print(f"   git add .")
    print(f"   git commit -m 'Deploy Gymbite to Hugging Face Spaces'")
    print(f"   git push hf dev:main")
    print("")
    print(f"✅ Your app will be live at: {hf_url}")
    print("   (Spaces will automatically build and deploy your Docker image)")


def deploy_render():
    """Deploy to Render.com."""
    print("\n🚀 Preparing Render.com deployment...")
    print("\n📋 Steps:")
    print("1. Go to https://render.com")
    print("2. Sign up or log in with GitHub")
    print("3. Click 'New +' → 'Web Service'")
    print("4. Connect your gymbite_model repository")
    print("5. Configure:")
    print("   - Name: gymbite-model")
    print("   - Environment: Docker")
    print("   - Port: 7860")
    print("6. Click 'Create Web Service'")
    print("")
    print("✅ Render will automatically deploy on push to dev branch")


def deploy_railway():
    """Deploy to Railway.app."""
    print("\n🚂 Preparing Railway.app deployment...")
    print("\n📋 Steps:")
    print("1. Go to https://railway.app")
    print("2. Sign up with GitHub")
    print("3. Click 'New Project' → 'Deploy from GitHub repo'")
    print("4. Select your gymbite_model repository")
    print("5. Railway auto-detects Dockerfile")
    print("6. Set environment variable: PORT=7860")
    print("7. Deploy")
    print("")
    print("✅ Your app will be live at Railway-provided URL")


def test_health_endpoint(url="http://localhost:7860"):
    """Test the health endpoint."""
    print(f"\n🏥 Testing health endpoint at {url}/health...")
    try:
        import requests
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(response.json())
        else:
            print(f"❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")


def main():
    """Main menu."""
    print("\n" + "="*60)
    print("🎯 Gymbite Deployment Helper")
    print("="*60)
    
    options = {
        "1": ("Local Docker", deploy_docker_local),
        "2": ("Docker Hub", deploy_docker_hub),
        "3": ("Hugging Face Spaces", deploy_hugging_face),
        "4": ("Render.com", deploy_render),
        "5": ("Railway.app", deploy_railway),
        "6": ("Test Health Endpoint", test_health_endpoint),
    }
    
    print("\nChoose a deployment option:")
    for key, (name, _) in options.items():
        print(f"  {key}. {name}")
    print("  0. Exit")
    
    choice = input("\nEnter your choice (0-6): ").strip()
    
    if choice == "0":
        print("Goodbye!")
        return
    
    if choice in options:
        name, func = options[choice]
        print(f"\nSelected: {name}")
        try:
            func()
        except KeyboardInterrupt:
            print("\n\nCancelled by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
