CAMT Text Generator: Setup and Installation Guide
Welcome! This guide will walk you through exactly how to get this program running on your computer, even if you have zero technical experience. You only need to do this setup once.

Step 1: Download the Code

Go to the main page of this GitHub repository.

Click the green Code button near the top right of the files.

Select Download ZIP from the dropdown menu .

Once downloaded, double-click the ZIP file to extract (unzip) it.

Move the extracted folder to an easy-to-find place, like your Desktop. Ensure the folder contains the core files, including camt_gui.py, citation_averages.json, and citation_percentiles.json.

Step 2: Install Python
Python is the engine that runs this application.

Go to the official website: python.org/downloads

Click the big download button for the latest version of Python.

Windows Users (Crucial Step): When you open the installer, look at the very bottom of the first screen. You must check the box that says "Add python.exe to PATH" . If you skip this, the next steps will fail! Click "Install Now" and wait for it to finish.

Mac Users: Simply run the downloaded installer package and click through the standard "Continue" and "Install" prompts.

Step 3: Open your Computer's Terminal
We need to type a few simple text commands to finish the setup.

Windows: Click your Start menu, type cmd, and open the Command Prompt.

Mac: Press Command + Space on your keyboard to open Spotlight search, type Terminal, and press Enter .

Step 4: Navigate to the Project Folder
In your terminal window, type the letters cd followed by a single space. (Do not press Enter yet).

Find the extracted project folder from Step 1 on your computer.

Click and drag that folder directly into the terminal window. This automatically pastes the exact path to the folder!

Press Enter.

Step 5: Install the Required Tools
This program relies on a language processing library called spacy. We need to download it.

Windows: Type pip install spacy and press Enter.

Mac: Type pip3 install spacy and press Enter.

Wait a minute or two for the text to stop scrolling and the installation to complete.

Step 6: Run the Application
Windows: Type python camt_gui.py and press Enter.

Mac: Type python3 camt_gui.py and press Enter.

Note for the first launch: The program needs a specific English language dictionary (en_core_web_sm) to work. If it doesn't see it, the terminal will say "Spacy model not found. Attempting simple download..." and will automatically download it for you.

After a brief pause, the application window will pop up on your screen, and you are ready to generate your text!
