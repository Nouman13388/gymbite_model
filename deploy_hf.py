#!/usr/bin/env python3
"""
Deploy Gymbite to Hugging Face Spaces
"""

import subprocess
import sys


def run_command(cmd, description=""):
    """Run a shell command."""
    if description:
        print(f"\n📦 {description}")
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Error: {cmd}")
        return False
    return True


def main():
    print("\n" + "=" * 60)
    print("🤗 HUGGING FACE SPACES DEPLOYMENT")
    print("=" * 60)
    
    username = input("\n📝 Enter your Hugging Face username: ").strip()
    if not username:
        print("❌ Username required")
        return
    
    space_name = input("📝 Enter Space name (default: gymbite-model): ").strip() or "gymbite-model"
    
    print("\n" + "=" * 60)
    print("STEP 1: Create Space on Hugging Face")
    print("=" * 60)
    print("\n1. Open: https://huggingface.co/spaces/new")
    print("\n2. Fill in the form:")
    print("   • Owner: Your account")
    print(f"   • Space name: {space_name}")
    print("   • License: MIT (recommended)")
    print("   • Space SDK: Docker")
    print("   • Visibility: Public")
    print("\n3. Click 'Create Space'")
    
    input("\n⏳ Press Enter once you've created the Space on Hugging Face...")
    
    print("\n" + "=" * 60)
    print("STEP 2: Add Hugging Face Remote")
    print("=" * 60)
    
    hf_remote = f"https://huggingface.co/spaces/{username}/{space_name}"
    
    # Remove existing hf remote if it exists
    subprocess.run("git remote remove hf", shell=True, stderr=subprocess.DEVNULL)
    
    # Add new hf remote
    if not run_command(f"git remote add hf {hf_remote}", "Adding Hugging Face remote"):
        return
    
    print("\n" + "=" * 60)
    print("STEP 3: Push to Hugging Face Spaces")
    print("=" * 60)
    print("\n⚠️  This will build and deploy your Docker image automatically...")
    print("(This may take 2-5 minutes)\n")
    
    if not run_command("git push hf dev:main", "Pushing to Hugging Face Spaces"):
        print("\n❌ Push failed!")
        print("   Check your git configuration and ensure you have git credentials set up.")
        return
    
    print("\n" + "=" * 60)
    print("✅ DEPLOYMENT STARTED!")
    print("=" * 60)
    
    print(f"\n🎉 Your app is now deploying at:")
    print(f"   https://huggingface.co/spaces/{username}/{space_name}")
    
    print(f"\n⏳ Deployment typically takes 2-5 minutes. You can monitor progress in:")
    print(f"   • Build logs: https://huggingface.co/spaces/{username}/{space_name}/settings")
    
    print("\n📊 Next Steps:")
    print("\n1. Wait for the Space to build (watch the build logs)")
    print("\n2. Once deployed, test the health endpoint:")
    print(f"   curl https://huggingface.co/spaces/{username}/{space_name}/health")
    
    print("\n3. Test the prediction endpoint:")
    print(f"   curl -X POST https://huggingface.co/spaces/{username}/{space_name}/predict \\")
    print(f"     -H 'Content-Type: application/json' \\")
    print(f'     -d \'{{"age": 25, "weight": 75, "height": 180, "gender": "M"}}\'')
    
    print("\n4. Share your Space URL with others!")
    
    print("\n" + "=" * 60)
    print("💡 Useful Resources:")
    print("=" * 60)
    print("• Space settings: https://huggingface.co/spaces/{username}/{space_name}/settings")
    print("• Documentation: https://huggingface.co/docs/hub/spaces")
    print("• Docker guide: https://huggingface.co/docs/hub/spaces-docker")
    print()


if __name__ == "__main__":
    main()
