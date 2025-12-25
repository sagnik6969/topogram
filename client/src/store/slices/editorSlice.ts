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
}

interface EditorState {
  shapes: Shape[];
  selectedShapeId: string | null;
  canvasWidth: number;
  canvasHeight: number;
}

const initialState: EditorState = {
  shapes: [],
  selectedShapeId: null,
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
    },
    removeShape: (state, action: PayloadAction<string>) => {
      state.shapes = state.shapes.filter(s => s.id !== action.payload);
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
} = editorSlice.actions;

export default editorSlice.reducer;
