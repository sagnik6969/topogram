import Menubar from "@/components/Menubar";
import { useEffect } from "react";
import { Stage, Layer } from "react-konva";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import {
  updateShape,
  setCanvasSize,
  selectShape,
} from "@/store/slices/editorSlice";
import { SelectableShape } from "@/components/shapes/SelectableShape";

function Editor() {
  const dispatch = useAppDispatch();
  const shapes = useAppSelector((state) => state.editor.shapes);
  const selectedShapeId = useAppSelector(
    (state) => state.editor.selectedShapeId
  );
  const canvasWidth = useAppSelector((state) => state.editor.canvasWidth);
  const canvasHeight = useAppSelector((state) => state.editor.canvasHeight);

  // Update canvas size on window resize
  useEffect(() => {
    const handleResize = () => {
      dispatch(
        setCanvasSize({
          width: window.innerWidth,
          height: window.innerHeight,
        })
      );
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [dispatch]);

  const handleDragEnd = (shapeId: string) => (e: any) => {
    dispatch(
      updateShape({
        id: shapeId,
        updates: {
          x: e.target.x(),
          y: e.target.y(),
        },
      })
    );
  };

  const handleTransformEnd = (shapeId: string) => (e: any) => {
    const node = e.target;
    const shape = shapes.find((s) => s.id === shapeId);
    if (!shape) return;

    const updates: any = {
      x: node.x(),
      y: node.y(),
      rotation: node.rotation(),
    };

    if (shape.type === "rectangle") {
      console.log(node);
      updates.width = node.width() * node.scaleX();
      updates.height = node.height() * node.scaleY();
    } else if (shape.type === "ellipse") {
      updates.radiusX = node.radiusX() * node.scaleX();
      updates.radiusY = node.radiusY() * node.scaleY();
    } else if (shape.type === "text") {
      updates.fontSize = node.fontSize() * node.scaleY();
    }

    node.scaleX(1);
    node.scaleY(1);

    dispatch(
      updateShape({
        id: shapeId,
        updates,
      })
    );
  };

  const handleSelect = (shapeId: string) => () => {
    dispatch(selectShape(shapeId));
  };

  const handleStageClick = (e: any) => {
    // Deselect when clicking on empty area
    if (e.target === e.target.getStage()) {
      dispatch(selectShape(null));
    }
  };

  return (
    <div>
      <Menubar />
      <Stage
        width={canvasWidth}
        height={canvasHeight}
        onClick={handleStageClick}
        onTap={handleStageClick}
      >
        <Layer>
          {shapes.map((shape) => (
            <SelectableShape
              key={shape.id}
              shape={shape}
              isSelected={shape.id === selectedShapeId}
              onSelect={handleSelect(shape.id)}
              onDragEnd={handleDragEnd(shape.id)}
              onTransformEnd={handleTransformEnd(shape.id)}
            />
          ))}
        </Layer>
      </Stage>
    </div>
  );
}

export default Editor;
