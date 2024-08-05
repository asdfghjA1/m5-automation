import express from 'express';
import fetch from 'node-fetch';

const app = express()
const port = 3000

import aiRoutes from './aireddit.js'; // Import the router
app.use(express.json())

app.get('/ogreddit' , (req , res)=>{
    res.send('Hello world this is the ogreddit shit that i scraped')
})


// Define your credentials and userAgent
const clientId = '_T_ahf1IvUYj1HLt41zP2g'; // Your clientId
const clientSecret = 'QWf1lXvjHf3eib9lOQIku_X3GDv5dw'; // Your clientSecret
const userAgent = 'godscraper:1.0 (by /u/Famous_Space_7667)'; // Your userAgent

app.use('/ai', aiRoutes);

// Example endpoint using Reddit API
app.get('/reddit-top-posts', async (req, res) => {
  try {
    // Step 1: Get access token
    const tokenResponse = await fetch('https://www.reddit.com/api/v1/access_token', {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${Buffer.from(`${clientId}:${clientSecret}`).toString('base64')}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: 'grant_type=client_credentials'
    });

    if (!tokenResponse.ok) {
      throw new Error('Failed to fetch access token');
    }

    const tokenData = await tokenResponse.json();
    const accessToken = tokenData.access_token;

    // Step 2: Fetch top posts
    const postsResponse = await fetch('https://www.reddit.com/r/wallstreetbets/top/.json?limit=10', {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'User-Agent': userAgent
      }
    });

    if (!postsResponse.ok) {
      throw new Error('Failed to fetch posts');
    }

    const postsData = await postsResponse.json();
    res.json(postsData);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'An error occurred while fetching top posts' });
  }
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
