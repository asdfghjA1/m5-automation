// routes/aiRoutes.js
import express from 'express';
const router = express.Router(); // Create a new router instance

// Route for /ai/reddit
router.get('/reddit', (req, res) => {
    res.send('Congratulations, you have cum inside AI / Reddit shit bruh');
});

export default router;
