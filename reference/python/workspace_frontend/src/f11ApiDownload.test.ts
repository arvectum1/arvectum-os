import { afterEach, describe, expect, it, vi } from "vitest";
import { downloadCompanyOutput } from "./f11Api";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("F11A generated DOCX download boundary", () => {
  it("downloads through same-origin fetch with the Workspace release header", async () => {
    const fetchMock = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => new Response(
      new Blob(["docx-bytes"], { type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" }),
      {
        status: 200,
        headers: {
          "Content-Disposition": "attachment; filename=generated-owner-test.docx",
          "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        },
      },
    ));
    vi.stubGlobal("fetch", fetchMock);

    const result = await downloadCompanyOutput("/api/app/v1/company-materials/outputs/OUT-owner-test/download");

    expect(result.filename).toBe("generated-owner-test.docx");
    expect(fetchMock).toHaveBeenCalledTimes(1);
    const init = fetchMock.mock.calls[0][1];
    const headers = new Headers(init?.headers);
    expect(headers.get("X-Arvectum-Workspace-Release")).toBeTruthy();
    expect(init?.credentials).toBe("same-origin");
  });

  it("rejects arbitrary download paths before any request", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);

    await expect(downloadCompanyOutput("https://attacker.invalid/file.docx")).rejects.toThrow("COMPANY_OUTPUT_DOWNLOAD_PATH_INVALID");
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
