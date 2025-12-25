import Menubar from "@/components/Menubar";
import { useEffect } from "react";
import { Stage, Layer, Circle } from "react-konva";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { addShape, updateShape, setCanvasSize } from "@/store/slices/editorSlice";

function Editor() {
  const dispatch = useAppDispatch();
  const shapes = useAppSelector((state) => state.editor.shapes);
  const canvasWidth = useAppSelector((state) => state.editor.canvasWidth);
  const canvasHeight = useAppSelector((state) => state.editor.canvasHeight);

  // Initialize with a sample circle if no shapes exist
  useEffect(() => {
    if (shapes.length === 0) {
      dispatch(addShape({
        id: 'circle-1',
        type: 'circle',
        x: 100,
        y: 100,
        radius: 40,
        fill: 'orange',
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

  return (
    <div>
      <Menubar />
      <Stage width={canvasWidth} height={canvasHeight}>
        <Layer>
          {shapes.map((shape) => {
            if (shape.type === 'circle') {
              return (
                <Circle
                  key={shape.id}
                  x={shape.x}
                  y={shape.y}
                  radius={shape.radius || 40}
                  fill={shape.fill || 'orange'}
                  draggable
                  onDragEnd={(e: any) => {
                    dispatch(updateShape({
                      id: shape.id,
                      updates: {
                        x: e.target.x(),
                        y: e.target.y(),
                      },
                    }));
                  }}
                />
              );
            }
            return null;
          })}
        </Layer>
      </Stage>
    </div>
  );
}

export default Editor;

