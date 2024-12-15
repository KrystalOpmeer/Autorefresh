# Autorefresh

This project automates web interactions using Selenium, providing features for interactive execution control such as pausing, resuming, and graceful termination. The script is designed for tasks involving button clicks and dynamic user input during automation.

Features

Automates clicking a Course button and a Go Back button.

Execution control via:

'p' key: Toggle pause/resume.

'q' key: Starts a 2-minute countdown to stop the script.

Multi-threaded monitoring for seamless performance.

Installation

Clone this repository:

git clone https://github.com/yourusername/selenium-clickmaster.git
cd selenium-clickmaster

Install the required Python packages:

pip install selenium keyboard

Download the appropriate WebDriver for your browser:

ChromeDriver

Usage

Update the XPath values in the script:

Replace the coursebutton XPath:

'//*[@id="pageDivId2"]/div/table/tbody/tr[4]/td[8]/button'

Replace the gobackbutton XPath:

'//*[@id="regForm"]/div[2]/table/thead/tr[16]/td/div/button[2]'

Run the script:

python selenium_script.py

Follow these steps during execution:

Start the browser and log in or navigate to the desired page.

Press Enter in the terminal after reaching the desired page.

Use the following controls:

'p': Pause or resume execution.

Mouse click: Automatically pauses execution.

'q': Initiates a 2-minute countdown to terminate the script.

Requirements

Python 3.7 or higher

Selenium

keyboard module (install via pip)
