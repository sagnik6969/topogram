import { useRef, useEffect } from "react";
import { Transformer } from "react-konva";
import type Konva from "konva";
import type { Shape } from "@/store/slices/editorSlice";
import {
  CircleShape,
  RectangleShape,
  LineShape,
  EllipseShape,
  TextShape,
} from "./ShapeRenderer";

interface SelectableShapeProps {
  shape: Shape;
  isSelected: boolean;
  onSelect: () => void;
  onDragEnd: (e: any) => void;
  onTransformEnd: (e: any) => void;
}

export function SelectableShape({
  shape,
  isSelected,
  onSelect,
  onDragEnd,
  onTransformEnd,
}: SelectableShapeProps) {
  const shapeRef = useRef<any>(null);
  const transformerRef = useRef<Konva.Transformer>(null);

  useEffect(() => {
    if (isSelected && transformerRef.current && shapeRef.current) {
      // Attach transformer to the selected shape
      transformerRef.current.nodes([shapeRef.current]);
      transformerRef.current.getLayer()?.batchDraw();
    }
  }, [isSelected]);

  const handleTransformEnd = (e: any) => {
    const node = shapeRef.current;
    if (!node) return;

    onTransformEnd(e);
  };

  const shapeProps = {
    shape,
    onDragEnd,
    onClick: onSelect,
    isSelected,
  };

  const renderShape = () => {
    switch (shape.type) {
      case "circle":
        return <CircleShape ref={shapeRef} {...shapeProps} />;
      case "rectangle":
        return <RectangleShape ref={shapeRef} {...shapeProps} />;
      case "line":
        return <LineShape ref={shapeRef} {...shapeProps} />;
      case "ellipse":
        return <EllipseShape ref={shapeRef} {...shapeProps} />;
      case "text":
        return <TextShape ref={shapeRef} {...shapeProps} />;
      default:
        return null;
    }
  };

  return (
    <>
      {renderShape()}
      {isSelected && (
        <Transformer
          ref={transformerRef}
          onTransformEnd={handleTransformEnd}
          boundBoxFunc={(oldBox, newBox) => {
            // Limit resize to prevent shapes from becoming too small
            if (newBox.width < 5 || newBox.height < 5) {
              return oldBox;
            }
            return newBox;
          }}
          enabledAnchors={
            shape.type === "text"
              ? ["top-left", "top-right", "bottom-left", "bottom-right"]
              : [
                  "top-left",
                  "top-center",
                  "top-right",
                  "middle-right",
                  "middle-left",
                  "bottom-left",
                  "bottom-center",
                  "bottom-right",
                ]
          }
          rotateEnabled={true}
        />
      )}
    </>
  );
}
