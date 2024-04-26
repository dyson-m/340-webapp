"""
This is for inserting initial data into the database.
Entering "flask seed" in the terminal will cause these items to be inserted into the database.
"""
from . import create_app
from .extensions import db
from .models import Product

def seed_products():
    products = [
        {'name': 'Smart TV', 'description': '55" 4K Ultra HD LED TV', 'price': 599.99, 'stock': 50},
        {'name': 'Bluetooth Speaker', 'description': 'Portable Wireless Bluetooth Speaker', 'price': 39.95, 'stock': 100},
        {'name': 'Gaming Console', 'description': 'Next-Gen Gaming Console with 1TB Storage', 'price': 399.75, 'stock': 80},
        {'name': 'Streaming Device', 'description': '4K HDR Streaming Media Player', 'price': 79.5, 'stock': 120},
        {'name': 'Wireless Earbuds', 'description': 'True Wireless Bluetooth Earbuds', 'price': 59.25, 'stock': 150},
        {'name': 'Fitness Tracker', 'description': 'Waterproof Fitness Tracker with Heart Rate Monitor', 'price': 29.99, 'stock': 200},
        {'name': 'Smart Thermostat', 'description': 'Programmable Smart Thermostat', 'price': 99.8, 'stock': 70},
        {'name': 'Robot Vacuum', 'description': 'Robotic Vacuum Cleaner with Mapping Technology', 'price': 199.5, 'stock': 60},
        {'name': 'Digital Camera', 'description': '24MP Digital Camera with 4K Video Recording', 'price': 299.25, 'stock': 90},
        {'name': 'Electric Toothbrush', 'description': 'Sonic Electric Toothbrush with UV Sanitizer', 'price': 49.75, 'stock': 100},
        {'name': 'Wireless Charger', 'description': 'Qi-Certified Wireless Charging Pad', 'price': 19.99, 'stock': 150},
        {'name': 'Bluetooth Headphones', 'description': 'Over-Ear Bluetooth Headphones', 'price': 49.5, 'stock': 100},
        {'name': 'Smart Doorbell', 'description': 'Wi-Fi Video Doorbell with Two-Way Audio', 'price': 119.9, 'stock': 50},
        {'name': 'Portable Power Bank', 'description': 'High-Capacity Portable Charger', 'price': 29.75, 'stock': 200},
        {'name': 'Home Security Camera', 'description': 'Indoor/Outdoor HD Security Camera System', 'price': 149.25, 'stock': 70},
        {'name': 'E-Reader', 'description': 'E-Ink Display E-Reader with Built-in Light', 'price': 99.99, 'stock': 80},
        {'name': 'Wireless Router', 'description': 'Dual-Band Wi-Fi Router with Gigabit Ethernet', 'price': 79.25, 'stock': 100},
        {'name': 'Smart Light Bulbs', 'description': 'Wi-Fi Connected LED Smart Bulbs', 'price': 14.99, 'stock': 250},
        {'name': 'Portable Projector', 'description': 'Mini HD Portable Projector', 'price': 99.75, 'stock': 60},
        {'name': 'Digital Scale', 'description': 'Bluetooth Smart Body Fat Scale', 'price': 24.95, 'stock': 120},
        {'name': 'Smartwatch', 'description': 'Waterproof Smartwatch with Fitness Tracker', 'price': 129.5, 'stock': 50},
        {'name': 'Wireless Mouse', 'description': 'Ergonomic Wireless Mouse with Silent Click', 'price': 19.75, 'stock': 100},
        {'name': 'Noise-Canceling Headphones', 'description': 'Bluetooth Noise-Canceling Headphones', 'price': 79.99, 'stock': 80},
        {'name': 'Tablet', 'description': '10.1" Android Tablet with Quad-Core Processor', 'price': 179.25, 'stock': 120},
        {'name': 'Home Assistant', 'description': 'Smart Home Assistant Speaker with Voice Control', 'price': 99.5, 'stock': 150},
        {'name': 'Action Camera', 'description': '4K Action Camera with Waterproof Case', 'price': 69.9, 'stock': 200},
        {'name': 'Wi-Fi Range Extender', 'description': 'Dual-Band Wi-Fi Range Extender', 'price': 34.95, 'stock': 70},
        {'name': 'External Hard Drive', 'description': '2TB Portable External Hard Drive', 'price': 89.75, 'stock': 60},
        {'name': 'Wireless Keyboard', 'description': 'Compact Wireless Keyboard with Touchpad', 'price': 29.99, 'stock': 90},
        {'name': 'Smart Plug', 'description': 'Mini Wi-Fi Smart Plug', 'price': 14.5, 'stock': 100},
        {'name': 'Bluetooth Car Kit', 'description': 'Bluetooth Car Adapter with Hands-Free Calling', 'price': 24.75, 'stock': 150},
        {'name': 'Fitness Smart Scale', 'description': 'Digital Bluetooth Smart Scale with BMI Tracking', 'price': 39.25, 'stock': 100},
        {'name': 'Wireless Earphones', 'description': 'Wireless Earphones with Charging Case', 'price': 49.99, 'stock': 50},
        {'name': 'USB-C Hub', 'description': '7-in-1 USB-C Hub with 4K HDMI and SD Card Reader', 'price': 49.9, 'stock': 200},
        {'name': 'VR Headset', 'description': 'All-in-One Virtual Reality Headset with Controller', 'price': 199.75, 'stock': 70},
        {'name': 'Dash Cam', 'description': '1080p Dash Cam with Night Vision', 'price': 59.95, 'stock': 80},
        {'name': 'Portable DVD Player', 'description': '9" Portable DVD Player with Swivel Screen', 'price': 69.5, 'stock': 100},
        {'name': 'Smart Wi-Fi Bulb', 'description': 'Color-Changing Smart Wi-Fi LED Bulb', 'price': 19.25, 'stock': 250},
        {'name': 'Mini Projector', 'description': 'Portable Mini Projector with HDMI Input', 'price': 79.99, 'stock': 60},
        {'name': 'Wireless Charging Stand', 'description': '2-in-1 Wireless Charging Stand for Phone and Watch', 'price': 39.75, 'stock': 120},
        {'name': 'Blackberry Phone', 'description': 'The ye olden blackberry phone, with the light up keyboard', 'price': 199.99, 'stock': 3}
    ]
    for product in products:
        new_product = Product(**product)
        db.session.add(new_product)
    db.session.commit()
    print("Seeded products...")


def seed_users():
    users = [
        # Add some seed users?
    ]

    for user in users:
        new_user = User(**user)
        db.session.add(user)
    db.session.commit()
    print("Seeding users...")

def seed():
    seed_products()
    seed_users()
    

