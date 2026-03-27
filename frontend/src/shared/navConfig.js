/** @type {{ title: string | null, items: { to: string; label: string; short: string }[] }[]} */
export const NAV_SECTIONS = [
  {
    title: null,
    items: [{ to: '/dashboard', label: 'Dashboard', short: 'Home' }],
  },
  {
    title: 'Your land',
    items: [
      { to: '/farms', label: 'Farms', short: 'Farms' },
      { to: '/fields', label: 'Fields', short: 'Fields' },
    ],
  },
  {
    title: 'Field data',
    items: [
      { to: '/soil', label: 'Soil', short: 'Soil' },
      { to: '/weather', label: 'Weather', short: 'Weather' },
    ],
  },
  {
    title: 'Decisions',
    items: [
      { to: '/recommendations', label: 'Recommendations', short: 'Crops' },
      { to: '/chat', label: 'Assistant', short: 'Chat' },
    ],
  },
]

export const NAV_ITEMS = NAV_SECTIONS.flatMap((s) => s.items)
