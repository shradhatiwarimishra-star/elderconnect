"""
Quick test to check CORS configuration
"""
from app import create_app

app = create_app()

print("=" * 60)
print("CORS Configuration Test")
print("=" * 60)
print(f"\nCORS_ORIGINS from config: {app.config.get('CORS_ORIGINS')}")
print(f"FRONTEND_URL from config: {app.config.get('FRONTEND_URL', 'NOT SET')}")

# Test if CORS is working
with app.test_client() as client:
    # Simulate OPTIONS preflight request
    response = client.options('/api/bookings',
        headers={
            'Origin': 'http://localhost:5173',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Authorization'
        })
    
    print(f"\nOPTIONS /api/bookings response:")
    print(f"  Status: {response.status_code}")
    print(f"  Headers:")
    for header, value in response.headers:
        if 'Access-Control' in header or 'Allow' in header:
            print(f"    {header}: {value}")

print("\n" + "=" * 60)
print("If you see 'Access-Control-Allow-Origin' header above,")
print("CORS is configured correctly!")
print("=" * 60)
