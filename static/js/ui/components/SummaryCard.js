const accentMap = {
    indigo: { bg: 'bg-primary-500/10', text: 'text-primary-400', border: 'border-primary-500/20' },
    green: { bg: 'bg-emerald-500/10', text: 'text-emerald-400', border: 'border-emerald-500/20' },
    red: { bg: 'bg-red-500/10', text: 'text-red-400', border: 'border-red-500/20' },
    amber: { bg: 'bg-amber-500/10', text: 'text-amber-400', border: 'border-amber-500/20' },
};

const SummaryCard = ({ title, value, icon, accent = 'indigo' }) => {
  const a = accentMap[accent] || accentMap.indigo;
  return `
    <div class="card p-4 lg:p-5 flex flex-col gap-3">
      <div class="flex items-center justify-between">
        <div class="p-2.5 rounded-lg ${a.bg} ${a.text}">${icon}</div>
      </div>
      <div>
        <p class="text-xs font-medium text-surface-400 uppercase tracking-wider">${title}</p>
        <p class="stat-value text-xl lg:text-2xl font-bold text-surface-50 mt-1">${value}</p>
      </div>
    </div>
  `;
};

export default SummaryCard;