import express from "express";
import diagramRoutes from "./routes/diagramRoutes.js";

const app = express();

app.use(express.json());

// Routes
app.use("/apis/v1/mermaid", diagramRoutes);

// Health check
app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

export default app;
