import { Router } from "express";
import {
  convertMermaidToJSON,
  renderGraph,
} from "../controllers/diagramController.js";

const router = Router();

router.post("/convert-mermaid-to-json", convertMermaidToJSON);
router.post("/render-graph", renderGraph);

export default router;
