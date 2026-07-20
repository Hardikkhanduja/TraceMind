import { LayoutDashboard, Search, History, Settings } from "lucide-react";
import { type LucideIcon } from "lucide-react";

interface NavigationItem {
    icon: LucideIcon;
    label: string;
    path: string;
}

export const navigationItems: NavigationItem[] = [
    { icon: LayoutDashboard, label: "Dashboard", path: "/" },
    { icon: Search, label: "Investigation", path: "/investigation" },
    { icon: History, label: "History", path: "/history" },
    { icon: Settings, label: "Settings", path: "/settings" },
];
