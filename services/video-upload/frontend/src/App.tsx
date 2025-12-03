import React, { useState } from 'react';
import { Container, Typography, Box, Button, CircularProgress, Alert } from '@mui/material';
import axios from 'axios';

function App() {
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
        const file = event.target.files[0];
        await uploadVideo(file);
    }
  };

  const uploadVideo = async (file: File) => {
      setUploading(true);
      setUploadStatus(null);
      const formData = new FormData();
      formData.append('video', file);

      try {
          const response = await axios.post('/api/videos/upload', formData, {
              headers: {
                  'Content-Type': 'multipart/form-data',
              },
          });
          setUploadStatus(`Upload successful! Video ID: ${response.data.video_id}`);
      } catch (error) {
          console.error('Error uploading video:', error);
          setUploadStatus('Upload failed. Please try again.');
      } finally {
          setUploading(false);
      }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Agile Video Metadata Generation
        </Typography>
        <Typography variant="body1" gutterBottom>
          Upload your video to automatically generate titles, synopsis, and thumbnails.
        </Typography>
        
        <Box sx={{ mt: 4, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
             <Button variant="contained" component="label" disabled={uploading}>
                {uploading ? 'Uploading...' : 'Upload Video'}
                <input type="file" hidden accept="video/*" onChange={handleFileChange} />
            </Button>
            {uploading && <CircularProgress />}
            {uploadStatus && (
                <Alert severity={uploadStatus.includes('failed') ? 'error' : 'success'}>
                    {uploadStatus}
                </Alert>
            )}
        </Box>
      </Box>
    </Container>
  );
}

export default App;
