# Redux Setup Documentation

## Overview
This project now uses **Redux Toolkit** for state management. Redux Toolkit is the official, recommended way to write Redux logic.

## Structure

```
src/
├── store/
│   ├── index.ts              # Store configuration
│   ├── hooks.ts              # Typed Redux hooks
│   └── slices/
│       └── editorSlice.ts    # Editor state slice
```

## Files Created

### 1. `src/store/index.ts`
The main store configuration file that combines all reducers.

```typescript
import { configureStore } from '@reduxjs/toolkit';
import editorReducer from './slices/editorSlice';

export const store = configureStore({
  reducer: {
    editor: editorReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### 2. `src/store/hooks.ts`
Typed hooks for use throughout the application instead of the plain `useDispatch` and `useSelector`.

```typescript
import { useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from './index';

export const useAppDispatch = useDispatch.withTypes<AppDispatch>();
export const useAppSelector = useSelector.withTypes<RootState>();
```

### 3. `src/store/slices/editorSlice.ts`
The editor slice containing state and reducers for the diagram editor.

**State Shape:**
```typescript
interface EditorState {
  shapes: Shape[];
  selectedShapeId: string | null;
  canvasWidth: number;
  canvasHeight: number;
}
```

**Available Actions:**
- `addShape(shape)` - Add a new shape to the canvas
- `updateShape({ id, updates })` - Update an existing shape
- `removeShape(id)` - Remove a shape from the canvas
- `selectShape(id)` - Select a shape
- `setCanvasSize({ width, height })` - Update canvas dimensions
- `clearCanvas()` - Clear all shapes

## Usage Examples

### Reading State
```typescript
import { useAppSelector } from '@/store/hooks';

function MyComponent() {
  const shapes = useAppSelector((state) => state.editor.shapes);
  const selectedId = useAppSelector((state) => state.editor.selectedShapeId);
  
  return <div>{shapes.length} shapes</div>;
}
```

### Dispatching Actions
```typescript
import { useAppDispatch } from '@/store/hooks';
import { addShape, updateShape } from '@/store/slices/editorSlice';

function MyComponent() {
  const dispatch = useAppDispatch();
  
  const handleAddCircle = () => {
    dispatch(addShape({
      id: 'unique-id',
      type: 'circle',
      x: 100,
      y: 100,
      radius: 50,
      fill: 'blue',
    }));
  };
  
  const handleUpdatePosition = (id: string, x: number, y: number) => {
    dispatch(updateShape({
      id,
      updates: { x, y },
    }));
  };
  
  return <button onClick={handleAddCircle}>Add Circle</button>;
}
```

## Adding New Slices

To add a new slice for different features:

1. Create a new file in `src/store/slices/`:
```typescript
// src/store/slices/uiSlice.ts
import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
}

const initialState: UIState = {
  sidebarOpen: true,
  theme: 'light',
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },
    setTheme: (state, action: PayloadAction<'light' | 'dark'>) => {
      state.theme = action.payload;
    },
  },
});

export const { toggleSidebar, setTheme } = uiSlice.actions;
export default uiSlice.reducer;
```

2. Add it to the store in `src/store/index.ts`:
```typescript
import uiReducer from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    editor: editorReducer,
    ui: uiReducer,  // Add new reducer here
  },
});
```

## Best Practices

1. **Always use typed hooks** (`useAppDispatch`, `useAppSelector`) instead of the plain ones
2. **Keep slices focused** - Each slice should manage a specific domain of your app
3. **Use `createSlice`** - It automatically generates action creators and action types
4. **Immutable updates** - Redux Toolkit uses Immer, so you can write "mutating" logic that's actually immutable
5. **Type-only imports** - Use `type` keyword for type imports to comply with `verbatimModuleSyntax`

## Dependencies Installed

```json
{
  "@reduxjs/toolkit": "^2.x.x",
  "react-redux": "^9.x.x"
}
```

## Integration Points

- **Provider**: Wrapped in `src/main.tsx`
- **Example Usage**: `src/pages/Editor.tsx` demonstrates how to use Redux with Konva shapes

## DevTools

Redux DevTools Extension is automatically configured with Redux Toolkit. Install the browser extension to inspect state changes:
- [Chrome Extension](https://chrome.google.com/webstore/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd)
- [Firefox Extension](https://addons.mozilla.org/en-US/firefox/addon/reduxdevtools/)

## Next Steps

Consider adding:
- **Async actions** using `createAsyncThunk` for API calls
- **Persistence** using `redux-persist` to save state to localStorage
- **Middleware** for logging, analytics, or custom logic
- **Selectors** using `createSelector` from Reselect for memoized derived state
