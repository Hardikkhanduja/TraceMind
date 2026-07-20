import { Outlet } from "react-router-dom";

import MobileSidebar from "./MobileSidebar";
import PageContainer from "./PageContainer";
import Sidebar from "./Sidebar";

const AppShell = () => {
  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />

      <MobileSidebar />

      <PageContainer>
        <Outlet />
      </PageContainer>
    </div>
  );
};

export default AppShell;