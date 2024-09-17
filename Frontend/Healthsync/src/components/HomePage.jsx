import React, { useState, useEffect } from "react";
import Sidebar from "./Sidebar";
import MedicalCard from "./ui/medicalCard";
import PatientCard from "./ui/PatientCard";
import Nodes from "./ui/Nodes";

function HomePage() {
  const [counts, setCounts] = useState({
    total_doctors: 0,
    available_doctors: 0,
    total_nurses: 0,
    available_nurses: 0,
    total_equipment: 0,
    available_equipment: 0,
    patients_being_treated: 0,
    patients_in_waiting_room: 0,
    beds_available: 0,
  });

  useEffect(() => {
    const fetchCounts = () => {
      fetch("/counts.json")
        .then((response) => response.json())
        .then((data) => {
          console.log("Data received:", data);
          setCounts(data);
        })
        .catch((error) => console.error("Error fetching data:", error));
    };

    // Initial fetch
    fetchCounts();

    // Set up interval to refresh every second
    const intervalId = setInterval(fetchCounts, 1000);

    // Cleanup interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  // Helper function to calculate percentage and assign status
  // Helper function to calculate percentage and assign status
  const calculateStatus = (available, total) => {
    if (total === 0) return "Unknown"; // Handle divide by zero case
    const percentage = (available / total) * 100;
    return percentage < 30 ? "Low" : "High";
  };

  // Corrected to match the status logic for all resources
  const calculateResource = (available, total) => {
    if (total === 0) return "Unknown"; // Handle divide by zero case
    const percentage = (available / total) * 100;
    return percentage < 30 ? "Low" : "High";
  };

  return (
    <section className="flex w-full">
      <Sidebar />

      {/* Home Page */}
      <section className="ml-12 px-12 py-6 w-full">
        <div className="mb-8">
          <h1 className="font-bold text-4xl">
            Health<span className="text-blue">sync</span>
          </h1>
          <p className="text-secondary">Welcome back!</p>
        </div>

        <section className="mt-4">
          {/* agents section */}
          <h2> Agents</h2>
          <div className="flex gap-8">
            <Nodes />

            {/* hospital information */}
            <div className="flex flex-col justify-between">
              <MedicalCard
                count={String(counts.available_doctors) + " \\ " + counts.total_doctors}
                position="Doctors"
                status={calculateResource(
                  counts.available_doctors,
                  counts.total_doctors
                )}
              />
              <MedicalCard
                count={String(counts.available_nurses) + " \\ " + counts.total_nurses}
                position="Nurses"
                status={calculateResource(
                  counts.available_nurses,
                  counts.total_nurses
                )}
              />
              <MedicalCard
                count={String(counts.available_equipment) + " \\ " + counts.total_equipment}
                position="Equipment"
                status={calculateResource(
                  counts.available_equipment,
                  counts.total_equipment
                )}
              />
            </div>
          </div>
        </section>

        {/* Patient Information */}
        <section className="mt-24 mb-4">
          <h2> Patient Information </h2>

          <section className="my-12">
            <div className="mb-8">
              <h4> Waiting </h4>
              <div className="flex gap-8">
                <PatientCard
                  count={String(counts.patients_in_waiting_room)}
                  title="Waiting"
                  status={calculateStatus(
                    counts.patients_in_waiting_room,
                    counts.beds_available
                  )}
                />
              </div>
            </div>
            <div className="mb-12">
              <h4> Observing </h4>
              <div className="flex gap-8">
                <PatientCard
                  count={String(counts.patients_being_treated)}
                  title="Being Treated"
                  status={calculateStatus(
                    counts.patients_being_treated,
                    counts.beds_available
                  )}
                />
                <PatientCard count="70" title="Emergency" status="High" />
              </div>
            </div>
            <div className="mb-12">
              <h4> Observing </h4>
              <div className="flex gap-8">
                <PatientCard count="30" title="General" status="Low" />
                <PatientCard count="70" title="Intensive Care" status="High" />
                <PatientCard count="50" title="Operating Room" status="High" />
              </div>
            </div>
          </section>
        </section>
      </section>
    </section>
  );
}

export default HomePage;
