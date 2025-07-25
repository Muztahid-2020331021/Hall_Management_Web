import React, { useEffect, useState } from "react";
import axios from "axios";

const BLOOD_GROUP_LABELS = {
  'A+': 'A(+ve)',
  'A-': 'A(-ve)',
  'B+': 'B(+ve)',
  'B-': 'B(-ve)',
  'AB+': 'AB(+ve)',
  'AB-': 'AB(-ve)',
  'O+': 'O(+ve)',
  'O-': 'O(-ve)',
  'Others': 'Others',
};

const BloodBank = () => {
  const [donors, setDonors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDonor, setSelectedDonor] = useState(null);
  const [newDate, setNewDate] = useState("");
  const [updating, setUpdating] = useState(false);

  const loggedInEmail = localStorage.getItem("userEmail");

  useEffect(() => {
    const fetchDonors = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/blood_bank/donors/");
        setDonors(response.data.results || response.data);
      } catch (error) {
        console.error("Error fetching donors:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDonors();
  }, []);

  const groupByBloodGroup = (donors) => {
    const grouped = {};
    Object.keys(BLOOD_GROUP_LABELS).forEach((group) => {
      grouped[group] = donors.filter((donor) => donor.blood_group === group);
    });
    return grouped;
  };

  const handleUpdateClick = (donor) => {
    setSelectedDonor(donor);
    setNewDate(""); // reset previous input
  };

  const handleUpdateSubmit = async () => {
    if (!newDate || !selectedDonor) return;
    setUpdating(true);

    try {
      await axios.patch(`http://127.0.0.1:8000/blood_bank/donors/${selectedDonor.id}/`, {
        last_donation_date: newDate,
      });

      // Refresh donors
      const response = await axios.get("http://127.0.0.1:8000/blood_bank/donors/");
      setDonors(response.data.results || response.data);

      // Clear modal
      setSelectedDonor(null);
    } catch (error) {
      console.error("Update failed:", error);
    } finally {
      setUpdating(false);
    }
  };

  const groupedDonors = groupByBloodGroup(donors);

  if (loading) return <div className="text-center mt-10 text-lg">Loading donors...</div>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6 text-center text-red-700">Blood Donor Directory</h1>

      {Object.entries(groupedDonors).map(([bloodGroup, donorsInGroup]) => (
        <div key={bloodGroup} className="mb-10">
          <h2 className="text-xl font-semibold mb-2 text-white bg-red-600 px-4 py-2 rounded-md w-fit shadow">
            {BLOOD_GROUP_LABELS[bloodGroup]} Group
          </h2>

          {donorsInGroup.length === 0 ? (
            <p className="text-gray-500 italic ml-4">No donors available</p>
          ) : (
            <div className="overflow-x-auto mt-2">
              <table className="table-auto w-full border border-gray-300 shadow-md bg-white">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="px-4 py-2 border">Name</th>
                    <th className="px-4 py-2 border">Email</th>
                    <th className="px-4 py-2 border">Phone</th>
                    <th className="px-4 py-2 border">Role</th>
                    <th className="px-4 py-2 border">Department</th>
                    <th className="px-4 py-2 border">Last Donation</th>
                    <th className="px-4 py-2 border">Willing</th>
                    {donorsInGroup.some(d => d.email === loggedInEmail) && (
                      <th className="px-4 py-2 border">Action</th>
                    )}

                  </tr>
                </thead>
                <tbody>
                  {donorsInGroup.map((donor) => (
                    <tr key={donor.id} className="hover:bg-gray-50">
                      <td className="px-4 py-2 border">{donor.full_name}</td>
                      <td className="px-4 py-2 border">{donor.email}</td>
                      <td className="px-4 py-2 border">{donor.phone}</td>
                      <td className="px-4 py-2 border capitalize">{donor.user_role.replace("_", " ")}</td>
                      <td className="px-4 py-2 border">{donor.department || "—"}</td>
                      <td className="px-4 py-2 border">{donor.last_donation_date || "Never"}</td>
                      <td className={`px-4 py-2 border font-medium ${donor.willing_to_donate ? "text-green-600" : "text-red-500"}`}>
                        {donor.willing_to_donate ? "Yes" : "No"}
                      </td>
                    {donor.email === loggedInEmail && (
                      <td className="px-4 py-2 border text-center">
                        <button
                          className="bg-blue-500 text-white px-3 py-1 text-sm rounded hover:bg-blue-600"
                          onClick={() => handleUpdateClick(donor)}
                        >
                          Update
                        </button>
                      </td>
                    )}
                    
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      ))}

      {/* Modal */}
      {selectedDonor && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white rounded-md p-6 w-full max-w-md shadow-lg">
            <h2 className="text-lg font-semibold mb-4 text-center">Update Donation Date</h2>
            <p className="mb-2 text-sm text-gray-700">
              Updating for: <strong>{selectedDonor.full_name}</strong>
            </p>
            <input
              type="date"
              className="w-full border px-3 py-2 rounded mb-4"
              value={newDate}
              onChange={(e) => setNewDate(e.target.value)}
            />
            <div className="flex justify-end gap-3">
              <button
                className="px-4 py-2 rounded bg-gray-400 text-white hover:bg-gray-500"
                onClick={() => setSelectedDonor(null)}
              >
                Cancel
              </button>
              <button
                className={`px-4 py-2 rounded text-white ${
                  updating ? "bg-blue-300" : "bg-blue-600 hover:bg-blue-700"
                }`}
                onClick={handleUpdateSubmit}
                disabled={updating}
              >
                {updating ? "Updating..." : "Update"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BloodBank;
