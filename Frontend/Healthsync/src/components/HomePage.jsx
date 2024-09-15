import Sidebar from "./Sidebar";

function HomePage() {
  return (
    <section className="flex">
      <Sidebar />
      <section className="px-12 py-8">
        <div>
          <h1 className="font-bold text-4xl">
            Health<span className="text-blue">sync</span>
          </h1>
          <p className="text-secondary">Welcome back!</p>
        </div>
      </section>
    </section>
  );
}

export default HomePage;
