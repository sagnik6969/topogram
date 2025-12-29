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
        draggable
        onDragEnd={onDragEnd}
        onClick={onClick}
        onTap={onClick}
        strokeScaleEnabled={false}
        {...shape}
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
        draggable
        onDragEnd={onDragEnd}
        onClick={onClick}
        onTap={onClick}
        strokeScaleEnabled={false}
        {...shape}
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
        draggable
        onDragEnd={onDragEnd}
        onClick={onClick}
        onTap={onClick}
        strokeScaleEnabled={false}
        {...shape}
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
        draggable
        onDragEnd={onDragEnd}
        onClick={onClick}
        onTap={onClick}
        strokeScaleEnabled={false}
        radiusX={shape.radiusX ?? 0}
        radiusY={shape.radiusY ?? 0}
        {...shape}
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
        draggable
        onDragEnd={onDragEnd}
        onClick={onClick}
        onTap={onClick}
        strokeScaleEnabled={false}
        {...shape}
      />
    );
  }
);
TextShape.displayName = "TextShape";
