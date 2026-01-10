import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

export interface Shape {
  id: string;
  type: 'circle' | 'rectangle' | 'line' | 'ellipse' | 'text';
  x: number;
  y: number;
  fill?: string;
  stroke?: string;
  strokeWidth?: number;
  // Circle properties
  radius?: number;
  // Rectangle & Ellipse properties
  width?: number;
  height?: number;
  // Line properties
  points?: number[];
  // Text properties
  text?: string;
  fontSize?: number;
  fontFamily?: string;
  rotation?: number;
  opacity?: number;
  // ellipse properties
  radiusX?: number;
  radiusY?: number
}

export interface Connection {
  id: string;
  from: string; // source shape ID
  to: string;   // target shape ID
}

export type ActiveTool = 'select' | 'hand' | 'connector';

interface EditorState {
  shapes: Shape[];
  connections: Connection[];
  selectedShapeId: string | null;
  activeTool: ActiveTool;
  canvasWidth: number;
  canvasHeight: number;
}

const initialState: EditorState = {
  shapes: [],
  connections: [],
  selectedShapeId: null,
  activeTool: 'select',
  canvasWidth: window.innerWidth,
  canvasHeight: window.innerHeight,
};

const editorSlice = createSlice({
  name: 'editor',
  initialState,
  reducers: {
    addShape: (state, action: PayloadAction<Shape>) => {
      state.shapes.push(action.payload);
    },
    updateShape: (state, action: PayloadAction<{ id: string; updates: Partial<Shape> }>) => {
      const shape = state.shapes.find(s => s.id === action.payload.id);
      if (shape) {
        Object.assign(shape, action.payload.updates);
      }
      else {
        console.error(`Shape with ID ${action.payload.id} not found`);
      }
    },
    removeShape: (state, action: PayloadAction<string>) => {
      state.shapes = state.shapes.filter(s => s.id !== action.payload);
      state.connections = state.connections.filter(c => c.from !== action.payload && c.to !== action.payload);
    },
    setActiveTool: (state, action: PayloadAction<ActiveTool>) => {
      state.activeTool = action.payload;
    },
    addConnection: (state, action: PayloadAction<Connection>) => {
      state.connections.push(action.payload);
    },
    removeConnection: (state, action: PayloadAction<string>) => {
      state.connections = state.connections.filter(c => c.id !== action.payload);
    },
    selectShape: (state, action: PayloadAction<string | null>) => {
      state.selectedShapeId = action.payload;
    },
    setCanvasSize: (state, action: PayloadAction<{ width: number; height: number }>) => {
      state.canvasWidth = action.payload.width;
      state.canvasHeight = action.payload.height;
    },
    clearCanvas: (state) => {
      state.shapes = [];
      state.selectedShapeId = null;
    },
  },
});

export const {
  addShape,
  updateShape,
  removeShape,
  selectShape,
  setCanvasSize,
  clearCanvas,
  setActiveTool,
  addConnection,
  removeConnection,
} = editorSlice.actions;

export default editorSlice.reducer;
