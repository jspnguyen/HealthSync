import PropTypes from "prop-types";

// prop validation
MedicalCard.propTypes = {
  count: PropTypes.string.isRequired,
  position: PropTypes.string.isRequired,
  status: PropTypes.string.isRequired,
};

export default function MedicalCard({ count, position, status }) {
  let statusColor = "bg-green";

  if (status === "Normal") {
    statusColor = "bg-green";
  } else {
    statusColor = "bg-red";
  }

  return (
    <div className="w-[250px] h-[200px] flex flex-col justify-center items-center border-2 rounded-2xl gap-4">
      <h3> {position} </h3>
      <p className="peopleCount"> {count} </p>
      <div
        className={`px-3 py-1.5 flex items-center gap-2 text-black rounded-lg ${statusColor}`}
      >
        {status}
      </div>
    </div>
  );
}
