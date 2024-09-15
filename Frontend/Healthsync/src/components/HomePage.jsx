import Sidebar from "./Sidebar";

function HomePage() {
  return (
    <section className="flex w-99vw">
      <Sidebar />

      {/* Home Page */}
      <section className="ml-12 px-12 py-8 w-full">
        <div>
          <h1 className="font-bold text-4xl">
            Health<span className="text-blue">sync</span>
          </h1>
          <p className="text-secondary">Welcome back!</p>
        </div>

        <section>
          <h2 className=""> Agents</h2>

          <div className="border-2 w-[9500px] max-w-[950px] h-[500px] rounded-2xl">
            {/* insert node inside this div container */}
          </div>
        </section>
      </section>
    </section>
  );
}

export default HomePage;
