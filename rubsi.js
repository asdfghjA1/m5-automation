const puppeteer = require('puppeteer');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const fs = require('fs');
const csv = require('csv-parser');
const { exec } = require('child_process');
const path = require('path');

// Function to convert view count text to a number
const parseViewCount = (viewsText) => {
  if (viewsText.includes('M')) {
    return parseFloat(viewsText.replace('M', '')) * 1_000_000;
  } else if (viewsText.includes('K')) {
    return parseFloat(viewsText.replace('K', '')) * 1_000;
  } else {
    return parseInt(viewsText.replace(/,/g, ''), 10);
  }
};

const scrapeChannelShorts = async (browser, channelLink) => {
  const page = await browser.newPage();
  const shortsLink = channelLink.includes('/shorts') ? channelLink : `${channelLink}/shorts`;

  try {
    await page.goto(shortsLink, { waitUntil: 'networkidle2' });

    // Scroll the page to load all shorts
    await page.evaluate(async () => {
      await new Promise(resolve => {
        const scroll = setInterval(() => {
          window.scrollBy(0, 1000);
          if (window.innerHeight + window.scrollY >= document.body.scrollHeight) {
            clearInterval(scroll);
            resolve();
          }
        }, 1000);
      });
    });

    // Extract video data
    const videoData = await page.evaluate(() => {
      const videos = Array.from(document.querySelectorAll('ytd-rich-item-renderer'));
      return videos.map(video => {
        const titleElement = video.querySelector('#video-title');
        const linkElement = video.querySelector('a#thumbnail');
        const viewsElement = video.querySelector('.inline-metadata-item.style-scope.ytd-video-meta-block');

        const viewsText = viewsElement ? viewsElement.textContent.trim() : '0 views';
        return {
          title: titleElement ? titleElement.textContent.trim() : 'No title',
          link: linkElement ? linkElement.href : 'No link',
          views: viewsText
        };
      });
    });

    return videoData.map(video => ({
      ...video,
      views: parseViewCount(video.views)
    }));
  } catch (error) {
    console.error(`Failed to scrape ${channelLink}:`, error);
    return [];
  } finally {
    await page.close();
  }
};

// Function to download a video and audio using yt-dlp and merge them
const downloadVideo = (url, filePath) => {
  return new Promise((resolve, reject) => {
    // Command to download both video and audio and merge them
    const command = `yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 ${url} -o ${filePath}`;
    exec(command, (error, stdout, stderr) => {
      if (error) {
        reject(`Error: ${stderr}`);
      } else {
        console.log(`Downloaded video to ${filePath}`);
        resolve(filePath);
      }
    });
  });
};

// Function to print top 3 links and download the videos
const printAndDownloadTop3Links = async () => {
  const results = [];

  fs.createReadStream('video_data.csv')
    .pipe(csv())
    .on('data', (data) => results.push(data))
    .on('end', async () => {
      // Sort the results by views in descending order
      results.sort((a, b) => parseFloat(b.Views) - parseFloat(a.Views));
      
      // Get the top 3 items
      const top3 = results.slice(0, 3);
      const top3Links = top3.map(item => item.Link);

      // Print the top 3 links
      console.log('Top 3 video links:');
      top3Links.forEach(link => console.log(link));

      // Ensure the /videos directory exists
      const videoDir = path.join(__dirname, 'videos');
      if (!fs.existsSync(videoDir)) {
        fs.mkdirSync(videoDir);
      }

      // Download the top 3 videos
      for (const [index, link] of top3Links.entries()) {
        const filePath = path.join(videoDir, `video${index + 1}.mp4`);
        try {
          await downloadVideo(link, filePath);
        } catch (error) {
          console.error(`Failed to download video from ${link}: ${error}`);
        }
      }
    });
};

const main = async () => {
  const browser = await puppeteer.launch({ headless: true });
  const allVideoData = [];

  // Read channel links from channels.txt
  const channelLinks = fs.readFileSync('channels.txt', 'utf-8').split('\n').filter(Boolean);

  for (const channelLink of channelLinks) {
    console.log(`Scraping channel: ${channelLink}`);
    const videoData = await scrapeChannelShorts(browser, channelLink);
    allVideoData.push(...videoData);

    console.log('Extracted Data:', videoData);
  }

  await browser.close();

  if (allVideoData.length === 0) {
    console.error('No video data found.');
    return;
  }

  // Sort all video data by views (highest to lowest)
  allVideoData.sort((a, b) => b.views - a.views);

  // Define CSV writer
  const csvWriter = createCsvWriter({
    path: 'video_data.csv',
    header: [
      { id: 'title', title: 'Title' },
      { id: 'link', title: 'Link' },
      { id: 'views', title: 'Views' }
    ]
  });

  // Write data to CSV
  await csvWriter.writeRecords(allVideoData);
  console.log('CSV file was written successfully');

  // Function to print top 3 links and download the top 3 videos
  await printAndDownloadTop3Links();
};

main().catch(console.error);
