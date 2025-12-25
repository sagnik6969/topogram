# Shape System Documentation

## Overview
The diagram editor now supports multiple shape types with a clean, extensible architecture. Each shape type has its own dedicated renderer function, making it easy to add new shapes or customize existing ones.

## Supported Shape Types

### 1. Circle
```typescript
{
  id: string;
  type: 'circle';
  x: number;
  y: number;
  radius?: number;
  fill?: string;
  stroke?: string;
  strokeWidth?: number;
  rotation?: number;
  opacity?: number;
}
```

### 2. Rectangle
```typescript
{
  id: string;
  type: 'rectangle';
  x: number;
  y: number;
  width?: number;
  height?: number;
  fill?: string;
  stroke?: string;
  strokeWidth?: number;
  rotation?: number;
  opacity?: number;
}
```

### 3. Line
```typescript
{
  id: string;
  type: 'line';
  x: number;
  y: number;
  points?: number[]; // Array of coordinates [x1, y1, x2, y2, ...]
  stroke?: string;
  strokeWidth?: number;
  rotation?: number;
  opacity?: number;
}
```

### 4. Ellipse
```typescript
{
  id: string;
  type: 'ellipse';
  x: number;
  y: number;
  width?: number;  // Used to calculate radiusX
  height?: number; // Used to calculate radiusY
  fill?: string;
  stroke?: string;
  strokeWidth?: number;
  rotation?: number;
  opacity?: number;
}
```

### 5. Text
```typescript
{
  id: string;
  type: 'text';
  x: number;
  y: number;
  text?: string;
  fontSize?: number;
  fontFamily?: string;
  fill?: string;
  rotation?: number;
  opacity?: number;
}
```

## Architecture

### Shape Renderer Components
Located in: `src/components/shapes/ShapeRenderer.tsx`

Each shape type has its own dedicated component function:
- `CircleShape` - Renders circle shapes
- `RectangleShape` - Renders rectangle shapes
- `LineShape` - Renders line shapes
- `EllipseShape` - Renders ellipse shapes
- `TextShape` - Renders text shapes

### Main Renderer Function
The `renderShape()` function uses a switch case to determine which component to render:

```typescript
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
```

## Usage Examples

### Adding Shapes with Redux

```typescript
import { useAppDispatch } from '@/store/hooks';
import { addShape } from '@/store/slices/editorSlice';

function MyComponent() {
  const dispatch = useAppDispatch();

  const addCircle = () => {
    dispatch(addShape({
      id: 'circle-' + Date.now(),
      type: 'circle',
      x: 100,
      y: 100,
      radius: 50,
      fill: '#FF6B6B',
      stroke: '#C92A2A',
      strokeWidth: 2,
    }));
  };

  const addRectangle = () => {
    dispatch(addShape({
      id: 'rect-' + Date.now(),
      type: 'rectangle',
      x: 200,
      y: 200,
      width: 120,
      height: 80,
      fill: '#4ECDC4',
      stroke: '#0D7377',
      strokeWidth: 2,
    }));
  };

  const addLine = () => {
    dispatch(addShape({
      id: 'line-' + Date.now(),
      type: 'line',
      x: 300,
      y: 300,
      points: [0, 0, 100, 0, 100, 100, 0, 100],
      stroke: '#2196F3',
      strokeWidth: 3,
    }));
  };

  return (
    <div>
      <button onClick={addCircle}>Add Circle</button>
      <button onClick={addRectangle}>Add Rectangle</button>
      <button onClick={addLine}>Add Line</button>
    </div>
  );
}
```

### Using Shape Factory Utilities

```typescript
import { useAppDispatch } from '@/store/hooks';
import { addShape } from '@/store/slices/editorSlice';
import {
  createCircle,
  createRectangle,
  createText,
  generateShapeId,
  COLOR_PRESETS,
} from '@/utils/shapeFactory';

function MyComponent() {
  const dispatch = useAppDispatch();

  const addStyledCircle = () => {
    const circle = createCircle(
      generateShapeId('circle'),
      150,
      150,
      {
        radius: 60,
        ...COLOR_PRESETS.blue,
      }
    );
    dispatch(addShape(circle));
  };

  const addTextLabel = () => {
    const text = createText(
      generateShapeId('text'),
      200,
      200,
      'Hello World!',
      {
        fontSize: 24,
        fill: COLOR_PRESETS.purple.fill,
      }
    );
    dispatch(addShape(text));
  };

  return (
    <div>
      <button onClick={addStyledCircle}>Add Blue Circle</button>
      <button onClick={addTextLabel}>Add Text</button>
    </div>
  );
}
```

