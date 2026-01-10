# Shape Resize and Transform Feature

## Overview
Shapes can now be selected, resized, and rotated using Konva's Transformer component. This provides an intuitive interface with visual handles for manipulating shapes.

## Features

### ✅ Shape Selection
- **Click any shape** to select it
- Selected shapes show a **blue highlight** (stroke color changes to #0066FF)
- **Click on empty canvas** to deselect

### ✅ Resize Handles
When a shape is selected, resize handles appear:
- **8 anchor points** for most shapes (corners and midpoints)
- **4 corner anchors** for lines
- **Drag handles** to resize the shape
- **Minimum size constraint** prevents shapes from becoming too small (5px minimum)

### ✅ Rotation
- **Rotation handle** appears above selected shapes
- **Drag to rotate** the shape around its center
- Rotation angle is saved to Redux state

### ✅ Transform Behavior by Shape Type

#### Circle
- Resizing adjusts the **radius**
- Maintains circular shape (uniform scaling)
- Rotation is supported but visually has no effect on circles

#### Rectangle
- Independent **width** and **height** resizing
- Corner handles resize proportionally
- Side handles resize in one dimension
- Full rotation support

#### Ellipse
- Independent **width** and **height** resizing
- Adjusts radiusX and radiusY
- Full rotation support

#### Line
- **4 corner handles** only
- Scales the point coordinates
- Full rotation support

#### Text
- Resizing adjusts **font size**
- Maintains aspect ratio
- Full rotation support

## Implementation Details

### Components

#### `SelectableShape.tsx`
Wraps each shape with selection and transformation capabilities:
- Manages shape ref for Transformer attachment
- Handles selection state
- Renders appropriate shape component
- Attaches Transformer when selected

#### `ShapeRenderer.tsx` (Updated)
All shape components now:
- Use `forwardRef` to expose refs to parent
- Accept `isSelected` prop for visual feedback
- Show blue stroke when selected
- Support `onClick` and `onTap` events

### State Management

#### Redux Actions Used
```typescript
// Select a shape
dispatch(selectShape(shapeId));

// Deselect all shapes
dispatch(selectShape(null));

// Update shape after transform
dispatch(updateShape({
  id: shapeId,
  updates: {
    x, y, rotation,
    width, height, // for rectangles/ellipses
    radius, // for circles
    fontSize, // for text
  }
}));
```

### Event Handlers

#### `handleSelect(shapeId)`
- Called when a shape is clicked
- Dispatches `selectShape` action
- Updates Redux state with selected shape ID

#### `handleStageClick(e)`
- Called when canvas background is clicked
- Deselects current shape if clicking empty area
- Dispatches `selectShape(null)`

#### `handleTransformEnd(shapeId)`
- Called when resize/rotate operation completes
- Extracts new dimensions from Konva node
- Calculates appropriate updates based on shape type
- Dispatches `updateShape` with new properties
- Resets scale to 1 (dimensions are updated instead)

## Usage

### Selecting a Shape
```typescript
// Click on any shape
onClick={() => dispatch(selectShape(shape.id))}
```

### Deselecting
```typescript
// Click on empty canvas
if (e.target === e.target.getStage()) {
  dispatch(selectShape(null));
}
```

### Accessing Selected Shape
```typescript
const selectedShapeId = useAppSelector(
  (state) => state.editor.selectedShapeId
);

const isSelected = shape.id === selectedShapeId;
```

## Visual Feedback

### Selected State
- **Stroke color**: Changes to #0066FF (blue)
- **Stroke width**: Increases (2-3px for most shapes)
- **Transformer**: Shows resize handles and rotation handle
- **Bounding box**: Visible around the shape

### Transform Handles
- **Corner handles**: Resize proportionally (or both dimensions)
- **Side handles**: Resize in one dimension
- **Rotation handle**: Circular handle above the shape
- **Handle color**: Blue (#0066FF)

## Keyboard Shortcuts (Future Enhancement)
Potential additions:
- **Delete**: Remove selected shape
- **Ctrl+D**: Duplicate selected shape
- **Ctrl+Z**: Undo
- **Ctrl+Y**: Redo
- **Arrow keys**: Nudge selected shape

## Constraints

### Minimum Size
- Shapes cannot be resized smaller than **5px**
- Text font size cannot be smaller than **8px**
- Enforced in `boundBoxFunc` of Transformer

### Scale Normalization
After transformation:
- Scale is reset to 1
- Actual dimensions are updated instead
- Prevents scale accumulation on repeated transforms

## Code Example

### Complete Transform Flow
```typescript
// 1. User clicks shape
<SelectableShape
  onSelect={() => dispatch(selectShape(shape.id))}
/>

// 2. Shape becomes selected
isSelected={shape.id === selectedShapeId}

// 3. Transformer attaches to shape
useEffect(() => {
  if (isSelected) {
    transformerRef.current.nodes([shapeRef.current]);
  }
}, [isSelected]);

// 4. User resizes/rotates
// Transformer handles the interaction

// 5. Transform ends
onTransformEnd={(e) => {
  const node = e.target;
  dispatch(updateShape({
    id: shape.id,
    updates: {
      x: node.x(),
      y: node.y(),
      rotation: node.rotation(),
      width: node.width(),
      height: node.height(),
    }
  }));
}}
```

## Browser Compatibility
- ✅ Desktop: Full support (mouse events)
- ✅ Touch devices: Full support (onTap events)
- ✅ All modern browsers

## Performance Considerations
- Transformer only renders for selected shape
- Efficient ref-based attachment
- Batch drawing after transformer attachment
- No re-renders for unselected shapes

## Troubleshooting

### Transformer not appearing
- Check if shape ref is properly forwarded
- Verify `isSelected` prop is true
- Ensure Transformer is in the same Layer

### Resize not updating Redux
- Check `handleTransformEnd` is called
- Verify `updateShape` action is dispatched
- Check shape type-specific update logic

### Shape jumps after resize
- Ensure scale is reset to 1
- Verify x, y coordinates are updated
- Check for scale accumulation

## Future Enhancements
1. **Multi-select**: Select multiple shapes with Shift+Click
2. **Group transforms**: Transform multiple shapes together
3. **Aspect ratio lock**: Hold Shift while resizing
4. **Snap to grid**: Align shapes to grid while transforming
5. **Smart guides**: Show alignment guides relative to other shapes
