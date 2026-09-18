interface HowItWorksSectionProps {
  dict: {
    badge: string;
    title: string;
    subtitle: string;
    step1Num: string;
    step1Title: string;
    step1Desc: string;
    step1Tag: string;
    step1Preview: string;
    step2Num: string;
    step2Title: string;
    step2Desc: string;
    step2Tag: string;
    step3Num: string;
    step3Title: string;
    step3Desc: string;
    step3Tag: string;
    step3Assertions: string;
    step4Num: string;
    step4Title: string;
    step4Desc: string;
    step4Tag: string;
    step4Sensei: string;
  };
}

export function HowItWorksSection({ dict }: HowItWorksSectionProps) {
  const steps = [
    {
      num: dict.step1Num,
      title: dict.step1Title,
      desc: dict.step1Desc,
      icon: "📖",
      tag: dict.step1Tag,
      pillBg: "border-emerald-500/30 bg-emerald-500/10 text-emerald-400",
      accent: "from-emerald-500 to-teal-400",
      preview: (
        <div className="rounded border border-white/[0.06] bg-black/40 p-2 font-mono text-[10px] text-zinc-300">
          <span className="text-emerald-400 font-semibold"># Concept</span>
          <p className="text-zinc-400 truncate mt-0.5">{dict.step1Preview}</p>
        </div>
      ),
    },
    {
      num: dict.step2Num,
      title: dict.step2Title,
      desc: dict.step2Desc,
      icon: "💻",
      tag: dict.step2Tag,
      pillBg: "border-cyan-500/30 bg-cyan-500/10 text-cyan-400",
      accent: "from-cyan-500 to-sky-400",
      preview: (
        <div className="rounded border border-white/[0.06] bg-black/40 p-2 font-mono text-[10px] text-zinc-300">
          <span className="text-cyan-400 font-semibold">function</span> isPalindrome(s) &#123;
          <p className="text-zinc-400 truncate mt-0.5">  let l = 0, r = s.length - 1;</p>
        </div>
      ),
    },
    {
      num: dict.step3Num,
      title: dict.step3Title,
      desc: dict.step3Desc,
      icon: "⚡",
      tag: dict.step3Tag,
      pillBg: "border-teal-500/30 bg-teal-500/10 text-teal-400",
      accent: "from-teal-500 to-emerald-400",
      preview: (
        <div className="rounded border border-emerald-500/30 bg-emerald-950/20 p-2 font-mono text-[10px] flex items-center justify-between">
          <span className="text-emerald-400 font-semibold">✓ {dict.step3Assertions}</span>
          <span className="text-zinc-400">8ms</span>
        </div>
      ),
    },
    {
      num: dict.step4Num,
      title: dict.step4Title,
      desc: dict.step4Desc,
      icon: "🤖",
      tag: dict.step4Tag,
      pillBg: "border-purple-500/30 bg-purple-500/10 text-purple-400",
      accent: "from-purple-500 to-pink-400",
      preview: (
        <div className="rounded border border-purple-500/30 bg-purple-950/20 p-2 font-mono text-[10px] text-purple-300">
          <p className="truncate font-semibold text-purple-300">{dict.step4Sensei}</p>
        </div>
      ),
    },
  ];

  return (
    <section aria-labelledby="how-it-works-heading" className="w-full flex flex-col gap-8 pt-6">
      <div className="flex flex-col items-center text-center gap-2">
        <span className="badge-pixel badge-pixel-quest">{dict.badge}</span>
        <h2
          id="how-it-works-heading"
          className="text-2xl font-bold tracking-tight text-white sm:text-3xl"
        >
          {dict.title}
        </h2>
        <p className="max-w-xl text-sm text-zinc-400 leading-relaxed">
          {dict.subtitle}
        </p>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 relative">
        {steps.map((step, idx) => (
          <div
            key={idx}
            className="glass-card card-glow-hover flex flex-col justify-between p-5 rounded-xl group relative overflow-hidden"
          >
            {/* Top Step Pill & Number */}
            <div className="flex flex-col gap-3">
              <div className="flex items-center justify-between">
                <span className={`text-[10px] font-mono px-2 py-0.5 rounded-md border font-semibold ${step.pillBg}`}>
                  {step.tag}
                </span>
                <span className="font-mono text-xs font-bold text-zinc-400 group-hover:text-emerald-400 transition-colors">
                  {step.num}
                </span>
              </div>

              <div className="flex items-center gap-2.5">
                <span className="text-xl" aria-hidden="true">{step.icon}</span>
                <h3 className="font-bold text-base text-zinc-100 group-hover:text-emerald-300 transition-colors">
                  {step.title}
                </h3>
              </div>

              <p className="text-xs text-zinc-400 leading-relaxed">
                {step.desc}
              </p>
            </div>

            {/* Bottom Mini Preview Widget */}
            <div className="mt-4 pt-3 border-t border-white/[0.06]">
              {step.preview}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
