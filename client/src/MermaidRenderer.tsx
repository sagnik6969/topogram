import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';
import elkLayout from '@mermaid-js/layout-elk';

mermaid.registerLayoutLoaders(elkLayout);

mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
});

interface MermaidRendererProps {
  chart: string;
}

const MermaidRenderer: React.FC<MermaidRendererProps> = ({ chart }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const renderChart = async () => {
      if (containerRef.current && chart) {
        try {
          // Generate a unique ID for each render to avoid conflicts
          const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`;
          // mermaid.render returns an object { svg: string }
          const { svg } = await mermaid.render(id, chart);
          if (containerRef.current) {
            containerRef.current.innerHTML = svg;
          }
        } catch (error) {
          console.error('Mermaid syntax error:', error);
          if (containerRef.current) {
            // Keep the previous diagram if possible, or show error?
            // Usually showing error is better in a live editor context
            // But mermaid's default error is often an SVG too, or we can just print text
             containerRef.current.innerHTML = `<pre style="color: red;">${error instanceof Error ? error.message : String(error)}</pre>`;
          }
        }
      }
    };

    renderChart();
  }, [chart]);

  return <div ref={containerRef} style={{ width: '100%', height: '100%', overflow: 'auto' }} />;
};

export default MermaidRenderer;
