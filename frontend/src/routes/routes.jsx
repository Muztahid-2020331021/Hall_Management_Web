// routes/routes.jsx
import React from 'react'
import { createBrowserRouter } from 'react-router-dom'  // ✅ correct import
import Login from '../pages/Login'
import ApplyForm from '../pages/ApplyForm'
import Main from '../Layout/Main'
import DashboardLayout from '../Layout/DashboardLayout'
import NotFoundPage from '../pages/NotFoundPage'
import DashboardHome from '../pages/DashboardHome'
import Menu from '../pages/student/Menu'
import Notices from '../pages/Notices'
import Complaints from '../pages/student/Complaints'
import LostFoundItems from '../pages/student/LostFoundItems'
import ManageNotices from '../pages/official_stuff/ManageNotices'
import ManageComplaints from '../pages/official_stuff/ManageComplaints'
import HallApplicants from '../pages/official_stuff/HallApplicants'
import ManageStudents from '../pages/official_stuff/ManageStudents'
import Meetings from '../pages/official_stuff/Meetings'
import ManageMenu from '../pages/dining_canteen/ManageMenu'
import Reviews from '../pages/dining_canteen/Reviews'
import BloodBank from '../pages/BloodBank'
import Forum from '../pages/Forum'
import OfficialContact from '../pages/OfficialContact'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Main />,
    children: [
      { index: true, element: <Login /> },
      { path: 'apply', element: <ApplyForm /> },
    ],
  },
  {
    path: '/dashboard',
    element: <DashboardLayout />,
    children: [
      { index: true, element: <DashboardHome /> },
      { path: 'forum', element: <Forum /> },
      { path: 'blood-bank', element: <BloodBank /> },
      { path: 'official-contact', element: <OfficialContact /> },
      { path: 'menu', element: <Menu /> },
      { path: 'complaints', element: <Complaints /> },
      { path: 'lost-found-items', element: <LostFoundItems /> },
      { path: 'manage-hall-applicants', element: <HallApplicants /> },
      { path: 'manage-complaints', element: <ManageComplaints /> },
      { path: 'manage-notices', element: <ManageNotices /> },
      { path: 'manage-students', element: <ManageStudents /> },
      { path: 'meetings', element: <Meetings /> },
      { path: 'manage-menu', element: <ManageMenu /> },
      { path: 'reviews', element: <Reviews /> },
      { path: 'notices', element: <Notices /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
  {
    path: '*',
    element: <Main><NotFoundPage /></Main>,
  },
])
