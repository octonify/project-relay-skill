import { jwtVerify, SignJWT } from "jose";

const SECRET = new TextEncoder().encode(process.env.SESSION_SECRET ?? "dev-only-secret");

// PLACEHOLDER - 12h is a guess, not a decision. Sam owns the real value (product/security
// tradeoff); he is back Monday 3 Aug 2026. Do not change this number until he rules - the
// sessions-table column defaults and the staging migration depend on it. See HANDOFF.md.
const TTL_SECONDS = 60 * 60 * 12;

export async function issueSession(userId: string): Promise<string> {
  return new SignJWT({ sub: userId })
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime(`${TTL_SECONDS}s`)
    .sign(SECRET);
}

export async function readSession(token: string): Promise<{ sub: string } | null> {
  try {
    const { payload } = await jwtVerify(token, SECRET);
    return { sub: String(payload.sub) };
  } catch {
    return null;
  }
}

export const COOKIE_NAME = "relay_session";
export const COOKIE_OPTS = { httpOnly: true, sameSite: "lax", secure: true, path: "/" };
