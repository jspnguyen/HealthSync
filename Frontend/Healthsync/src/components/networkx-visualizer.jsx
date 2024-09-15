import * as d3 from 'd3';
import React, { useState, useEffect, useRef } from 'react';
import './networkx-visualizer.css';

const ForceDirectedLayout = () => {
  const [simulationRunning, setSimulationRunning] = useState(false);
  const svgRef = useRef();  // The ref for the SVG element
  const colorMapping = {
    Doctor: '#1f77b4',    // Blue
    Nurse: '#ff7f0e',     // Orange
    Patient: '#2ca02c',   // Green
    Equipment: '#d62728', // Red
    Room: '#9467bd',      // Purple
    Bed: '#8c564b',       // Brown
    WaitingRoom: '#e377c2'// Pink
  };

  useEffect(() => {
    const width = 960;
    const height = 650;
    const maxLinkDistance = 150;  // Maximum distance between nodes

    // Select the svg element
    const svg = d3.select(svgRef.current);
    svg.attr("width", width).attr("height", height);

    // Append groups for links and nodes if they don't already exist
    let linkGroup = svg.select("g.links");
    if (linkGroup.empty()) {
      linkGroup = svg.append("g").attr("class", "links");
    }

    let nodeGroup = svg.select("g.nodes");
    if (nodeGroup.empty()) {
      nodeGroup = svg.append("g").attr("class", "nodes");
    }

    const simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(d => d.id).distance(50).strength(0.8))  // Reduced link distance
    .force("charge", d3.forceManyBody().strength(-50))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .alphaDecay(0.05);

    fetch('/force.json')
      .then(response => response.json())
      .then(data => {

        // Create or update links
        const link = linkGroup.selectAll("line")
          .data(data.links)
          .join("line")
          .attr("stroke", "#999");

        // Create or update nodes
        const node = nodeGroup.selectAll("circle")
          .data(data.nodes)
          .join('circle')
          .attr("r", 5)
          .attr("fill", d => colorMapping[d.type])
          .call(
            d3.drag()
              .on("start", (event, d) => {
                if (!simulationRunning) {
                  simulation.alphaTarget(0.3).restart();  // Boost alpha for smoother interaction
                  setSimulationRunning(true);
                }
                d.fx = d.x;
                d.fy = d.y;
              })
              .on("drag", (event, d) => {
                d.fx = event.x;
                d.fy = event.y;
              })
              .on("end", (event, d) => {
                if (!event.active) {
                  simulation.alphaTarget(0);  // Lower alpha back to 0 to settle simulation
                }
                d.fx = null;  // Free the node when dragging ends
                d.fy = null;
                setSimulationRunning(false);
              })
          );

        node.append('title')
          .text(d => d.id);

        // Run the simulation
        simulation
          .nodes(data.nodes)
          .on("tick", () => {
            link
              .attr("x1", d => d.source.x)
              .attr("y1", d => d.source.y)
              .attr("x2", d => d.target.x)
              .attr("y2", d => d.target.y);

            node
              .attr("cx", d => d.x)
              .attr("cy", d => d.y);
          });

        simulation.force("link")
          .links(data.links);
      })
      .catch(error => console.error('Error loading JSON:', error));

    // Cleanup simulation on unmount
    return () => simulation.stop();
  }, []);

  return (
    <div>
      <svg  ref={svgRef}></svg>
    </div>
  );
};

export default ForceDirectedLayout;
