import { Router } from "express";
import {
  convertToJSON,
  renderGraph,
} from "../controllers/diagramController.js";

const router = Router();

router.post("/convert", convertToJSON);
router.post("/render_graph", renderGraph);
export default router;