### Rendering Shapes in Canvas

```typescript
import { Stage, Layer } from 'react-konva';
import { useAppSelector, useAppDispatch } from '@/store/hooks';
import { updateShape } from '@/store/slices/editorSlice';
import { renderShape } from '@/components/shapes/ShapeRenderer';

function Canvas() {
  const dispatch = useAppDispatch();
  const shapes = useAppSelector((state) => state.editor.shapes);

  const handleDragEnd = (shapeId: string) => (e: any) => {
    dispatch(updateShape({
      id: shapeId,
      updates: {
        x: e.target.x(),
        y: e.target.y(),
      },
    }));
  };

  return (
    <Stage width={800} height={600}>
      <Layer>
        {shapes.map((shape) => 
          renderShape(shape, handleDragEnd(shape.id))
        )}
      </Layer>
    </Stage>
  );
}
```

## Adding New Shape Types

To add a new shape type (e.g., "star"):

### 1. Update the Shape Interface
In `src/store/slices/editorSlice.ts`:
```typescript
export interface Shape {
  id: string;
  type: 'circle' | 'rectangle' | 'line' | 'ellipse' | 'text' | 'star';
  // ... existing properties
  // Star-specific properties
  numPoints?: number;
  innerRadius?: number;
  outerRadius?: number;
}
```

### 2. Create the Shape Component
In `src/components/shapes/ShapeRenderer.tsx`:
```typescript
import { Star } from 'react-konva';

export function StarShape({ shape, onDragEnd, onClick }: ShapeRendererProps) {
  return (
    <Star
      x={shape.x}
      y={shape.y}
      numPoints={shape.numPoints || 5}
      innerRadius={shape.innerRadius || 20}
      outerRadius={shape.outerRadius || 40}
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
```

### 3. Add to Switch Case
In the `renderShape` function:
```typescript
switch (shape.type) {
  // ... existing cases
  case 'star':
    return <StarShape key={shape.id} {...props} />;
  default:
    return null;
}
```

### 4. Create Factory Function (Optional)
In `src/utils/shapeFactory.ts`:
```typescript
export function createStar(
  id: string,
  x: number,
  y: number,
  options?: Partial<Shape>
): Shape {
  return {
    id,
    type: 'star',
    x,
    y,
    numPoints: 5,
    innerRadius: 20,
    outerRadius: 40,
    fill: '#FFD700',
    stroke: '#FFA500',
    strokeWidth: 2,
    ...options,
  };
}
```

## Color Presets

Available color presets in `shapeFactory.ts`:
- `red` - Vibrant red with darker stroke
- `blue` - Bright blue with darker stroke
- `green` - Fresh green with darker stroke
- `yellow` - Sunny yellow with darker stroke
- `purple` - Rich purple with darker stroke
- `orange` - Warm orange with darker stroke
- `teal` - Cool teal with darker stroke
- `pink` - Soft pink with darker stroke
- `gray` - Neutral gray with darker stroke

Usage:
```typescript
import { COLOR_PRESETS } from '@/utils/shapeFactory';

dispatch(addShape({
  // ... other properties
  ...COLOR_PRESETS.blue,
}));
```

## Best Practices

1. **Always use `generateShapeId()`** to create unique IDs
2. **Use factory functions** for consistent shape creation
3. **Extract event handlers** to avoid inline functions in render
4. **Use color presets** for consistent styling
5. **Add TypeScript types** for all shape properties
6. **Keep shape components pure** - no side effects or state

## Common Patterns

### Updating Shape Properties
```typescript
dispatch(updateShape({
  id: shapeId,
  updates: {
    fill: '#FF0000',
    strokeWidth: 5,
    rotation: 45,
  },
}));
```

### Removing Shapes
```typescript
dispatch(removeShape(shapeId));
```

### Selecting Shapes
```typescript
dispatch(selectShape(shapeId));
```

### Clearing All Shapes
```typescript
dispatch(clearCanvas());
```

## Performance Tips

1. Use `React.memo()` for shape components if needed
2. Avoid creating new functions in render (use `useCallback`)
3. Keep the shape array immutable (Redux Toolkit handles this)
4. Use virtualization for large numbers of shapes
5. Consider using `perfectDrawEnabled={false}` on Konva Stage for better performance
