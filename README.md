# Wheel of Fortune Winning Spin ID Tracker

Wheel of Fortune is a game show on television weeknights at 7pm EST. Each night the show chooses a random audience member's Spin ID from the Wheel Watcher's Club (register for free at https://www.wheeloffortune.com/join/benefits) to win $10,000. However, if your Spin ID is ever selected, you only have 24 hours to claim your prize or else you will receive nothing!

I built this program to automate the manual process of checking your Spin ID each night because I would never want to miss out on the $10,000 cash prize!

This program scrapes nightly winning Spin ID's from wheeloffortunesolutions.com, logs them to a CSV (for historical tracking purposes), and emails users if they win the $10,000 prize. 

## Features
- Scrapes Spin IDs with Python (`requests`, `BeautifulSoup`).
- Logs winners (or "No winner tonight") to CSV.
- Emails matches via Gmail (`smtplib`).
- Runs weeknights at 10pm EST (`schedule`).

## Setup
1. Clone: `git clone https://github.com/mattdimauro2/wheel-of-fortune-scraper`
2. Install: `pip install requests beautifulsoup4 schedule`
3. Add your Spin ID/email to `tracked_spin_ids`.
4. Set `EMAIL_PASS` in your OS with a Gmail app password.
5. Run: `python wheel_scraper.py`

## Why?
I wanted a hands-off way to catch Wheel wins—turned a daily chore into a script.

Built by Matt DiMauro