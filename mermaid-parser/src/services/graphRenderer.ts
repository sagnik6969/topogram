import ELK from "elkjs/lib/elk.bundled.js";

export const renderGraphUsingELK = async (jsonGraph: any): Promise<any> => {
  const elk = new (ELK as any)();
  const renderedGraph = await elk.layout(jsonGraph);
  return renderedGraph;
};
