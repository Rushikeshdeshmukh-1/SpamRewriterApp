import google.generativeai as genai

# Your API key
api_key = "AIzaSyApRtIWlXf8Ya_bImiYSk0g66CCphZFf3I"

# Configure API
genai.configure(api_key=api_key)

print("Testing different model names...")

# Models to test (most common working ones)
test_models = [
    "models/gemini-1.5-flash",
    "models/gemini-1.5-pro",
    "models/gemini-pro",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-pro"
]

working_model = None

for model_name in test_models:
    try:
        print(f"\nTrying: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello, this is a test")

        if response.text:
            print(f"✅ SUCCESS! Model '{model_name}' works!")
            print(f"Response: {response.text[:100]}...")
            working_model = model_name
            break

    except Exception as e:
        print(f"❌ Failed: {e}")

if working_model:
    print(f"\n🎉 USE THIS MODEL: '{working_model}'")
    print(f"\nNow update your llm_rewriter.py file:")
    print(f"Replace the model initialization with:")
    print(f"self.model = genai.GenerativeModel('{working_model}')")
else:
    print("\n❌ No working models found. Let's check what's available...")
    try:
        models = genai.list_models()
        print("\nAvailable models:")
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                print(f"  • {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")