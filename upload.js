const fs = require('fs');
const path = require('path');
const mega = require('megajs');

// Mega account credentials
const email = 'dev.m5.team@gmail.com';
const password = '#BigBootyDonnyCake27';

// Initialize Mega storage
const storage = mega({ email, password }, (error) => {
    if (error) {
        console.error('Login failed:', error);
        return;
    }

    console.log('Login successful!');

    // Specify the folder to upload
    const folderPath = path.join(__dirname, 'videos');
    const uploadsFolderName = 'uploads';
    
    // Helper function to upload a single file
    const uploadFile = (filePath, fileSize) => {
        return new Promise((resolve, reject) => {
            const file = path.basename(filePath);
            const uploadsFolder = storage.root.children.find(folder => folder.name === uploadsFolderName);

            const uploadStream = storage.upload({
                name: file,
                size: fileSize,
                allowUploadBuffering: true,
                target: uploadsFolder
            });

            fs.createReadStream(filePath).pipe(uploadStream);

            uploadStream.on('complete', () => {
                console.log(`Uploaded ${file} successfully!`);
                resolve();
            });

            uploadStream.on('error', (uploadError) => {
                console.error(`Failed to upload ${file}:`, uploadError);
                reject(uploadError);
            });
        });
    };

    // Read the folder and upload files
    fs.readdir(folderPath, async (err, files) => {
        if (err) {
            console.error('Failed to read the folder:', err);
            return;
        }

        // Filter files and get their paths and sizes
        const filePromises = files
            .filter(file => fs.statSync(path.join(folderPath, file)).isFile())
            .map(file => {
                const filePath = path.join(folderPath, file);
                const fileSize = fs.statSync(filePath).size;
                return uploadFile(filePath, fileSize);
            });

        try {
            await Promise.all(filePromises);
            console.log('All files uploaded successfully!');
        } catch (uploadError) {
            console.error('One or more files failed to upload.');
        } finally {
            process.exit(); // Exit the process
        }
    });
});
