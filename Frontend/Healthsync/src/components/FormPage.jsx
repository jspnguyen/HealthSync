import Sidebar from "./Sidebar";

function FormPage() {
  return (
    <section className="flex w-[95vw]">
      <Sidebar />

      {/* Home Page */}
      <section className="ml-12 px-12 py-6 w-full">
        <div className="mb-8">
          <h1 className="font-bold text-4xl">
            Health<span className="text-blue">sync</span>
          </h1>
          <p className="text-secondary">Welcome back!</p>
        </div>
      </section>
    </section>
  );
}

export default FormPage;
