const express = require("express");
const app = express();
app.use(express.json());


app.get("/", (req, res) => {
  res.json({ message: "Riverlight+ backend is running" });
});


app.post("/api/getStreamUrl", (req, res) => {
  const { contentId } = req.body;

  
  res.json({
    streamUrl: `https://your-video-host.com/${contentId}`
  });
});
app.get("/ping", (req, res) => {
  res.json({ status: "ok", message: "Riverlight+ backend is alive" });
});
app.listen(port, () => {
  console.log(`Backend running on port ${port}`);
});
app.listen(process.env.PORT || 8080, () => {
  console.log("Backend running");
});
