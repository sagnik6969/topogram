import { Circle, Rect, Line, Ellipse, Text } from "react-konva";
import type { Shape } from "@/store/slices/editorSlice";
import { forwardRef } from "react";
import type Konva from "konva";

interface ShapeRendererProps {
  shape: Shape;
  onDragEnd: (e: any) => void;
  onClick?: (e: any) => void;
  isSelected?: boolean;
}

export const CircleShape = forwardRef<Konva.Circle, ShapeRendererProps>(
  ({ shape, onDragEnd, onClick, isSelected }, ref) => {
    return (
      <Circle
        ref={ref}
        x={shape.x}
        y={shape.y}
        radius={shape.radius}
        fill={shape.fill}
        stroke={isSelected ? "#0066FF" : shape.stroke}
        strokeWidth={isSelected ? 3 : shape.strokeWidth}
        rotation={shape.rotation}
        opacity={shape.opacity}
        draggable
        onDragEnd={onDragEnd}
        onClick={onClick}
        onTap={onClick}
        strokeScaleEnabled={false}
      />
    );
  }
);
CircleShape.displayName = "CircleShape";

export const RectangleShape = forwardRef<Konva.Rect, ShapeRendererProps>(
  ({ shape, onDragEnd, onClick, isSelected }, ref) => {
    return (
      <Rect
        ref={ref}
        x={shape.x}
        y={shape.y}
        width={shape.width}
        height={shape.height}
        fill={shape.fill}
        stroke={isSelected ? "#0066FF" : shape.stroke}
        strokeWidth={isSelected ? 3 : shape.strokeWidth}
        rotation={shape.rotation}
        opacity={shape.opacity}
        draggable
        onDragEnd={onDragEnd}
        onClick={onClick}
        onTap={onClick}
        strokeScaleEnabled={false}
      />
    );
  }
);
RectangleShape.displayName = "RectangleShape";

export const LineShape = forwardRef<Konva.Line, ShapeRendererProps>(
  ({ shape, onDragEnd, onClick, isSelected }, ref) => {
    return (
      <Line
        ref={ref}
        x={shape.x}
        y={shape.y}
        points={shape.points}
        stroke={isSelected ? "#0066FF" : shape.stroke || "#000"}
        strokeWidth={isSelected ? 4 : shape.strokeWidth || 2}
        rotation={shape.rotation}
        opacity={shape.opacity}
        draggable
        onDragEnd={onDragEnd}
        onClick={onClick}
        onTap={onClick}
        strokeScaleEnabled={false}
      />
    );
  }
);
LineShape.displayName = "LineShape";

export const EllipseShape = forwardRef<Konva.Ellipse, ShapeRendererProps>(
  ({ shape, onDragEnd, onClick, isSelected }, ref) => {
    return (
      <Ellipse
        ref={ref}
        x={shape.x}
        y={shape.y}
        radiusX={shape.radiusX!}
        radiusY={shape.radiusY!}
        fill={shape.fill}
        stroke={isSelected ? "#0066FF" : shape.stroke}
        strokeWidth={isSelected ? 3 : shape.strokeWidth}
        rotation={shape.rotation}
        opacity={shape.opacity}
        draggable
        onDragEnd={onDragEnd}
        onClick={onClick}
        onTap={onClick}
        strokeScaleEnabled={false}
      />
    );
  }
);
EllipseShape.displayName = "EllipseShape";

export const TextShape = forwardRef<Konva.Text, ShapeRendererProps>(
  ({ shape, onDragEnd, onClick, isSelected }, ref) => {
    return (
      <Text
        ref={ref}
        x={shape.x}
        y={shape.y}
        text={shape.text || "Text"}
        fontSize={shape.fontSize || 16}
        fontFamily={shape.fontFamily || "Arial"}
        fill={shape.fill || "#000"}
        stroke={isSelected ? "#0066FF" : undefined}
        strokeWidth={isSelected ? 1 : 0}
        rotation={shape.rotation}
        opacity={shape.opacity}
        draggable
        onDragEnd={onDragEnd}
        onClick={onClick}
        onTap={onClick}
        strokeScaleEnabled={false}
      />
    );
  }
);
TextShape.displayName = "TextShape";
