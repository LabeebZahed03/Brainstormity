import secrets

# Generate a secure API key for your frontend team
api_key = "bst_prod_" + secrets.token_urlsafe(32)
print(f"Generated API Key: {api_key}")
print(f"Add this to your main.py VALID_API_KEYS dictionary")
