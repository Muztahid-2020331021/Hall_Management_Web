import React, { useEffect, useState } from "react";

const DashboardHome = () => {
  const [loading, setLoading] = useState(true);
  const [userInfo, setUserInfo] = useState(null);
  const [passwords, setPasswords] = useState({ oldPassword: "", newPassword: "" });

  const userEmail = localStorage.getItem("userEmail");

  useEffect(() => {
    const fetchUserInfo = async () => {
      if (!userEmail) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const res = await fetch(
          `http://127.0.0.1:8000/user_info/get_user_details/?email=${userEmail}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        );

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        if (data.user_info) {
          const base = data.user_info;

          const info = {
            email: base.email,
            name: base.name,
            phone: base.phone_number,
            role: base.user_role,
            bloodGroup: base.blood_group,
            hallId: base.hall,
            profilePicture: base.image
              ? `http://127.0.0.1:8000${base.image}`
              : "https://via.placeholder.com/150",
          };

          const extra = data.extra_info || {};

          if (base.user_role === "student") {
            info.registrationNumber = extra.registration_number || "";
            info.department = extra.department || "";
            info.semester = extra.semester || "";
            info.session = extra.session || "";
            info.roomNumber = localStorage.getItem("roomNumber") || "";
          } else if (base.user_role === "provost_body") {
            info.provostRole = extra.provost_body_role || "";
            info.department = extra.department || "";
            info.departmentRole = extra.department_role || "";
            info.priority = extra.priority || "";
          } else if (base.user_role === "official_person") {
            info.officialRole = extra.official_role || "";
          }

          setUserInfo(info);

          // ✅ Store hallId in localStorage for use in other components
          localStorage.setItem("userHallId", info.hallId);
        } else {
          setUserInfo(null);
        }
      } catch (error) {
        console.error("Failed to fetch user info:", error);
        setUserInfo(null);
      } finally {
        setLoading(false);
      }
    };

    fetchUserInfo();
  }, [userEmail]);

  const handleProfilePicChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);
    formData.append("email", userInfo.email);

    try {
      const res = await fetch("http://127.0.0.1:8000/user_info/update_profile_picture/", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      const data = await res.json();

      if (!res.ok) {
        alert(`❌ ${data?.error || "Image upload failed."}`);
        return;
      }

      alert("✅ Profile picture updated successfully!");
      setUserInfo((prev) => ({
        ...prev,
        profilePicture: `http://127.0.0.1:8000${data.image_url}`,
      }));
    } catch (error) {
      console.error("Upload error:", error);
      alert("❌ Upload failed. Try again.");
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();

    if (!passwords.oldPassword || !passwords.newPassword) {
      alert("Please fill both password fields.");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/user_info/change_password/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          email: userInfo.email,
          old_password: passwords.oldPassword,
          new_password: passwords.newPassword,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        alert(`❌ ${data.error || "Failed to update password."}`);
        return;
      }

      alert("✅ Password updated successfully!");
      setPasswords({ oldPassword: "", newPassword: "" });
    } catch (error) {
      console.error("Password update failed:", error);
      alert("❌ Something went wrong. Try again.");
    }
  };

  const hallName = localStorage.getItem("hallName");

  const renderDashboardDetails = () => {
    switch (userInfo.role) {
      case "student":
        return (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-blue-600 text-white p-8 rounded-xl shadow-lg">
                <h3 className="text-2xl font-semibold">Current Semester</h3>
                <p className="text-4xl font-bold mt-4">{userInfo.semester}</p>
              </div>
              <div className="bg-green-600 text-white p-8 rounded-xl shadow-lg">
                <h3 className="text-2xl font-semibold">Room Number</h3>
                <p className="text-4xl font-bold mt-4">{userInfo.roomNumber || "N/A"}</p>
              </div>
              <div className="bg-purple-600 text-white p-8 rounded-xl shadow-lg">
                <h3 className="text-2xl font-semibold">Hall Name</h3>
                <p className="text-4xl font-bold mt-4">{hallName}</p>
              </div>
            </div>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-white p-6 rounded-xl shadow-lg">
                <h3 className="text-2xl font-semibold mb-4 text-blue-800">📚 Academic Details</h3>
                <p><strong>Department:</strong> {userInfo.department.toUpperCase()}</p>
                <p><strong>Session:</strong> {userInfo.session}</p>
                <p><strong>Semester:</strong> {userInfo.semester}</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-lg">
                <h3 className="text-2xl font-semibold mb-4 text-green-800">🏠 Residence Details</h3>
                <p><strong>Room Number:</strong> {userInfo.roomNumber || "N/A"}</p>
                <p><strong>Hall Name:</strong> {hallName}</p>
              </div>
            </div>
          </>
        );

      case "provost_body":
        return (
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <h3 className="text-2xl font-semibold mb-4 text-red-700">🏛️ Provost Body Details</h3>
            <p><strong>Name:</strong> {userInfo.name}</p>
            <p><strong>Role:</strong> {userInfo.provostRole || "N/A"}</p>
            <p><strong>Department:</strong> {userInfo.department || "N/A"}</p>
            <p><strong>Department Role:</strong> {userInfo.departmentRole || "N/A"}</p>
            <p><strong>Priority:</strong> {userInfo.priority || "N/A"}</p>
            <p><strong>Hall Name:</strong> {hallName}</p>
          </div>
        );

      case "official_person":
        return (
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <h3 className="text-2xl font-semibold mb-4 text-yellow-700">👮‍♂️ Official Person Details</h3>
            <p><strong>Name:</strong> {userInfo.name}</p>
            <p><strong>Role:</strong> {userInfo.officialRole || "N/A"}</p>
            <p><strong>Hall Name:</strong> {hallName}</p>
          </div>
        );

      case "dining_shop_canteen":
        return (
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <h3 className="text-2xl font-semibold mb-4 text-green-700">🍽️ Dining / Shop / Canteen Details</h3>
            <p><strong>Name:</strong> {userInfo.name}</p>
            <p><strong>Hall Name:</strong> {hallName}</p>
            <p><strong>Role:</strong> {userInfo.role}</p>
          </div>
        );

      default:
        return <p className="text-gray-700">No dashboard data available for this role.</p>;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex justify-center items-center">
        <p className="text-lg text-gray-700">Loading user data...</p>
      </div>
    );
  }

  if (!userInfo) {
    return (
      <div className="min-h-screen flex justify-center items-center">
        <p className="text-lg text-red-600">User data not found or not logged in.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-tr from-gray-100 to-blue-50 p-10">
      <div className="max-w-7xl mx-auto grid gap-8 grid-cols-1 md:grid-cols-3">
        {/* Profile Card */}
        <div className="bg-white p-6 rounded-xl shadow-md col-span-1 flex flex-col items-center text-center">
          <img
            src={userInfo.profilePicture}
            alt="Profile"
            onError={(e) => {
              e.target.src = "https://via.placeholder.com/150";
            }}
            className="rounded-full w-36 h-36 object-cover border mb-4"
          />
          <h2 className="text-2xl font-bold mb-1">{userInfo.name}</h2>
          <p className="text-gray-600">📧 {userInfo.email}</p>
          <p className="text-gray-600">📱 {userInfo.phone}</p>
          <p className="text-gray-600">🩸 Blood Group: {userInfo.bloodGroup}</p>
          <p className="text-gray-600">🏛️ Hall: {hallName}</p>
          <p className="text-gray-600">🔑 Role: {userInfo.role}</p>

          {userInfo.role === "student" && (
            <>
              <p className="text-gray-600">📘 Department: {userInfo.department.toUpperCase()}</p>
              <p className="text-gray-600">🎓 Semester: {userInfo.semester}</p>
              <p className="text-gray-600">🏠 Room No: {userInfo.roomNumber || "N/A"}</p>
            </>
          )}

          <input
            type="file"
            accept="image/*"
            onChange={handleProfilePicChange}
            className="mt-4 text-sm cursor-pointer"
          />
        </div>

        {/* Dashboard Info */}
        <div className="bg-white p-6 rounded-xl shadow-md col-span-2">
          <h1 className="text-3xl font-bold mb-4">📊 Dashboard Overview</h1>
          {renderDashboardDetails()}
        </div>
      </div>
    </div>
  );
};

export default DashboardHome;
