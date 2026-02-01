import { parseMermaid, renderJson } from "@rendermaid/core";
import { AppError } from "../utils/AppError.js";

export const convertMermaidToJson = (mermaidString: string): any => {
  const parseResult = parseMermaid(mermaidString);

  if (!parseResult.success) {
    throw new AppError("Failed to parse mermaid diagram", 400);
  }

  // Render to JSON
  const jsonResult = renderJson(parseResult.data, {
    pretty: true,
    includeMetadata: true,
  });

  if (jsonResult.success) {
    return JSON.parse(jsonResult.data);
  } else {
    throw new AppError(
      "Failed to render generated JSON graph",
      500,
      jsonResult
    );
  }
};
