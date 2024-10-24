const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');

const app = express();

// Enable CORS
app.use(cors());

const upload = multer({ dest: 'uploads/' });

app.use(express.static(path.join(__dirname, 'uploads')));

app.post('/upload', upload.single('file'), (req, res) => {
  // Process the image file here
  console.log(req.file);
  res.send({ message: 'File uploaded successfully!' });
});

app.listen(5001, () => {
  console.log('Server is running on port 5001');
});
