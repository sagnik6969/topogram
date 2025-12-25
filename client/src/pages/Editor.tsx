import Menubar from "@/components/Menubar";
import { useState } from "react";
import { Stage, Layer, Circle } from "react-konva";

function Editor() {
  const [pos, setPos] = useState({ x: 100, y: 100 });

  return (
    <div>
      <Menubar />
      <Stage width={window.innerWidth} height={window.innerHeight}>
        <Layer>
          <Circle
            x={pos.x}
            y={pos.y}
            radius={40}
            fill="orange"
            draggable
            onDragEnd={(e: any) =>
              setPos({
                x: e.target.x(),
                y: e.target.y(),
              })
            }
          />
        </Layer>
        {/* <Layer>
          
        </Layer> */}
      </Stage>
    </div>
  );
}

export default Editor;
