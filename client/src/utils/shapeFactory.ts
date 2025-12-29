import type { Shape } from "@/store/slices/editorSlice";

/**
 * Utility functions to create shapes with default values
 */

export function createCircle(
  id: string,
  x: number,
  y: number,
  options?: Partial<Shape>
): Shape {
  return {
    id,
    type: "circle",
    x,
    y,
    radius: 40,
    fill: "#FF6B6B",
    stroke: "#C92A2A",
    strokeWidth: 2,
    ...options,
  };
}

export function createRectangle(
  id: string,
  x: number,
  y: number,
  options?: Partial<Shape>
): Shape {
  return {
    id,
    type: "rectangle",
    x,
    y,
    width: 100,
    height: 80,
    fill: "#4ECDC4",
    stroke: "#0D7377",
    strokeWidth: 2,
    ...options,
  };
}

export function createLine(
  id: string,
  x: number,
  y: number,
  points: number[],
  options?: Partial<Shape>
): Shape {
  return {
    id,
    type: "line",
    x,
    y,
    points,
    stroke: "#2196F3",
    strokeWidth: 2,
    ...options,
  };
}

export function createEllipse(
  id: string,
  x: number,
  y: number,
  options?: Partial<Shape>
): Shape {
  return {
    id,
    type: "ellipse",
    x,
    y,
    width: 120,
    height: 80,
    fill: "#9C27B0",
    stroke: "#6A1B9A",
    strokeWidth: 2,
    ...options,
  };
}

export function createText(
  id: string,
  x: number,
  y: number,
  text: string,
  options?: Partial<Shape>
): Shape {
  return {
    id,
    type: "text",
    x,
    y,
    text,
    fontSize: 16,
    fontFamily: "Arial",
    fill: "#000000",
    ...options,
  };
}

/**
 * Generate a unique ID for shapes
 */
export function generateShapeId(type: Shape["type"]): string {
  return `${type}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Color presets for quick shape creation
 */
export const COLOR_PRESETS = {
  red: { fill: "#FF6B6B", stroke: "#C92A2A" },
  blue: { fill: "#4DABF7", stroke: "#1971C2" },
  green: { fill: "#51CF66", stroke: "#2F9E44" },
  yellow: { fill: "#FFD43B", stroke: "#F59F00" },
  purple: { fill: "#CC5DE8", stroke: "#9C36B5" },
  orange: { fill: "#FF922B", stroke: "#E8590C" },
  teal: { fill: "#20C997", stroke: "#0CA678" },
  pink: { fill: "#F06595", stroke: "#C2255C" },
  gray: { fill: "#ADB5BD", stroke: "#495057" },
  slate: { fill: "#F1F5F9", stroke: "#64748B" },
} as const;
