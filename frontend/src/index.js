import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { UserProvider } from "./components/UserContext.js";
import GuestRoute from "./components/GuestRoute.js";
import AuthForm from "./components/AuthForm.js";
import BookingComponent from "./components/BookingComponent.js";
import AllRooms from "./components/AllRooms.js";
import OccupiedDatesDisplay from "./components/OccupiedDatesDisplay.js";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App></App>,
    children: [
      { path: "/", element: <BookingComponent></BookingComponent> },
      {
        path: "/all-rooms",
        element: <AllRooms></AllRooms>,
      },
      {
        path: "/auth",
        element: (
          <GuestRoute>
            <AuthForm></AuthForm>
          </GuestRoute>
        ),
      },
      {
        path: "/my-bookings",
        element: <OccupiedDatesDisplay></OccupiedDatesDisplay>,
      },
    ],
  },
]);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <UserProvider>
      <RouterProvider router={router} />
    </UserProvider>
  </React.StrictMode>,
);
