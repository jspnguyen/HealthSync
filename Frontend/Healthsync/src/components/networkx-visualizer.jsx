import React, { useEffect, useRef, useState } from "react";
import * as d3 from "d3";

// Define color mapping for node types
const colorMapping = {
  Doctor: "#1f77b4", // Blue
  Nurse: "#ff7f0e", // Orange
  Patient: "#2ca02c", // Green
  Equipment: "#d62728", // Red
  Room: "#9467bd", // Purple
  Bed: "#8c564b", // Brown
  WaitingRoom: "#e377c2", // Pink
};

const Graph = () => {
  const svgRef = useRef(null);

  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const baseNodes = useRef([]); // Store the initial data from the API
  const baseLinks = useRef([]); // Store the initial data from the API

  const simulationRef = useRef(null);
  const linkGroupRef = useRef(null);
  const nodeGroupRef = useRef(null);

  // Helper function to extract IDs from source and target
  const getLinkId = (link) => {
    const sourceId = typeof link.source === "object" ? link.source.id : link.source;
    const targetId = typeof link.target === "object" ? link.target.id : link.target;
    return `${sourceId}-${targetId}`;
  };

  // Helper function to check if the graph data changed
  const hasGraphChanged = (newNodes, newLinks) => {
    const newNodeIds = new Set(newNodes.map((n) => n.id));
    const baseNodeIds = new Set(baseNodes.current.map((n) => n.id));

    const nodesAddedOrRemoved =
      newNodeIds.size !== baseNodeIds.size ||
      [...newNodeIds].some((id) => !baseNodeIds.has(id)) ||
      [...baseNodeIds].some((id) => !newNodeIds.has(id));

    const newLinkIds = new Set(newLinks.map(getLinkId));
    const baseLinkIds = new Set(baseLinks.current.map(getLinkId));

    const linksAddedOrRemoved =
      newLinkIds.size !== baseLinkIds.size ||
      [...newLinkIds].some((id) => !baseLinkIds.has(id)) ||
      [...baseLinkIds].some((id) => !newLinkIds.has(id));

    return nodesAddedOrRemoved || linksAddedOrRemoved;
  };

  // Fetch the data from the API
  const fetchData = async () => {
    const response = await fetch("http://localhost:8080/graph");
    const newData = await response.json();

    // Deep clone the new data to prevent D3 mutations from affecting our comparison
    const clonedNodes = structuredClone(newData.nodes);
    const clonedLinks = structuredClone(newData.links);

    // Check if nodes or links are removed or added
    if (hasGraphChanged(clonedNodes, clonedLinks)) {
      baseNodes.current = clonedNodes;
      baseLinks.current = clonedLinks;

      // Deep clone data before setting state to prevent mutations
      setGraphData({
        nodes: structuredClone(clonedNodes),
        links: structuredClone(clonedLinks),
      });
    }
  };

  useEffect(() => {
    fetchData(); // Fetch data on component mount

    // Optionally, set an interval to keep fetching updated data from the API
    const intervalId = setInterval(fetchData, 1000);
    return () => clearInterval(intervalId); // Cleanup the interval on component unmount
  }, []);

  useEffect(() => {
    // Initialize SVG and simulation on mount
    const svg = d3.select(svgRef.current);
    const width = 800;
    const height = 600;
    svg.attr("width", width).attr("height", height);

    // Add groups for links and nodes
    const linkGroup = svg.append("g").attr("class", "links");
    const nodeGroup = svg.append("g").attr("class", "nodes");

    linkGroupRef.current = linkGroup;
    nodeGroupRef.current = nodeGroup;

    // Initialize simulation
    const simulation = d3
      .forceSimulation()
      .force("link", d3.forceLink().id((d) => d.id).distance(15))
      .force("charge", d3.forceManyBody().strength(-10))
      .force("center", d3.forceCenter(width / 2, height / 2));

    simulationRef.current = simulation;

    simulation.on("tick", () => {
      // Update positions on every tick
      linkGroup
        .selectAll("line")
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      nodeGroup
        .selectAll("circle")
        .attr("cx", (d) => d.x)
        .attr("cy", (d) => d.y);
    });

    return () => {
      // Clean up
      simulation.stop();
    };
  }, []); // Empty dependency array to run only on mount

  useEffect(() => {
    if (
      !graphData ||
      graphData.nodes.length === 0 ||
      graphData.links.length === 0
    ) {
      return;
    }

    const simulation = simulationRef.current;
    const linkGroup = linkGroupRef.current;
    const nodeGroup = nodeGroupRef.current;

    // Update links
    const linkElements = linkGroup
      .selectAll("line")
      .data(graphData.links, getLinkId);

    linkElements.exit().remove();

    const linkEnter = linkElements
      .enter()
      .append("line")
      .attr("stroke-width", 1)
      .attr("stroke", "rgba(50, 50, 50, 0.2)");

    linkEnter.merge(linkElements);

    // Update nodes
    const nodeElements = nodeGroup
      .selectAll("circle")
      .data(graphData.nodes, (d) => d.id);

    nodeElements.exit().remove();

    const nodeEnter = nodeElements
      .enter()
      .append("circle")
      .attr("r", 5)
      .attr("fill", (d) => colorMapping[d.type] || "#ccc")
      .call(drag(simulation));

    nodeEnter.merge(nodeElements);

    // Update and restart simulation only if there are changes
    simulation.nodes(graphData.nodes);
    simulation.force("link").links(graphData.links);
    simulation.alpha(1).restart();
  }, [graphData]);

  // Drag behavior
  function drag(simulation) {
    return d3
      .drag()
      .on("start", (event) => {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
      })
      .on("drag", (event) => {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      })
      .on("end", (event) => {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
      });
  }

  return (
    <svg ref={svgRef}>
      <g />
    </svg>
  );
};

export default Graph;
