const icon = (svgContent, props = {}) => {
  const attributes = Object.entries(props)
    .map(([key, value]) => {
      if (key === 'className') return `class="${value}"`;
      const k = key.replace(/([A-Z])/g, g => `-${g[0].toLowerCase()}`);
      return `${k}="${value}"`;
    })
    .join(' ');
  if (attributes) return svgContent.replace('<svg ', `<svg ${attributes} `);
  return svgContent;
};

const s = (p) => `stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"`;

export const ChartBarIcon = (p) => icon(`<svg ${s()}><path d="M3 13a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><path d="M9 9a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1z"/><path d="M15 5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1z"/></svg>`, p);
export const CheckCircleIcon = (p) => icon(`<svg ${s()}><circle cx="12" cy="12" r="9"/><path d="M9 12l2 2 4-4"/></svg>`, p);
export const XCircleIcon = (p) => icon(`<svg ${s()}><circle cx="12" cy="12" r="9"/><path d="M10 10l4 4m0-4l-4 4"/></svg>`, p);
export const XMarkIcon = (p) => icon(`<svg ${s()}><path d="M18 6l-12 12"/><path d="M6 6l12 12"/></svg>`, p);
export const CalendarDaysIcon = (p) => icon(`<svg ${s()}><rect x="4" y="5" width="16" height="16" rx="2"/><path d="M16 3v4M8 3v4M4 11h16"/><path d="M11 15h1v3"/></svg>`, p);
export const UserCircleIcon = (p) => icon(`<svg ${s()}><circle cx="12" cy="12" r="9"/><circle cx="12" cy="10" r="3"/><path d="M6.168 18.849A4 4 0 0 1 10 16h4a4 4 0 0 1 3.834 2.855"/></svg>`, p);
export const WalletIcon = (p) => icon(`<svg ${s()}><path d="M17 8V5a1 1 0 0 0-1-1H6a2 2 0 0 0 0 4h12a1 1 0 0 1 1 1v3m0 4v3a1 1 0 0 1-1 1H6a2 2 0 0 1-2-2V6"/><path d="M20 12v4h-4a2 2 0 1 1 0-4h4z"/></svg>`, p);
export const ArrowTrendingUpIcon = (p) => icon(`<svg ${s()}><path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/></svg>`, p);
export const ArrowTrendingDownIcon = (p) => icon(`<svg ${s()}><path d="M3 7l6 6 4-4 8 8"/><path d="M14 17h7v-7"/></svg>`, p);
export const ArrowUpCircleIcon = (p) => icon(`<svg ${s()}><circle cx="12" cy="12" r="9"/><path d="M12 8l-4 4"/><path d="M12 8v8"/><path d="M16 12l-4-4"/></svg>`, p);
export const ArrowDownCircleIcon = (p) => icon(`<svg ${s()}><circle cx="12" cy="12" r="9"/><path d="M8 12l4 4"/><path d="M12 16V8"/><path d="M16 12l-4 4"/></svg>`, p);
export const HomeIcon = (p) => icon(`<svg ${s()}><path d="M5 12l-2 0 9-9 9 9-2 0"/><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/><path d="M9 21v-6a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v6"/></svg>`, p);
export const BookOpenIcon = (p) => icon(`<svg ${s()}><path d="M3 19a9 9 0 0 1 9 0 9 9 0 0 1 9 0"/><path d="M3 6a9 9 0 0 1 9 0 9 9 0 0 1 9 0"/><path d="M3 6v13"/><path d="M12 6v13"/><path d="M21 6v13"/></svg>`, p);
export const MagnifyingGlassIcon = (p) => icon(`<svg ${s()}><circle cx="10" cy="10" r="7"/><path d="M21 21l-6-6"/></svg>`, p);
export const PencilSquareIcon = (p) => icon(`<svg ${s()}><path d="M7 7H6a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2v-1"/><path d="M20.385 6.585a2.1 2.1 0 0 0-2.97-2.97L9 12v3h3l8.385-8.415z"/><path d="M16 5l3 3"/></svg>`, p);
export const BoltIcon = (p) => icon(`<svg ${s()}><path d="M13 3v7h6l-8 11v-7H5l8-11z"/></svg>`, p);
export const BuildingLibraryIcon = (p) => icon(`<svg ${s()}><path d="M3 21h18"/><path d="M3 10h18"/><path d="M5 6l7-3 7 3"/><path d="M4 10v11"/><path d="M20 10v11"/><path d="M8 14v3"/><path d="M12 14v3"/><path d="M16 14v3"/></svg>`, p);
export const CogIcon = (p) => icon(`<svg ${s()}><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09a1.65 1.65 0 0 0-1.08-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09a1.65 1.65 0 0 0 1.51-1.08 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1.08 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9c.26.604.852.997 1.51 1.08H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1.08z"/></svg>`, p);
export const PlayCircleIcon = (p) => icon(`<svg ${s()}><circle cx="12" cy="12" r="9"/><path d="M10 8l6 4-6 4z"/></svg>`, p);
export const StopCircleIcon = (p) => icon(`<svg ${s()}><circle cx="12" cy="12" r="9"/><rect x="9" y="9" width="6" height="6" rx="1"/></svg>`, p);
export const ListBulletIcon = (p) => icon(`<svg ${s()}><path d="M9 6h11"/><path d="M9 12h11"/><path d="M9 18h11"/><circle cx="5" cy="6" r=".5" fill="currentColor"/><circle cx="5" cy="12" r=".5" fill="currentColor"/><circle cx="5" cy="18" r=".5" fill="currentColor"/></svg>`, p);
export const InformationCircleIcon = (p) => icon(`<svg ${s()}><circle cx="12" cy="12" r="9"/><path d="M12 16v-4"/><circle cx="12" cy="8" r=".5" fill="currentColor"/></svg>`, p);
export const SunIcon = (p) => icon(`<svg ${s()}><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2m-10-10h2m16 0h2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M4.93 19.07l1.41-1.41m11.32-11.32l1.41-1.41"/></svg>`, p);
export const MoonIcon = (p) => icon(`<svg ${s()}><path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446A9 9 0 1 1 12 2.992z"/></svg>`, p);
export const ArrowRightOnRectangleIcon = (p) => icon(`<svg ${s()}><path d="M14 8V6a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2-2v-2"/><path d="M9 12h12l-3-3"/><path d="M18 15l3-3"/></svg>`, p);
export const Bars3Icon = (p) => icon(`<svg ${s()}><path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/></svg>`, p);
export const ShieldCheckIcon = (p) => icon(`<svg ${s()}><path d="M12 3a12 12 0 0 0 8.5 3 12 12 0 0 1-8.5 15A12 12 0 0 1 3.5 6 12 12 0 0 0 12 3z"/><path d="M9 12l2 2 4-4"/></svg>`, p);
export const TrashIcon = (p) => icon(`<svg ${s()}><path d="M4 7h16"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2l1-12"/><path d="M9 7V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v3"/></svg>`, p);
export const EyeIcon = (p) => icon(`<svg ${s()}><path d="M10 12a2 2 0 1 0 4 0 2 2 0 0 0-4 0"/><path d="M21 12c-2.4 4-5.4 6-9 6s-6.6-2-9-6c2.4-4 5.4-6 9-6s6.6 2 9 6z"/></svg>`, p);
export const ArrowPathIcon = (p) => icon(`<svg ${s()}><path d="M20 11a8.1 8.1 0 0 0-15.5-2m-.5-4v4h4"/><path d="M4 13a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4"/></svg>`, p);
export const PlusIcon = (p) => icon(`<svg ${s()}><path d="M12 5v14"/><path d="M5 12h14"/></svg>`, p);
export const ExclamationTriangleIcon = (p) => icon(`<svg ${s()}><path d="M12 9v4"/><path d="M10.363 3.591l-8.106 13.534a1.914 1.914 0 0 0 1.636 2.875h16.214a1.914 1.914 0 0 0 1.636-2.875l-8.106-13.534a1.914 1.914 0 0 0-3.274 0z"/><circle cx="12" cy="16" r=".5" fill="currentColor"/></svg>`, p);
export const ClockIcon = (p) => icon(`<svg ${s()}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>`, p);
export const ActivityIcon = (p) => icon(`<svg ${s()}><path d="M3 12h4l2-9 4 18 2-9h4"/></svg>`, p);
export const ClipboardIcon = (p) => icon(`<svg ${s()}><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><path d="M9 14l2 2 4-4"/></svg>`, p);
