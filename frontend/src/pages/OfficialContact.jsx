// import React, { useEffect, useState } from 'react';
// import { FaWhatsapp } from 'react-icons/fa';

// const OfficialCard = ({ official }) => {
//   const {
//     profile_picture,
//     name,
//     official_role,
//     provost_body_role,
//     university_profile,
//     user_role,
//     email,
//     phone_number,
//     blood_group,
//     id,
//   } = official;

//   const openWhatsApp = (phone) => {
//     if (!phone) {
//       alert("No phone number available");
//       return;
//     }
//     const formattedPhone = phone.replace(/\D/g, '');
//     const whatsappURL = `https://wa.me/${formattedPhone}`;

//     const newWindow = window.open(whatsappURL, '_blank');

//     const timeout = setTimeout(() => {
//       alert("WhatsApp not detected or failed to open. Please ensure WhatsApp is installed.");
//     }, 2000);

//     if (newWindow) {
//       clearTimeout(timeout);
//     }
//   };

//   return (
//     <div key={id} className="bg-white shadow-md rounded-2xl p-4 flex flex-col items-center text-center space-y-2">
//       <img
//         src={profile_picture || '/default-profile.png'}
//         alt={name || 'Profile'}
//         className="w-24 h-24 rounded-full object-cover border-2 border-gray-300"
//         onError={(e) => (e.target.src = '/default-profile.png')}
//       />

//       <div className="font-semibold text-lg">{name}</div>

//       {official_role && (
//         <div className="text-sm text-gray-600">{official_role.toUpperCase()}</div>
//       )}
//       {provost_body_role && (
//         <div className="text-sm text-gray-600">{provost_body_role.toUpperCase()}</div>
//       )}

//       {user_role === "provost_body" && university_profile && (
//         <a
//           href={university_profile}
//           target="_blank"
//           rel="noopener noreferrer"
//           className="text-sm text-blue-600 underline hover:text-blue-800"
//         >
//           View University Profile
//         </a>
//       )}

//       <div className="text-gray-600 text-sm">{email}</div>

//       <button
//         onClick={() => openWhatsApp(phone_number)}
//         className="flex items-center gap-2 text-green-600 text-sm hover:underline focus:outline-none"
//       >
//         <FaWhatsapp className="text-xl" />
//         {phone_number}
//       </button>

//       <div className="text-sm text-gray-600">Blood Group: {blood_group}</div>
//     </div>
//   );
// };

// const OfficialContact = () => {
//   const [officials, setOfficials] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   const fetchOfficials = async () => {
//     try {
//       const res = await fetch("http://127.0.0.1:8000/official/official_registration/");
//       if (!res.ok) throw new Error("Failed to fetch data");
//       const data = await res.json();
//       setOfficials(data?.results || []);
//     } catch (err) {
//       console.error(err);
//       setError(err.message);
//     }
//     setLoading(false);
//   };

//   useEffect(() => {
//     fetchOfficials();
//   }, []);

//   if (loading) {
//     return (
//       <div className="text-center py-10 text-blue-600 font-semibold">
//         Loading official data...
//       </div>
//     );
//   }

//   if (error) {
//     return (
//       <div className="text-center py-10 text-red-600 font-semibold">
//         Error: {error}
//       </div>
//     );
//   }

//   return (
//     <div className="p-6 max-w-7xl mx-auto">
//       <h2 className="text-2xl font-bold text-center mb-6">Official Contact List</h2>
//       <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
//         {officials.map((official) => (
//           <OfficialCard key={official.id || official.email} official={official} />
//         ))}
//       </div>
//     </div>
//   );
// };

// export default OfficialContact;


import React, { useEffect, useState } from 'react';
import { FaWhatsapp } from 'react-icons/fa';

const OfficialCard = ({ official }) => {
  const {
    profile_picture,
    name,
    official_role,
    provost_body_role,
    university_profile,
    user_role,
    email,
    phone_number,
    blood_group,
    hall_id,
    id,
  } = official;

  const openWhatsApp = (phone) => {
    const formattedPhone = phone?.replace(/\D/g, '');
    const whatsappURL = `https://wa.me/${formattedPhone}`;

    const newWindow = window.open(whatsappURL, '_blank');

    const timeout = setTimeout(() => {
      alert("❌ WhatsApp not detected or failed to open. Please ensure WhatsApp is installed.");
    }, 2000);

    if (newWindow) {
      clearTimeout(timeout);
    }
  };

  return (
    <div className="bg-white shadow-md rounded-2xl p-4 flex flex-col items-center text-center space-y-2">
      <img
        src={profile_picture || '/default-profile.png'}
        alt={name || 'Profile'}
        className="w-24 h-24 rounded-full object-cover border-2 border-gray-300"
        onError={(e) => (e.target.src = '/default-profile.png')}
      />

      <div className="font-semibold text-lg">{name}</div>

      {official_role && (
        <div className="text-sm text-gray-600">{official_role.toUpperCase()}</div>
      )}
      {provost_body_role && (
        <div className="text-sm text-gray-600">{provost_body_role.toUpperCase()}</div>
      )}

      {user_role === 'provost_body' && university_profile && (
        <a
          href={university_profile}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm text-blue-600 underline hover:text-blue-800"
        >
          View University Profile
        </a>
      )}

      <div className="text-gray-600 text-sm">{email}</div>

      {phone_number && (
        <button
          onClick={() => openWhatsApp(phone_number)}
          className="flex items-center gap-2 text-green-600 text-sm hover:underline focus:outline-none"
        >
          <FaWhatsapp className="text-xl" />
          {phone_number}
        </button>
      )}

      <div className="text-sm text-gray-600">Blood Group: {blood_group}</div>
    </div>
  );
};

const OfficialContact = () => {
  const [officials, setOfficials] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const userHallId = localStorage.getItem('userHallId');

  const fetchOfficials = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/official/official_registration/');
      if (!res.ok) throw new Error('Failed to fetch official data');
      const data = await res.json();

      // ✅ Filter by user's hall ID
      const filtered = (data.results || []).filter(
        (official) => String(official.hall) === String(userHallId)
        
      );
      console.log("userHallId", userHallId);
      console.log("Matching officials:", filtered);

      setOfficials(filtered);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOfficials();
  }, [userHallId]);

  if (loading) {
    return (
      <div className="text-center py-10 text-blue-600 font-semibold">
        Loading official contact list...
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-10 text-red-600 font-semibold">
        Error: {error}
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h2 className="text-2xl font-bold text-center mb-6">Official Contact List</h2>

      {officials.length === 0 ? (
        <div className="text-center text-gray-500">No officials found for your hall.</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {officials.map((official) => (
            <OfficialCard key={official.id || official.email} official={official} />
          ))}
        </div>
      )}
    </div>
  );
};

export default OfficialContact;
