import { createBrowserRouter } from "react-router-dom";

import AppShell from "@/components/layout/AppShell";

import Dashboard from "@/pages/Dashboard/Dashboard";
import History from "@/pages/History/History";
import Investigation from "@/pages/Investigation/Investigation";
import Settings from "@/pages/Settings/Settings";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppShell />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: "investigation",
        element: <Investigation />,
      },
      {
        path: "history",
        element: <History />,
      },
      {
        path: "settings",
        element: <Settings />,
      },
    ],
  },
]);