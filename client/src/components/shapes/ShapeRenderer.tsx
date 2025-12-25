import { Circle, Rect, Line, Ellipse, Text } from "react-konva";
import type { Shape } from "@/store/slices/editorSlice";

interface ShapeRendererProps {
  shape: Shape;
  onDragEnd: (e: any) => void;
  onClick?: (e: any) => void;
}

export function CircleShape({ shape, onDragEnd, onClick }: ShapeRendererProps) {
  return (
    <Circle
      x={shape.x}
      y={shape.y}
      radius={shape.radius}
      fill={shape.fill}
      stroke={shape.stroke}
      strokeWidth={shape.strokeWidth}
      rotation={shape.rotation}
      opacity={shape.opacity}
      draggable
      onDragEnd={onDragEnd}
      onClick={onClick}
    />
  );
}

export function RectangleShape({ shape, onDragEnd, onClick }: ShapeRendererProps) {
  return (
    <Rect
      x={shape.x}
      y={shape.y}
      width={shape.width}
      height={shape.height}
      fill={shape.fill}
      stroke={shape.stroke}
      strokeWidth={shape.strokeWidth}
      rotation={shape.rotation}
      opacity={shape.opacity}
      draggable
      onDragEnd={onDragEnd}
      onClick={onClick}
    />
  );
}

export function LineShape({ shape, onDragEnd, onClick }: ShapeRendererProps) {
  return (
    <Line
      x={shape.x}
      y={shape.y}
      points={shape.points}
      stroke={shape.stroke || '#000'}
      strokeWidth={shape.strokeWidth || 2}
      rotation={shape.rotation}
      opacity={shape.opacity}
      draggable
      onDragEnd={onDragEnd}
      onClick={onClick}
    />
  );
}

export function EllipseShape({ shape, onDragEnd, onClick }: ShapeRendererProps) {
  return (
    <Ellipse
      x={shape.x}
      y={shape.y}
      radiusX={(shape.width || 100) / 2}
      radiusY={(shape.height || 60) / 2}
      fill={shape.fill}
      stroke={shape.stroke}
      strokeWidth={shape.strokeWidth}
      rotation={shape.rotation}
      opacity={shape.opacity}
      draggable
      onDragEnd={onDragEnd}
      onClick={onClick}
    />
  );
}

export function TextShape({ shape, onDragEnd, onClick }: ShapeRendererProps) {
  return (
    <Text
      x={shape.x}
      y={shape.y}
      text={shape.text || 'Text'}
      fontSize={shape.fontSize || 16}
      fontFamily={shape.fontFamily || 'Arial'}
      fill={shape.fill || '#000'}
      rotation={shape.rotation}
      opacity={shape.opacity}
      draggable
      onDragEnd={onDragEnd}
      onClick={onClick}
    />
  );
}

export function renderShape(
  shape: Shape,
  onDragEnd: (e: any) => void,
  onClick?: (e: any) => void
) {
  const props = { shape, onDragEnd, onClick };

  switch (shape.type) {
    case 'circle':
      return <CircleShape key={shape.id} {...props} />;
    case 'rectangle':
      return <RectangleShape key={shape.id} {...props} />;
    case 'line':
      return <LineShape key={shape.id} {...props} />;
    case 'ellipse':
      return <EllipseShape key={shape.id} {...props} />;
    case 'text':
      return <TextShape key={shape.id} {...props} />;
    default:
      return null;
  }
}
