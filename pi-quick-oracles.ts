import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";

// Pi/OpenAI: load only in Nico children with subagentOnlyExtensions, not in the parent.
export default function boundedTurns(pi: ExtensionAPI) {
	const reviewTokens = Number(process.env.PI_REVIEW_TOKENS ?? 4000);
	const answerTokens = Number(process.env.PI_ANSWER_TOKENS ?? 2000);
	let remaining = reviewTokens;
	let phase: "review" | "answer" | "done" = "review";
	const stop = (ctx: ExtensionContext, reason: string): never => {
		phase = "done";
		void ctx.abort(); // Pi/OpenAI: provider-hook exceptions alone do not stop a request.
		throw new Error(reason);
	};

	pi.on("before_provider_request", (event, ctx) => {
		if (phase === "done") stop(ctx, "This bounded review has finished; no further automatic model call is allowed.");
		if (![reviewTokens, answerTokens].every(limit => Number.isSafeInteger(limit) && limit >= 16)) {
			stop(ctx, "Review token limits must be integers of at least 16.");
		}
		const payload = { ...(event.payload as Record<string, any>) };
		switch (ctx.model?.api) {
			case "openai-responses":
			case "openai-codex-responses":
				payload.max_output_tokens = remaining;
				break;
			case "openai-completions":
				payload["max_completion_tokens" in payload ? "max_completion_tokens" : "max_tokens"] = remaining;
				break;
			case "anthropic-messages":
				payload.max_tokens = remaining;
				if (payload.thinking?.type === "enabled" && payload.thinking.budget_tokens >= remaining) {
					stop(ctx, "The remaining output budget cannot contain this model's thinking budget.");
				}
				break;
			case "google-generative-ai":
			case "google-vertex":
				payload.config = { ...payload.config, maxOutputTokens: remaining };
				break;
			default:
				stop(ctx, `No verified token-cap mapping for API ${ctx.model?.api}.`);
		}
		return payload;
	});

	pi.on("message_end", (event) => {
		if (phase === "answer" && event.message.role === "assistant" && event.message.stopReason === "length") {
			return { message: { ...event.message, errorMessage: "Final answer reached its token limit; this review is incomplete." } };
		}
	});

	pi.on("turn_end", (event, ctx) => {
		const message = event.message;
		if (message.role !== "assistant") return;
		remaining -= message.usage.output;
		pi.appendEntry("bounded-turns", { phase, outputTokens: message.usage.output, remaining, stopReason: message.stopReason });
		if (message.stopReason === "error" || message.stopReason === "aborted" || ctx.signal?.aborted) {
			phase = "done";
			return;
		}
		if (phase === "answer") {
			phase = "done";
			return;
		}
		if (message.stopReason === "stop") {
			phase = "done";
			return;
		}
		if (remaining < 16 || message.stopReason === "length") {
			phase = "answer";
			remaining = answerTokens;
			pi.setActiveTools([]);
			pi.setThinkingLevel("minimal");
			pi.sendUserMessage(
				"The review token budget is exhausted. Using the existing context, give your final answer now. Do not use tools or start a new analysis. State any missing evidence or unfinished work.",
				{ deliverAs: "followUp" },
			);
		}
	});
}
