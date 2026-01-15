import { Request, Response } from "express";
import { parseMermaid, renderJson } from "@rendermaid/core";
import ELK from "elkjs/lib/elk.bundled.js";

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

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const elk = new (ELK as any)();
    const renderedGraph = await elk.layout(jsonGraph);
    res.json(renderedGraph);
  } catch (error) {
    console.error("Error rendering graph from JSON:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};

export const convertToJSON = (req: Request, res: Response): void => {
  try {
    const { diagram } = req.body;

    if (!diagram) {
      res.status(400).json({ error: "Diagram content is required" });
      return;
    }

    // Parse the diagram
    const parseResult = parseMermaid(diagram);

    if (!parseResult.success) {
      res.status(400).json({
        error: "Failed to parse mermaid diagram",
        details: parseResult,
      });
      return;
    }

    // Render to JSON
    const jsonResult = renderJson(parseResult.data, {
      pretty: true,
      includeMetadata: true,
    });

    if (jsonResult.success) {
      try {
        const parsedData =
          typeof jsonResult.data === "string"
            ? JSON.parse(jsonResult.data)
            : jsonResult.data;
        res.json(parsedData);
      } catch (e) {
        res.json({ status: "success", result: jsonResult.data });
      }
    } else {
      res.status(500).json({
        error: "Failed to render JSON",
        details: jsonResult,
      });
    }
  } catch (error) {
    console.error("Error converting mermaid to JSON:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};
