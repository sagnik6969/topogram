import React, { useMemo } from 'react';
import { Arrow } from 'react-konva';
import { type Shape, type Connection as ConnectionType } from '@/store/slices/editorSlice';

interface ConnectionProps {
  connection: ConnectionType;
  shapes: Shape[];
}

interface Point {
  x: number;
  y: number;
}

interface Anchor {
  x: number;
  y: number;
  side: 'top' | 'right' | 'bottom' | 'left';
}

const getShapeBounds = (shape: Shape) => {
  if (shape.type === 'circle' && shape.radius) {
    return {
      x: shape.x - shape.radius,
      y: shape.y - shape.radius,
      width: shape.radius * 2,
      height: shape.radius * 2,
    };
  }
  if (shape.type === 'ellipse' && shape.radiusX && shape.radiusY) {
    return {
      x: shape.x - shape.radiusX,
      y: shape.y - shape.radiusY,
      width: shape.radiusX * 2,
      height: shape.radiusY * 2,
    };
  }
  return {
    x: shape.x,
    y: shape.y,
    width: shape.width || 0,
    height: shape.height || 0,
  };
};

const getAnchors = (shape: Shape): Anchor[] => {
  const bounds = getShapeBounds(shape);
  const { x, y, width, height } = bounds;
  
  return [
    { x: x + width / 2, y: y, side: 'top' },           // Top
    { x: x + width, y: y + height / 2, side: 'right' },// Right
    { x: x + width / 2, y: y + height, side: 'bottom' },// Bottom
    { x: x, y: y + height / 2, side: 'left' },         // Left
  ];
};

const getDistance = (p1: Point, p2: Point) => {
  return Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
};

const getControlPoint = (anchor: Anchor): Point => {
    const offset = 50; // Curve intensity
    switch (anchor.side) {
        case 'top': return { x: anchor.x, y: anchor.y - offset };
        case 'bottom': return { x: anchor.x, y: anchor.y + offset };
        case 'left': return { x: anchor.x - offset, y: anchor.y };
        case 'right': return { x: anchor.x + offset, y: anchor.y };
        default: return { x: anchor.x, y: anchor.y };
    }
}

export const Connection: React.FC<ConnectionProps> = ({ connection, shapes }) => {
  const sourceShape = shapes.find(s => s.id === connection.from);
  const targetShape = shapes.find(s => s.id === connection.to);

  const points = useMemo(() => {
    if (!sourceShape || !targetShape) return [];

    const sourceAnchors = getAnchors(sourceShape);
    const targetAnchors = getAnchors(targetShape);

    // Find pair with minimum distance
    let minDistance = Infinity;
    let bestPair = { start: sourceAnchors[0], end: targetAnchors[0] };

    for (const start of sourceAnchors) {
      for (const end of targetAnchors) {
        const dist = getDistance(start, end);
        if (dist < minDistance) {
          minDistance = dist;
          bestPair = { start, end };
        }
      }
    }

    const { start, end } = bestPair;
    const cp1 = getControlPoint(start);
    const cp2 = getControlPoint(end);

    // Return flattened array [sx, sy, cp1x, cp1y, cp2x, cp2y, ex, ey] for bezier arrow?
    // React-konva Arrow uses `points` array. If pointerAtBeginning is false, 
    // it draws lines. For bezier, we might need a custom Shape or Path, 
    // OR just use Konva.Arrow with 'bezier' property if supported? 
    // Konva Arrow supports `tension`. But to have FULL control like eraser.io, 
    // we manually compute points for a bezier curve?
    // Actually, Konva has a `bezier` boolean property for Line/Arrow but it requires exactly 4 pairs of numbers if using cubic? 
    // Docs say: "If you want to draw quadratic or cubic bezier, you should use `bezier: true` and pass points."
    
    return [start.x, start.y, cp1.x, cp1.y, cp2.x, cp2.y, end.x, end.y];
  }, [sourceShape, targetShape]);

  if (!sourceShape || !targetShape) return null;

  return (
    <Arrow
      points={points}
      stroke="#cbd5e1" // slate-300
      strokeWidth={2}
      fill="#cbd5e1"
      bezier={true}
      pointerWidth={10}
      pointerLength={10}
    />
  );
};
