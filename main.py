import os
from PIL import Image
from vision import get_actions
from scrapebot import scrape

scrape()

# Path to the screenshots directory
screenshots_dir = "screenshots/"

# List all files in the screenshots directory
screenshot_files = os.listdir(screenshots_dir)

# Process each screenshot
for screenshot_file in screenshot_files:
    # Construct the full path to the screenshot
    screenshot_path = os.path.join(screenshots_dir, screenshot_file)
    
    # Open the screenshot image
    screenshot_image = Image.open(screenshot_path)
    
    # Call the action file from vision to process the screenshot
    actions = get_actions(screenshot_image)
    
    # Optional: Handle the actions as needed
    # For example, print them or store them in a database
    print(actions)
