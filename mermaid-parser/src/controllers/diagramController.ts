import { Request, Response } from 'express';
// @ts-ignore
import { parseMermaid, renderJson } from "@rendermaid/core";

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
                details: parseResult 
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
                const parsedData = typeof jsonResult.data === 'string' 
                    ? JSON.parse(jsonResult.data) 
                    : jsonResult.data;
                res.json(parsedData);
            } catch (e) {
                 res.json(jsonResult.data);
            }
        } else {
             res.status(500).json({ 
                error: "Failed to render JSON", 
                details: jsonResult 
            });
        }

    } catch (error) {
        console.error("Error converting mermaid to JSON:", error);
        res.status(500).json({ error: "Internal server error" });
    }
};
