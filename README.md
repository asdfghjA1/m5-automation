# Stream Clips Scraper

## Overview

This project is a web scraping script designed to fetch data from [Streams Charts](https://streamscharts.com/clips) every 12 hours. The script identifies and downloads the top 3 clips each time. The downloaded clips are saved locally for further use or analysis.

## Technologies Used

- **Puppeteer**: For web scraping.
- **yt-dlp**: For downloading video clips.

## Requirements

Ensure you have the following software installed on your system:

- Node.js (version 14 or above)
- yt-dlp
- npm

## Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/stream-clips-scraper.git
   cd stream-clips-scraper
npm install
sudo apt update
sudo apt install yt-dlp
## Usage
Run the script:
To run the script manually, use:
node scraper.js
