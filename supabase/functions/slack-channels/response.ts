import { CORS_HEADERS } from "./constants.ts";

/**
 * Creates a JSON response with CORS headers
 */
export function jsonResponse(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      ...CORS_HEADERS,
      "Content-Type": "application/json",
    },
  });
}

/**
 * Handles CORS preflight OPTIONS requests
 */
export function corsPreflightResponse(): Response {
  return new Response(null, {
    status: 200,
    headers: CORS_HEADERS,
  });
}