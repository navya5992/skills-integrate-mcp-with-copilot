#!/usr/bin/env python3
"""
Generate QR Code for Memory Match Arena
Creates a QR code that mobile devices can scan to access the game
"""

import qrcode
import os
from PIL import Image, ImageDraw, ImageFont
import socket
from pathlib import Path

def get_local_network_ip():
    """Get the local network IP address."""
    try:
        # Try to get the local IP by connecting to a remote server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def generate_qr_code():
    """Generate QR code for mobile access."""
    port = 5000
    local_ip = get_local_network_ip()

    # Check if we're in a dev container
    in_dev_container = (
        local_ip.startswith('10.') or  # Docker bridge network
        local_ip.startswith('172.') or # Docker bridge network
        '/workspaces/' in os.getcwd()  # VS Code dev container
    )

    if in_dev_container:
        # In dev container, use localhost (will be forwarded by VS Code)
        game_url = f"http://localhost:{port}"
        print("🐳 DEV CONTAINER DETECTED")
        print("📱 QR Code will use localhost (forward via VS Code Ports panel)")
    else:
        # Use network IP for direct access
        game_url = f"http://{local_ip}:{port}"
        print("🏠 LOCAL MACHINE DETECTED")
        print("📱 QR Code will use network IP")

    print(f"🎮 Game URL: {game_url}")
    print(f"🌐 Local IP: {local_ip}")

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(game_url)
    qr.make(fit=True)

    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Add text below QR code
    # Convert to RGB if needed
    if qr_img.mode != 'RGB':
        qr_img = qr_img.convert('RGB')

    # Create new image with space for text
    width, height = qr_img.size
    new_height = height + 80  # Space for text
    combined_img = Image.new('RGB', (width, new_height), 'white')

    # Paste QR code
    combined_img.paste(qr_img, (0, 0))

    # Add text
    draw = ImageDraw.Draw(combined_img)

    # Try to use a nice font, fallback to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        except:
            font = ImageFont.load_default()

    # Add title
    title = "Memory Match Arena"
    draw.text((width//2, height + 10), title, fill="black", font=font, anchor="mm")

    # Add URL
    url_text = f"Scan to play: {game_url}"
    draw.text((width//2, height + 35), url_text, fill="black", font=font, anchor="mm")

    # Add instructions for dev container
    if in_dev_container:
        instruction = "VS Code: Forward port 5000 for mobile access"
        draw.text((width//2, height + 55), instruction, fill="red", font=font, anchor="mm")

    # Save the image
    static_dir = Path(__file__).parent / "src" / "web_frontend" / "static"
    static_dir.mkdir(parents=True, exist_ok=True)
    qr_path = static_dir / "game_qr.png"
    combined_img.save(str(qr_path))

    print(f"✅ QR Code saved to: {qr_path}")
    print("📱 Mobile devices can scan this QR code to access the game")
    if in_dev_container:
        print("⚠️  IMPORTANT: Set up VS Code port forwarding first!")

if __name__ == "__main__":
    generate_qr_code()
