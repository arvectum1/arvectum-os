import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { Guide } from "./Guide";
import { LanguageProvider } from "./i18n";

afterEach(() => {
  cleanup();
  window.history.replaceState({}, "", "/");
});

describe("P9.11-F10A Workspace guide", () => {
  it("explains current Russian-first capabilities, limitations and authority boundary", () => {
    render(<LanguageProvider initialLanguage="ru"><Guide release="p9.11.f10-test" /></LanguageProvider>);

    expect(screen.getByRole("heading", { name: "Что здесь можно делать" })).toBeTruthy();
    expect(screen.getByText("p9.11.f10-test")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Что работает сейчас" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Чего пока нет" })).toBeTruthy();
    expect(screen.getByText(/ещё нет общего приёма организационных материалов/)).toBeTruthy();
    expect(screen.getByText(/не является решением, разрешением, организационным полномочием/)).toBeTruthy();
    expect(screen.getByRole("link", { name: "Посмотреть задачи" })).toHaveAttribute("href", "/work");
    expect(screen.getByRole("link", { name: "Найти информацию" })).toHaveAttribute("href", "/information");
    expect(screen.getByRole("link", { name: "Спросить Arvectum AI" })).toHaveAttribute("href", "/copilot");
  });
});
