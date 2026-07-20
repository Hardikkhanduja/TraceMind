import Logo from "@/components/Logo";
import { navigationItems } from "@/constants/navigation";
import SidebarItem from "./SidebarItem";

const Sidebar = () => {
  return (
    <aside
      style={{
        width: "var(--sidebar-width)",
      }}
      className="hidden md-flex w-72 flex-col border-r border-zinc-800 bg-zinc-950/60 backdrop-blur-xl p-5"
    >
      <Logo />

      <nav className="mt-10 flex flex-col gap-2">
        {navigationItems.map((item) => (
          <SidebarItem
            key={item.path}
            icon={item.icon}
            label={item.label}
            path={item.path}
          />
        ))}
      </nav>

      <div className="mt-auto text-xs text-zinc-500">TraceMind v1.0</div>
    </aside>
  );
};

export default Sidebar;
