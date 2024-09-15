import PropTypes from "prop-types";

// prop validation
PatientCard.propTypes = {
  count: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  status: PropTypes.string.isRequired,
};

export default function PatientCard({ count, title, status }) {
  let statusColor = "bg-green";

  if (status === "Low") {
    statusColor = "bg-green";
  } else if (status === "Moderate") {
    statusColor = "bg-yellow";
  } else if (status === "High") {
    statusColor = "bg-red";
  } else {
    statusColor = "bg-secondary";
  }

  return (
    <div className="w-[350px] px-5 h-[160px] flex flex-col pt-4 items-center border-2 rounded-2xl gap-8">
      <div className="flex justify-between w-full ">
        <h3> {title} </h3>
        <div
          className={`px-3 py-1.5 flex items-center gap-2 text-black rounded-lg ${statusColor}`}
        >
          {status}
        </div>
      </div>
      <p className="peopleCount">
        {count}
        <span className="text-[#808080] text-base"> patients</span>
      </p>
    </div>
  );
}
