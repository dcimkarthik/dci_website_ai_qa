import os
from analyzer import analyze_website
from ai_test_generator import generate_tests

URL = input("Enter website URL: ")

print("Analyzing website...")
screenshot, tree = analyze_website(URL)

print("Generating test cases using AI...")
code = generate_tests(URL, screenshot, tree)

os.makedirs("tests", exist_ok=True)

with open("tests/generated_test.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Done!")
print("Generated: tests/generated_test.py")