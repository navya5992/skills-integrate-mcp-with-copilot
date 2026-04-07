#!/usr/bin/env python3
"""
Mobile Access Test Script
Tests if the memory game server is accessible from different network locations
"""

import requests
import socket
import json
from datetime import datetime

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Create a socket to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def test_server_access(ip, port=5000):
    """Test if server is accessible on given IP"""
    try:
        url = f"http://{ip}:{port}/api/health"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, str(e)

def main():
    print("🔍 MEMORY GAME MOBILE ACCESS TEST")
    print("=" * 50)

    # Get network info
    local_ip = get_local_ip()
    container_ip = "10.0.4.242"  # From our earlier checks

    print(f"📍 Local IP: {local_ip}")
    print(f"🐳 Container IP: {container_ip}")
    print(f"🔌 Port: 5000")
    print()

    # Test localhost
    print("🧪 TESTING LOCALHOST ACCESS:")
    success, result = test_server_access("127.0.0.1")
    if success:
        print("✅ Localhost: ACCESSIBLE")
        print(f"   Response: {result}")
    else:
        print("❌ Localhost: NOT ACCESSIBLE")
        print(f"   Error: {result}")

    # Test container IP
    print("\n🧪 TESTING CONTAINER IP ACCESS:")
    success, result = test_server_access(container_ip)
    if success:
        print("✅ Container IP: ACCESSIBLE")
        print(f"   Response: {result}")
    else:
        print("❌ Container IP: NOT ACCESSIBLE")
        print(f"   Error: {result}")

    # Test local network IP
    print("\n🧪 TESTING LOCAL NETWORK IP ACCESS:")
    success, result = test_server_access(local_ip)
    if success:
        print("✅ Local Network: ACCESSIBLE")
        print(f"   Response: {result}")
    else:
        print("❌ Local Network: NOT ACCESSIBLE")
        print(f"   Error: {result}")

    print("\n📋 RECOMMENDATIONS:")
    print("=" * 30)
    print("1. 📱 Use VS Code Port Forwarding:")
    print("   - Open Command Palette (Ctrl+Shift+P)")
    print("   - Type: 'Ports: Focus on Ports View'")
    print("   - Forward port 5000")
    print("   - Use the forwarded localhost URL on mobile")

    print("\n2. 🌐 Use ngrok for public access:")
    print("   - Install: pip install pyngrok")
    print("   - Run tunnel script to get public URL")

    print("\n3. 🔧 Manual port forwarding:")
    print("   - Forward port 5000 from host to container")
    print("   - Use host IP on mobile device")

if __name__ == "__main__":
    main()