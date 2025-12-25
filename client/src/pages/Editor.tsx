import Menubar from "@/components/Menubar";
import { useEffect } from "react";
import { Stage, Layer } from "react-konva";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { addShape, updateShape, setCanvasSize, selectShape } from "@/store/slices/editorSlice";
import { SelectableShape } from "@/components/shapes/SelectableShape";

function Editor() {
  const dispatch = useAppDispatch();
  const shapes = useAppSelector((state) => state.editor.shapes);
  const selectedShapeId = useAppSelector((state) => state.editor.selectedShapeId);
  const canvasWidth = useAppSelector((state) => state.editor.canvasWidth);
  const canvasHeight = useAppSelector((state) => state.editor.canvasHeight);

  // Initialize with sample shapes if no shapes exist
  useEffect(() => {
    if (shapes.length === 0) {
      // Add a circle
      dispatch(addShape({
        id: 'circle-1',
        type: 'circle',
        x: 100,
        y: 100,
        radius: 40,
        fill: 'orange',
        stroke: '#ff6b00',
        strokeWidth: 2,
      }));

      // Add a rectangle
      dispatch(addShape({
        id: 'rect-1',
        type: 'rectangle',
        x: 250,
        y: 80,
        width: 120,
        height: 80,
        fill: '#4CAF50',
        stroke: '#2E7D32',
        strokeWidth: 2,
      }));

      // Add a line
      dispatch(addShape({
        id: 'line-1',
        type: 'line',
        x: 450,
        y: 100,
        points: [0, 0, 100, 0, 100, 50, 0, 50],
        stroke: '#2196F3',
        strokeWidth: 3,
      }));

      // Add an ellipse
      dispatch(addShape({
        id: 'ellipse-1',
        type: 'ellipse',
        x: 150,
        y: 280,
        width: 140,
        height: 80,
        fill: '#9C27B0',
        stroke: '#6A1B9A',
        strokeWidth: 2,
      }));

      // Add text
      dispatch(addShape({
        id: 'text-1',
        type: 'text',
        x: 350,
        y: 250,
        text: 'Hello Diagram!',
        fontSize: 24,
        fontFamily: 'Arial',
        fill: '#E91E63',
      }));
    }
  }, [dispatch, shapes.length]);

  // Update canvas size on window resize
  useEffect(() => {
    const handleResize = () => {
      dispatch(setCanvasSize({
        width: window.innerWidth,
        height: window.innerHeight,
      }));
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [dispatch]);

  const handleDragEnd = (shapeId: string) => (e: any) => {
    dispatch(updateShape({
      id: shapeId,
      updates: {
        x: e.target.x(),
        y: e.target.y(),
      },
    }));
  };

  const handleTransformEnd = (shapeId: string) => (e: any) => {
    const node = e.target;
    const shape = shapes.find(s => s.id === shapeId);
    if (!shape) return;

    const updates: any = {
      x: node.x(),
      y: node.y(),
      rotation: node.rotation(),
    };

    // Update dimensions based on shape type
    if (shape.type === 'circle') {
      updates.radius = Math.max(5, node.width() / 2);
    } else if (shape.type === 'rectangle') {
      updates.width = Math.max(5, node.width());
      updates.height = Math.max(5, node.height());
    } else if (shape.type === 'ellipse') {
      updates.width = Math.max(5, node.width());
      updates.height = Math.max(5, node.height());
    } else if (shape.type === 'text') {
      updates.fontSize = Math.max(8, node.fontSize() * e.scaleY);
    }

    dispatch(updateShape({
      id: shapeId,
      updates,
    }));
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


