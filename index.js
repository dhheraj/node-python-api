const express = require("express");
const multer = require("multer");
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = 3000;

// Ensure uploads/ exists
if (!fs.existsSync("uploads")) fs.mkdirSync("uploads");

// Preserve image extensions for OpenCV to work
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "uploads/");
  },
  filename: function (req, file, cb) {
    const ext = path.extname(file.originalname);
    const name = `${Date.now()}-${Math.round(Math.random() * 1e9)}${ext}`;
    cb(null, name);
  },
});

const upload = multer({ storage: storage });

app.post("/upload-image", upload.single("image"), (req, res) => {
  const imagePath = req.file.path;

  const python = spawn("python", ["script.py", imagePath]);

  let output = "";
  let error = "";

  python.stdout.on("data", (data) => {
    output += data.toString();
  });

  python.stderr.on("data", (data) => {
    error += data.toString();
  });

  python.on("close", (code) => {
    // Clean up uploaded file
    fs.unlink(imagePath, () => {});

    if (code !== 0 || error) {
      return res.status(500).json({ error: error || "Python script failed" });
    }

    try {
      const result = JSON.parse(output);
      res.json(result);
    } catch (e) {
      res.status(500).json({ error: "Failed to parse Python output" });
    }
  });
});

app.listen(PORT, () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});
