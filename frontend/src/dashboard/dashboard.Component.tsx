import React, { useState } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { menuItems as appMenuItems } from "./components/menuConfig.component";
import type { MenuItem as AppMenuItem } from "./components/menuConfig.component";

import { Sidebar } from "primereact/sidebar";
import { Button } from "primereact/button";
import { PanelMenu } from "primereact/panelmenu";
import { Toolbar } from "primereact/toolbar";
import type {
  MenuItem as PrimeMenuItem,
  MenuItemOptions,
} from "primereact/menuitem";

import "./dashboard.styles.css";

// --- NEW COLOR PALETTE (Inspired by the image) ---
const SIDEBAR_BACKGROUND = "#4A55A2"; // Example: A deep indigo/purple
const SIDEBAR_TEXT_INACTIVE = "#A0AEC0"; // Example: Medium light grey for inactive text
const SIDEBAR_TEXT_ACTIVE = "#4A55A2"; // Example: Sidebar color for active text (on light background)
const SIDEBAR_BACKGROUND_ACTIVE = "#FFFFFF"; // Example: White background for active item
const SIDEBAR_ACTIVE_BORDER_COLOR = "#4A55A2"; // For the left border of the active item

const MAIN_APP_NAME_COLOR = "#FFFFFF"; // White for "Chrono Odyssey AI" in the new sidebar header
const MAIN_PAGE_TITLE_COLOR = "#2D3748"; // Dark grey for page title in toolbar

// --- Existing constants (can be removed or updated if not used elsewhere) ---
// const NEW_ACTIVE_COLOR = "#3B82F6";
// const ACTIVE_BACKGROUND_COLOR = "#e9ecef";
// const DEFAULT_TEXT_COLOR = "#000000";

