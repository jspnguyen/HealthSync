import ForceDirectedLayout from "../networkx-visualizer";
function Nodes() {
  return (
    <div className="border-2 w-fit h-fit rounded-2xl bg-white">
      <ForceDirectedLayout />
    </div>
  );
}

export default Nodes;
