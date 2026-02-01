import { Request, Response } from "express";
import { AppError } from "../utils/AppError.js";
import { renderGraphUsingELK } from "../services/graphRenderer.js";
import { convertMermaidToJson } from "../services/mermaidToJsonConverter.js";

export const renderGraph = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    if (!req.body || !req.body.jsonGraph) {
      res.status(400).json({ error: "jsonGraph field is required" });
      return;
    }

    const { jsonGraph } = req.body;

    const renderedGraph = await renderGraphUsingELK(jsonGraph);

    res.status(200).json(renderedGraph);
  } catch (error) {
    if (error instanceof AppError) {
      res
        .status(error.statusCode)
        .json({ error: error.message, details: error.details });
    }
    console.error("Error rendering graph from JSON:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};

export const convertMermaidToJSON = (req: Request, res: Response): void => {
  try {
    const { diagram } = req.body;

    if (!diagram) {
      res.status(400).json({ error: "Diagram content is required" });
      return;
    }

    // Parse the diagram
    const parseResult = convertMermaidToJson(diagram);

    res.status(200).json(parseResult);
  } catch (error) {
    if (error instanceof AppError) {
      res
        .status(error.statusCode)
        .json({ error: error.message, details: error.details });
    }
    console.error("Error converting mermaid to JSON:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};
