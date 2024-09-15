import Sidebar from "./Sidebar";
import MedicalCard from "./ui/medicalCard";
import PatientCard from "./ui/PatientCard";

function HomePage() {
  return (
    <section className="flex w-[95vw]">
      <Sidebar />

      {/* Home Page */}
      <section className="ml-12 px-12 py-6 w-full">
        <div>
          <h1 className="font-bold text-4xl">
            Health<span className="text-blue">sync</span>
          </h1>
          <p className="text-secondary">Welcome back!</p>
        </div>

        <section className="mt-4">
          {/* agents section */}
          <h2> Agents</h2>
          <div className="flex gap-8">
            <div className="border-2 w-[1200px] h-[650px] rounded-2xl">
              {/* insert node inside this div container */}
            </div>

            {/* hospital information */}
            <div className="flex flex-col justify-between">
              <MedicalCard count="20" position="Doctors" status="Normal" />
              <MedicalCard count="50" position="Nurses" status="Low" />
              <MedicalCard count="33" position="Equipment" status="Normal" />
            </div>
          </div>
        </section>

        {/* Patient Information */}
        <section className="mt-24 mb-4">
          <h2> Patient Information </h2>

          <section className="my-4">
            <div className="mb-8">
              <h4> Waiting </h4>
              <div className="flex gap-8">
                <PatientCard count="30" title="Waiting" status="Low" />
                <PatientCard count="70" title="Emergency" status="High" />
              </div>
            </div>
            <div className="mb-8">
              <h4> Observing </h4>
              <div className="flex gap-8">
                <PatientCard count="30" title="Waiting" status="Low" />
                <PatientCard count="70" title="Emergency" status="High" />
              </div>
            </div>
            <div className="mb-8">
              <h4> Observing </h4>
              <div className="flex gap-8">
                <PatientCard count="30" title="General" status="Low" />
                <PatientCard count="70" title="Intensive Care" status="High" />
                <PatientCard
                  count="50"
                  title="Operating Room"
                  status="Moderate"
                />
              </div>
            </div>
          </section>
        </section>
      </section>
    </section>
  );
}

export default HomePage;
