interface QuestRoadmapSectionProps {
  dict: {
    badge: string;
    title: string;
    subtitle: string;
    node1Title: string;
    node1Tag: string;
    node1Status: string;
    node2Title: string;
    node2Tag: string;
    node2Status: string;
    node3Title: string;
    node3Tag: string;
    node3Status: string;
    node4Title: string;
    node4Tag: string;
    node4Status: string;
    rewardLabel: string;
  };
}

export function QuestRoadmapSection({ dict }: QuestRoadmapSectionProps) {
  const nodes = [
    {
      title: dict.node1Title,
      tag: dict.node1Tag,
      status: dict.node1Status,
      icon: "🌐",
      xp: "+250 XP",
      state: "complete",
      border: "border-emerald-500/40 shadow-[0_0_20px_rgba(34,197,94,0.2)]",
      badgeClass: "badge-pixel badge-pixel-level",
      dot: "bg-emerald-400",
    },
    {
      title: dict.node2Title,
      tag: dict.node2Tag,
      status: dict.node2Status,
      icon: "⚡",
      xp: "+400 XP",
      state: "active",
      border: "border-cyan-400/60 shadow-[0_0_25px_rgba(6,182,212,0.35)] quest-node-active",
      badgeClass: "badge-pixel badge-pixel-streak",
      dot: "bg-cyan-400 animate-ping",
    },
    {
      title: dict.node3Title,
      tag: dict.node3Tag,
      status: dict.node3Status,
      icon: "🛡️",
      xp: "+650 XP",
      state: "locked",
      border: "border-amber-500/30 shadow-[0_0_15px_rgba(245,158,11,0.15)]",
      badgeClass: "badge-pixel badge-pixel-quest",
      dot: "bg-amber-400",
    },
    {
      title: dict.node4Title,
      tag: dict.node4Tag,
      status: dict.node4Status,
      icon: "🏆",
      xp: "+1,200 XP",
      state: "capstone",
      border: "border-purple-500/40 shadow-[0_0_25px_rgba(168,85,247,0.25)]",
      badgeClass: "badge-pixel badge-pixel-trophy",
      dot: "bg-purple-400",
    },
  ];

  return (
    <section aria-labelledby="quest-roadmap-heading" className="w-full flex flex-col gap-8 pt-6">
      <div className="flex flex-col items-center text-center gap-2">
        <span className="badge-pixel badge-pixel-trophy">{dict.badge}</span>
        <h2
          id="quest-roadmap-heading"
          className="text-2xl font-bold tracking-tight text-white sm:text-3xl"
        >
          {dict.title}
        </h2>
        <p className="max-w-xl text-sm text-zinc-400 leading-relaxed">
          {dict.subtitle}
        </p>
      </div>

      {/* Campaign Roadmap Nodes */}
      <div className="relative w-full rounded-2xl border border-white/[0.08] bg-gradient-to-b from-[#090d18] to-[#060810] p-6 sm:p-10 shadow-2xl overflow-hidden">
        {/* Ambient Backlight Spotlight */}
        <div
          className="pointer-events-none absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 -z-10 h-[350px] w-[800px] rounded-full bg-emerald-500/10 blur-[130px]"
          aria-hidden="true"
        />

        {/* Horizontal Connector Line (Desktop) */}
        <div
          className="hidden lg:block absolute top-[88px] left-16 right-16 h-1 bg-gradient-to-r from-emerald-500 via-cyan-400 to-purple-500 shadow-[0_0_12px_rgba(52,211,153,0.5)] z-0"
          aria-hidden="true"
        />

        {/* Grid of Quest Nodes */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 relative z-10">
          {nodes.map((node, i) => (
            <div
              key={i}
              className={`flex flex-col justify-between rounded-xl bg-[#0b1220]/95 p-5 backdrop-blur-md transition-all duration-300 hover:-translate-y-1.5 ${node.border}`}
            >
              <div className="flex flex-col gap-3">
                {/* Node Level Pin & Status */}
                <div className="flex items-center justify-between">
                  <span className={node.badgeClass}>{node.tag}</span>
                  <span className="font-mono text-[11px] font-bold text-zinc-300 flex items-center gap-1.5">
                    <span className={`h-2 w-2 rounded-full ${node.dot}`} aria-hidden="true" />
                    {node.status}
                  </span>
                </div>

                {/* Node Icon & Title */}
                <div className="flex items-center gap-3 pt-2">
                  <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-black/50 text-2xl border border-white/10 shadow-inner">
                    {node.icon}
                  </span>
                  <h3 className="font-bold text-sm text-white leading-snug">
                    {node.title}
                  </h3>
                </div>
              </div>

              {/* Node Footer with XP Reward */}
              <div className="mt-5 pt-3 border-t border-white/[0.07] flex items-center justify-between text-xs font-mono">
                <span className="text-zinc-400">{dict.rewardLabel}</span>
                <span className="text-emerald-400 font-bold">{node.xp}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
