import google.generativeai as genai

# Use your API key directly
api_key = "AIzaSyA2mS-VvxXBIDCtjgB7z4wJNDaQ1uDJlsA"
genai.configure(api_key=api_key)

print("\nAvailable Gemini models:")
print("=" * 60)
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"  ✓ {m.name}")
print("=" * 60)
