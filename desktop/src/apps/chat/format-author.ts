export interface AuthorContext {
  currentUserId: string | null;
  currentUserDisplayName: string | null;
  userNames?: Record<string, string>;
}

export function displayAuthor(
  msg: { author_id: string; author_type?: "user" | "agent" | "system" },
  ctx: AuthorContext,
): string {
  if (msg.author_type === "system") return "system";
  if (msg.author_type === "user") {
    if (msg.author_id === ctx.currentUserId && ctx.currentUserDisplayName) {
      return ctx.currentUserDisplayName;
    }
    if (ctx.userNames && ctx.userNames[msg.author_id]) {
      return ctx.userNames[msg.author_id] || msg.author_id;
    }
    return msg.author_id;
  }
  return msg.author_id; // agent slug
}