const DashboardComponent: React.FC = () => {
  const [sidebarVisible, setSidebarVisible] = useState(true);
  const location = useLocation();
  const navigate = useNavigate();

  const primeNavigationItems: PrimeMenuItem[] = appMenuItems.map(
    (item: AppMenuItem): PrimeMenuItem => {
      const isActive = location.pathname.startsWith(item.path);

      const linkStyle: React.CSSProperties = {
        display: "flex",
        alignItems: "center",
        width: "100%",
        padding: "0.85rem 1.25rem", // Adjusted padding for a slightly more spacious feel
        boxSizing: "border-box",
        textDecoration: "none",
        transition: "background-color 0.2s, color 0.2s, border-left-color 0.2s",
        borderLeft: `4px solid ${
          isActive ? SIDEBAR_ACTIVE_BORDER_COLOR : "transparent"
        }`,
        position: "relative",
        borderRadius: "6px", // Apply border-radius directly here for the background
        ...(isActive
          ? {
              background: SIDEBAR_BACKGROUND_ACTIVE,
              color: SIDEBAR_TEXT_ACTIVE,
              fontWeight: "600",
            }
          : {
              background: "transparent",
              color: SIDEBAR_TEXT_INACTIVE,
              fontWeight: "normal",
            }),
      };

      const itemTemplate = (
        menuItem: PrimeMenuItem,
        options: MenuItemOptions
      ) => {
        const isHeader = !!menuItem.items && menuItem.items.length > 0;
        const currentItemIsActive = location.pathname.startsWith(
          menuItem.id || item.path
        );

        const iconEffectiveStyle: React.CSSProperties = {
          marginRight: "0.75rem",
          color: currentItemIsActive
            ? SIDEBAR_TEXT_ACTIVE
            : SIDEBAR_TEXT_INACTIVE,
        };
        const labelEffectiveStyle: React.CSSProperties = {
          color: currentItemIsActive
            ? SIDEBAR_TEXT_ACTIVE
            : SIDEBAR_TEXT_INACTIVE,
        };
        // This style will be used for our manually rendered submenu icon
        const submenuIconEffectiveStyle: React.CSSProperties = {
          marginLeft: "auto",
          color: currentItemIsActive
            ? SIDEBAR_TEXT_ACTIVE
            : SIDEBAR_TEXT_INACTIVE,
        };

        const templateLinkStyle: React.CSSProperties = {
          display: "flex",
          alignItems: "center",
          width: "100%",
          padding: "0.85rem 1.25rem",
          boxSizing: "border-box",
          textDecoration: "none",
          transition:
            "background-color 0.2s, color 0.2s, border-left-color 0.2s",
          borderLeft: `4px solid ${
            currentItemIsActive ? SIDEBAR_ACTIVE_BORDER_COLOR : "transparent"
          }`,
          position: "relative",
          borderRadius: "6px",
          margin: "0.25rem 0.5rem",
          ...(currentItemIsActive
            ? {
                background: SIDEBAR_BACKGROUND_ACTIVE,
                color: SIDEBAR_TEXT_ACTIVE,
                fontWeight: "600",
              }
            : {
                background: "transparent",
                color: SIDEBAR_TEXT_INACTIVE,
                fontWeight: "normal",
              }),
        };

        return (
          <a
            href={menuItem.url || "#"}
            className={`${options.className} menu-item-link`}
            onClick={(e) => options.onClick(e)}
            style={templateLinkStyle}
            role={isHeader ? "button" : "menuitem"}
            aria-label={menuItem.label}
            tabIndex={0}
          >
            {options.iconClassName && (
              <span
                className={options.iconClassName}
                style={iconEffectiveStyle}
              ></span>
            )}
            {options.labelClassName && (
              <span
                className={options.labelClassName}
                style={labelEffectiveStyle}
              >
                {menuItem.label}
              </span>
            )}
            {/* Manually render submenu icon if it's a header */}
            {isHeader && (
              <span
                className="pi pi-angle-down" // Or pi-chevron-down, adjust as preferred
                style={submenuIconEffectiveStyle}
              ></span>
            )}
          </a>
        );
      };

      return {
        id: item.path,
        label: item.label,
        icon: item.icon || "pi pi-fw pi-bars",
        command: () => {
          navigate(item.path);
        },
        template: itemTemplate,
      };
    }
  );

  const currentRouteItem = appMenuItems.find((item) =>
    location.pathname.startsWith(item.path)
  );
  const pageTitle = currentRouteItem ? currentRouteItem.label : "Dashboard";

  // Toolbar will need significant changes to match the image's header style
  // For now, let's just update its text color
  const toolbarStartContent = (
    <div className="flex align-items-center">
      <Button
        icon="pi pi-bars"
        className="p-button-rounded p-button-text p-mr-2"
        onClick={() => setSidebarVisible(!sidebarVisible)}
        style={{ color: MAIN_PAGE_TITLE_COLOR }} // Adjust hamburger icon color
      />
      {/* App name might move into the sidebar header */}
    </div>
  );

  const toolbarCenterContent = (
    <span
      className="text-lg font-semibold"
      style={{ color: MAIN_PAGE_TITLE_COLOR }}
    >
      {pageTitle}
    </span>
  );

  return (
    <div className="dashboard-layout">
      <Sidebar
        visible={sidebarVisible}
        onHide={() => setSidebarVisible(false)}
        modal={false}
        className="dashboard-primereact-sidebar new-theme-sidebar" // Add new class for CSS
        style={{
          width: "260px", // Adjust as needed
          background: SIDEBAR_BACKGROUND, // New sidebar background
          borderRight: "none", // Remove border if not in new design
        }}
        showCloseIcon={false}
      >
        {/* Placeholder for Logo and App Name */}
        <div
          className="sidebar-app-header p-p-3"
          style={{
            display: "flex",
            alignItems: "center",
            // borderBottom: `1px solid ${SIDEBAR_TEXT_INACTIVE}`, // Optional separator
            paddingBottom: "1rem",
            marginBottom: "0.5rem",
          }}
        >
          {/* <img src="/path-to-your-logo.png" alt="Logo" style={{height: "30px", marginRight: '10px'}} /> */}
          <span
            className="text-xl font-bold"
            style={{ color: MAIN_APP_NAME_COLOR }}
          >
            Chrono Odyssey AI
          </span>
        </div>
        <PanelMenu
          model={primeNavigationItems}
          className="w-full new-theme-panelmenu"
        />{" "}
        {/* Add new class */}
        {/* Placeholder for User Profile / Upgrade section at the bottom */}
        <div
          className="sidebar-footer-placeholder"
          style={{ marginTop: "auto", padding: "1rem" }}
        >
          {/* Content for user profile or upgrade button */}
        </div>
      </Sidebar>

      <div
        className="dashboard-main-content"
        style={{
          marginLeft: sidebarVisible ? "260px" : "0px",
          transition: "margin-left 0.2s ease-in-out",
          // background: MAIN_CONTENT_BACKGROUND, // Will be set in CSS
        }}
      >
        <Toolbar
          className="app-header p-p-2 new-theme-toolbar" // Add new class
          style={{
            // background: "#ffffff", // White background for new header style
            // borderBottom: "1px solid #e2e8f0", // Light border
            // color: MAIN_PAGE_TITLE_COLOR,
            position: "sticky",
            top: 0,
            zIndex: 1000,
          }}
          start={toolbarStartContent}
          center={toolbarCenterContent}
        />
        <main className="dashboard-content-area p-p-3">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardComponent;
