import { useAppDispatch } from "@/store/hooks";
import { addShape } from "@/store/slices/editorSlice";
import {
  createCircle,
  createRectangle,
  createLine,
  createEllipse,
  createText,
  generateShapeId,
  COLOR_PRESETS,
} from "@/utils/shapeFactory";

export default function ShapeToolbar() {
  const dispatch = useAppDispatch();

  const addCircleShape = () => {
    const circle = createCircle(
      generateShapeId("circle"),
      Math.random() * 400 + 100,
      Math.random() * 300 + 100,
      {
        radius: 50,
        ...COLOR_PRESETS.blue,
      }
    );
    dispatch(addShape(circle));
  };

  const addRectangleShape = () => {
    const rectangle = createRectangle(
      generateShapeId("rectangle"),
      Math.random() * 400 + 100,
      Math.random() * 300 + 100,
      {
        width: 120,
        height: 80,
        ...COLOR_PRESETS.green,
      }
    );
    dispatch(addShape(rectangle));
  };

  const addLineShape = () => {
    const line = createLine(
      generateShapeId("line"),
      Math.random() * 400 + 100,
      Math.random() * 300 + 100,
      [0, 0, 100, 0, 100, 50, 0, 50],
      {
        ...COLOR_PRESETS.red,
        strokeWidth: 3,
      }
    );
    dispatch(addShape(line));
  };

  const addEllipseShape = () => {
    const ellipse = createEllipse(
      generateShapeId("ellipse"),
      Math.random() * 400 + 100,
      Math.random() * 300 + 100,
      {
        width: 140,
        height: 80,
        ...COLOR_PRESETS.slate,
      }
    );
    dispatch(addShape(ellipse));
  };

  const addTextShape = () => {
    const text = createText(
      generateShapeId("text"),
      Math.random() * 400 + 100,
      Math.random() * 300 + 100,
      "New Text",
      {
        fontSize: 20,
        fill: COLOR_PRESETS.orange.fill,
      }
    );
    dispatch(addShape(text));
  };

  return (
    <div className="fixed top-20 left-4 bg-white shadow-lg rounded-lg p-4 space-y-2 z-10">
      <h3 className="font-semibold text-sm text-gray-700 mb-3">Add Shapes</h3>

      <button
        onClick={addCircleShape}
        className="w-full px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md text-sm font-medium transition-colors"
      >
        ⭕ Circle
      </button>

      <button
        onClick={addRectangleShape}
        className="w-full px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-md text-sm font-medium transition-colors"
      >
        ⬜ Rectangle
      </button>

      <button
        onClick={addLineShape}
        className="w-full px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-md text-sm font-medium transition-colors"
      >
        📏 Line
      </button>

      <button
        onClick={addEllipseShape}
        className="w-full px-4 py-2 bg-purple-500 hover:bg-purple-600 text-white rounded-md text-sm font-medium transition-colors"
      >
        🥚 Ellipse
      </button>

      <button
        onClick={addTextShape}
        className="w-full px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white rounded-md text-sm font-medium transition-colors"
      >
        📝 Text
      </button>
    </div>
  );
}
