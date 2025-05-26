export interface MenuItem {
  path: string;
  label: string;
  icon?: string; // PrimeIcons are typically strings like 'pi pi-fw pi-home'
}

export const menuItems: MenuItem[] = [
  { path: "/transcriber", label: "Transcriber", icon: "pi pi-fw pi-youtube" },
  {
    path: "/reddit-scraper",
    label: "Reddit Scraper",
    icon: "pi pi-fw pi-reddit",
  },
  // Add more items here
  // { path: "/summarizer", label: "Summarizer Tool", icon: "pi pi-fw pi-book" },
];
