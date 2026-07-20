import { type LucideIcon } from "lucide-react";
import { NavLink } from "react-router-dom";

import { cn } from "@/lib/utils";

interface SidebarItemProps {
  icon: LucideIcon;
  label: string;
  path: string;
  collapsed?: boolean;
}

const SidebarItem = ({
  icon: Icon,
  label,
  path,
  collapsed = false,
}: SidebarItemProps) => {
  return (
    <NavLink
      to={path}
      className={({ isActive }) =>
        cn(
          "flex items-center gap-3 rounded-xl px-3 py-3 transition-all duration-200",
          isActive
            ? "bg-blue-500/10 text-blue-400"
            : "text-zinc-400 hover:bg-zinc-900 hover:text-white"
        )
      }
    >
      <Icon size={20} />

      {!collapsed && (
        <span className="font-medium">
          {label}
        </span>
      )}
    </NavLink>
  );
};

export default SidebarItem;