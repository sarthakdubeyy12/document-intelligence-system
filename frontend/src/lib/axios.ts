export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: {
      Accept: "application/json",
      ...(init?.headers || {}),
    },
    ...init,
  });

  if (!response.ok) {
    const errorText = await response.text();
    let message = "Something went wrong.";

    try {
      const parsed = JSON.parse(errorText);
      if (typeof parsed?.detail === "string") {
        message = parsed.detail;
      } else if (Array.isArray(parsed?.detail)) {
        message = parsed.detail
          .map((item: unknown) =>
            typeof item === "string"
              ? item
              : (item as { msg?: string })?.msg || "Invalid request",
          )
          .join(" ");
      } else if (typeof parsed?.message === "string") {
        message = parsed.message;
      } else if (errorText) {
        message = errorText;
      }
    } catch {
      if (errorText) {
        message = errorText;
      }
    }

    throw new Error(message);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}
