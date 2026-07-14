"use client";

import { useEffect, useMemo, useState } from "react";
import ReactFlow, {
  type Node,
  type Edge,
  type NodeMouseHandler,
  Background,
  Controls,
  MiniMap,
  ReactFlowProvider,
  useEdgesState,
  useNodesState,
  useReactFlow,
  Panel,
} from "reactflow";
import "reactflow/dist/style.css";

interface GraphViewProps {
  nodes: Node[];
  edges: Edge[];
}

function GraphCanvas({ nodes, edges }: GraphViewProps) {
  const [flowNodes, setFlowNodes, onNodesChange] = useNodesState(nodes);
  const [flowEdges, setFlowEdges, onEdgesChange] = useEdgesState(edges);
  const [selected, setSelected] = useState<Node | null>(null);
  const reactFlow = useReactFlow();

  useEffect(() => {
    setFlowNodes(nodes);
    setFlowEdges(edges);
    setSelected(null);
  }, [nodes, edges, setFlowNodes, setFlowEdges]);

  const initialLayout = useMemo(() => ({ nodes, edges }), [nodes, edges]);

  const onNodeClick: NodeMouseHandler = (_event, node) => {
    setSelected(node);
  };

  const resetLayout = () => {
    setFlowNodes(initialLayout.nodes);
    setFlowEdges(initialLayout.edges);
    setSelected(null);
    window.setTimeout(() => reactFlow.fitView({ padding: 0.2 }), 0);
  };

  return (
    <div className="h-full flex flex-col gap-2">
      <div className="flex-1 rounded-lg overflow-hidden border border-slate-700">
        <ReactFlow
          nodes={flowNodes}
          edges={flowEdges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          fitView
          attributionPosition="bottom-right"
        >
          <Panel position="top-right" className="flex gap-1">
            <button type="button" onClick={() => reactFlow.fitView({ padding: 0.2 })} className="px-2 py-1 text-xs rounded bg-slate-900/90 border border-slate-700 hover:bg-slate-700">
              Fit View
            </button>
            <button type="button" onClick={resetLayout} className="px-2 py-1 text-xs rounded bg-slate-900/90 border border-slate-700 hover:bg-slate-700">
              Reset Layout
            </button>
            <button type="button" onClick={() => reactFlow.zoomIn()} className="px-2 py-1 text-xs rounded bg-slate-900/90 border border-slate-700 hover:bg-slate-700">
              +
            </button>
            <button type="button" onClick={() => reactFlow.zoomOut()} className="px-2 py-1 text-xs rounded bg-slate-900/90 border border-slate-700 hover:bg-slate-700">
              −
            </button>
          </Panel>
          <Background color="#1e293b" gap={20} />
          <Controls />
          <MiniMap nodeColor="#1d4ed8" maskColor="rgba(0,0,0,0.6)" />
        </ReactFlow>
      </div>

      <div className="min-h-[64px] rounded-lg border border-slate-700 bg-slate-900/50 px-3 py-2 text-xs text-slate-300">
        {selected ? (
          <>
            <p className="font-semibold text-slate-100">{String(selected.data?.label || selected.id)}</p>
            {selected.data?.details ? <p className="text-slate-400 mt-1">{String(selected.data.details)}</p> : null}
          </>
        ) : (
          <p className="text-slate-500">Click a node to inspect details.</p>
        )}
      </div>
    </div>
  );
}

export default function GraphView({ nodes, edges }: GraphViewProps) {
  return (
    <ReactFlowProvider>
      <GraphCanvas nodes={nodes} edges={edges} />
    </ReactFlowProvider>
  );
}
