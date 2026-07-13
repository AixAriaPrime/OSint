"use client";

import ReactFlow, {
  type Node,
  type Edge,
  Background,
  Controls,
  MiniMap,
} from "reactflow";
import "reactflow/dist/style.css";

interface GraphViewProps {
  nodes: Node[];
  edges: Edge[];
}

export default function GraphView({ nodes, edges }: GraphViewProps) {
  return (
    <ReactFlow nodes={nodes} edges={edges} fitView attributionPosition="bottom-right">
      <Background color="#1e293b" gap={20} />
      <Controls />
      <MiniMap nodeColor="#1d4ed8" maskColor="rgba(0,0,0,0.6)" />
    </ReactFlow>
  );
}
