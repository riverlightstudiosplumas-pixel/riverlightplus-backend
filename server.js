const express = require("express");
const app = express();
app.use(express.json());

// Test endpoint
app.get("/", (req, res) => {
  res.json({ message: "Riverlight+ backend is running" });
});

// Example endpoint for stream URLs
app.post("/api/getStreamUrl", (req, res) => {
  const { contentId } = req.body;

  // Placeholder logic — later you’ll replace this with real logic
  res.json({
    streamUrl: `https://your-video-host.com/${contentId}`
  });
});

app.listen(process.env.PORT || 8080, () => {
  console.log("Backend running");
});
