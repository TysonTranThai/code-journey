import { describe, expect, it } from "vitest";

import { fmt, HTML_LANG, INTL_TAG, isLocale } from "@/lib/i18n/config";
import { getDictionary, pluralForm } from "@/lib/i18n/dictionaries";
import { createI18n } from "@/lib/i18n";

describe("i18n dictionaries", () => {
  it("has complete EN/VI parity (compiler-enforced; spot-check here)", () => {
    const en = getDictionary("en");
    const vi = getDictionary("vi");
    expect(Object.keys(vi)).toEqual(Object.keys(en));
    expect(vi.workspace.submit).toBeTruthy();
    expect(vi.verdict.passed).toBeTruthy();
    // Every leaf value must be a non-empty string in both locales.
    for (const dict of [en, vi]) {
      for (const section of Object.values(dict)) {
        for (const [key, value] of Object.entries(section)) {
          if (typeof value === "string") {
            expect(value.length, `${key} empty`).toBeGreaterThan(0);
          }
        }
      }
    }
  });

  it("translates a known chrome string", () => {
    expect(getDictionary("vi").workspace.submit).not.toBe(getDictionary("en").workspace.submit);
  });
});

describe("fmt", () => {
  it("interpolates named variables", () => {
    expect(fmt("Hello {name}, {count} items", { name: "Ada", count: 3 })).toBe(
      "Hello Ada, 3 items",
    );
  });
  it("keeps unknown placeholders visible", () => {
    expect(fmt("{known} {unknown}", { known: "x" })).toBe("x {unknown}");
  });
});

describe("pluralForm", () => {
  const forms = { one: "1 challenge", other: "{count} challenges" };
  it("uses one for 1 in English", () => {
    expect(pluralForm("en", 1, forms)).toBe("1 challenge");
  });
  it("uses other otherwise in English", () => {
    expect(pluralForm("en", 5, forms)).toBe("{count} challenges");
  });
  it("Vietnamese always uses other", () => {
    expect(pluralForm("vi", 1, forms)).toBe("{count} challenges");
    expect(pluralForm("vi", 5, forms)).toBe("{count} challenges");
  });
});

describe("createI18n", () => {
  it("tp interpolates count into the plural form", () => {
    const i18n = createI18n("en");
    expect(i18n.tp(1, { one: "{count} lesson", other: "{count} lessons" })).toBe("1 lesson");
    expect(i18n.tp(3, { one: "{count} lesson", other: "{count} lessons" })).toBe("3 lessons");
  });
  it("tp in Vietnamese always uses the other form", () => {
    const i18n = createI18n("vi");
    expect(i18n.tp(1, { one: "{count} bài học", other: "{count} bài học" })).toBe("1 bài học");
  });
});

describe("locale config", () => {
  it("validates locales", () => {
    expect(isLocale("vi")).toBe(true);
    expect(isLocale("en")).toBe(true);
    expect(isLocale("fr")).toBe(false);
    expect(isLocale(undefined)).toBe(false);
  });
  it("maps html lang + Intl tags", () => {
    expect(HTML_LANG.vi).toBe("vi");
    expect(INTL_TAG.vi).toBe("vi-VN");
    expect(INTL_TAG.en).toBe("en-US");
  });
});
