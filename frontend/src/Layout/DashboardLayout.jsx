import React, { useState, useEffect } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar/Sidebar";
import Topbar from "../components/Topbar/Topbar";

const DashboardLayout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(window.innerWidth >= 768);
  const [profilePicture, setProfilePicture] = useState(null); // Add state for profile pic

  const navigate = useNavigate();

  const userRole = localStorage.getItem("userRole");
  const userName = localStorage.getItem("userName");
  const userHallName = localStorage.getItem("hallName");
  const userEmail = localStorage.getItem("userEmail");

  useEffect(() => {
    // Responsive sidebar toggle on window resize
    const handleResize = () => {
      setIsSidebarOpen(window.innerWidth >= 768);
    };
    window.addEventListener("resize", handleResize);

    // Fetch user details to get profile image
    const fetchUserDetails = async () => {
      if (!userEmail) return;

      try {
        const res = await fetch(`http://127.0.0.1:8000/user_info/get_user_details/?email=${userEmail}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        if (!res.ok) throw new Error("Failed to fetch user details");

        const data = await res.json();

        if (data.user_info?.image) {
          setProfilePicture(`http://127.0.0.1:8000${data.user_info.image}`);
        } else {
          setProfilePicture(null); // Or a default image url
        }
      } catch (error) {
        console.error("Error fetching user details:", error);
        setProfilePicture(null);
      }
    };

    fetchUserDetails();

    return () => window.removeEventListener("resize", handleResize);
  }, [userEmail]);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="flex h-screen bg-base-200 overflow-auto">
      {/* Overlay for mobile when sidebar is open */}
      {isSidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black bg-opacity-50 lg:hidden"
          onClick={toggleSidebar}
        ></div>
      )}

      {/* Sidebar */}
      <div className="flex relative">
        <Sidebar
          isOpen={isSidebarOpen}
          userRole={userRole}
          toggleSidebar={toggleSidebar}
        />
      </div>

      {/* Main Content */}
      <div
        className={`flex-1 flex flex-col ${
          isSidebarOpen ? "lg:ml-64" : "lg:ml-20"
        } transition-all duration-300`}
      >
        {/* Pass profilePicture to Topbar */}
        <Topbar
          toggleSidebar={toggleSidebar}
          userName={userName}
          userHallName={userHallName}
          profilePicture={profilePicture}
        />
        <main className="flex-1 overflow-y-auto p-4 md:p-6 bg-primary-content text-black rounded-tl-xl shadow-inner">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
