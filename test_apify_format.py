#!/usr/bin/env python3
"""Test script to verify Apify startUrls format is correct."""
import json

# Test the format we're sending
app_url = "https://apps.apple.com/us/app/flo-period-pregnancy-tracker/id1038361850"

# Wrong format (what we had):
wrong_format = [{"url": app_url}]
print("❌ Wrong format (what we had):")
print(json.dumps({"startUrls": wrong_format}, indent=2))

# Correct format (what Apify expects):
correct_format = [app_url]
print("\n✅ Correct format (what Apify expects):")
print(json.dumps({"startUrls": correct_format}, indent=2))

print("\n" + "="*60)
print("The issue: Apify expects an array of URL strings, not objects")
print("Fix: Change [{\"url\": \"...\"}] to [\"...\"]")
print("="*60)
