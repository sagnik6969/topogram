import {
  Search,
  Square,
  Circle,
  MousePointer2,
  Ellipsis,
  Type,
} from "lucide-react";
import { useMemo, type ComponentType, type SVGProps } from "react";
import { useAppDispatch } from "@/store/hooks";
import { addShape } from "@/store/slices/editorSlice";
import {
  createRectangle,
  createEllipse,
  createText,
  generateShapeId,
  COLOR_PRESETS,
} from "@/utils/shapeFactory";

interface MenubarItemProps {
  icon: ComponentType<SVGProps<SVGSVGElement> & { size?: number | string }>;
  onClick?: () => void;
  active?: boolean;
}

function MenubarItem({ icon: Icon, onClick, active }: MenubarItemProps) {
  return (
    <button
      className={`p-3 hover:bg-slate-100 m-1 rounded transition-colors ${
        active ? "bg-slate-200" : ""
      }`}
      onClick={onClick}
    >
      <Icon size={14} />
    </button>
  );
}

function Menubar() {
  const dispatch = useAppDispatch();

  const addRectangleShape = () => {
    const rectangle = createRectangle(
      generateShapeId("rectangle"),
      Math.random() * 400 + 100,
      Math.random() * 300 + 100,
      {
        width: 120,
        height: 80,
        ...COLOR_PRESETS.slate,
      }
    );
    dispatch(addShape(rectangle));
  };

  const addEllipseShape = () => {
    const ellipse = createEllipse(
      generateShapeId("ellipse"),
      Math.random() * 400 + 100,
      Math.random() * 300 + 100,
      {
        radiusX: 140,
        radiusY: 80,
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
        fill: COLOR_PRESETS.slate.stroke,
      }
    );
    dispatch(addShape(text));
  };

  const menubarItems = useMemo(
    () => [
      {
        icon: Search,
        onClick: undefined, // Search/zoom tool (to be implemented)
      },
      {
        icon: MousePointer2,
        onClick: undefined, // Selection tool (to be implemented)
      },
      {
        icon: Circle,
        onClick: addEllipseShape,
      },
      {
        icon: Square,
        onClick: addRectangleShape,
      },
      {
        icon: Type,
        onClick: addTextShape,
      },
      {
        icon: Ellipsis,
        onClick: undefined,
      },
    ],
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  return (
    <div className="bg-background border-slate-200 border rounded-sm flex flex-col items-center justify-center w-fit shadow-md fixed top-[30%] left-3 z-50">
      {menubarItems.map((item, index) => (
        <MenubarItem key={index} icon={item.icon} onClick={item.onClick} />
      ))}
    </div>
  );
}

export default Menubar;
