import { Link, useLocation } from "react-router-dom";
import {
  GridIcon,
  PieChartIcon,
  GearIcon,
  ExitIcon,
} from "@radix-ui/react-icons"; // Adjust the import based on your icon library
import { UserButton } from "@clerk/clerk-react";

function Sidebar() {
  const location = useLocation();

  const navItems = [
    {
      path: "/home",
      icon: <GridIcon className="w-[25px] h-[25px]" />,
      label: "Dashboard",
    },
    {
      path: "/charts",
      icon: <PieChartIcon className="w-[25px] h-[25px]" />,
      label: "Charts",
    },
    {
      path: "/settings",
      icon: <GearIcon className="w-[25px] h-[25px]" />,
      label: "Settings",
    },
  ];

  return (
    <div className="px-3 h-screen bg-white rounded-r-xl items-center flex flex-col fixed top-0 left-0">
      <section className="flex-1">
        {navItems.map((item) => (
          <div
            key={item.path}
            className={`navButton ${
              location.pathname === item.path ? "bg-blue-500" : ""
            }`}
          >
            <Link to={item.path}>{item.icon}</Link>
          </div>
        ))}
      </section>
      <div className="rounded-lg mb-4">
        <UserButton  />
      </div>
    </div>
  );
}

export default Sidebar;
