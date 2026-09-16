import assert from "node:assert/strict";
import { test } from "node:test";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import boundedTurns from "../pi-quick-oracles.ts";

function setup(api = "openai-responses", compat: Record<string, boolean> = {}) {
	const env = { review: process.env.PI_REVIEW_TOKENS, answer: process.env.PI_ANSWER_TOKENS };
	process.env.PI_REVIEW_TOKENS = "100";
	process.env.PI_ANSWER_TOKENS = "50";
	const handlers = new Map<string, Function>();
	const prompts: unknown[] = [];
	let tools: string[] = ["read"];
	let thinking = "high";
	let aborts = 0;
	boundedTurns({
		on: (name: string, fn: Function) => handlers.set(name, fn),
		appendEntry() {},
		setActiveTools: (value: string[]) => { tools = value; },
		setThinkingLevel: (value: string) => { thinking = value; },
		sendUserMessage: (...args: unknown[]) => prompts.push(args),
	} as unknown as ExtensionAPI);
	for (const [key, value] of [["PI_REVIEW_TOKENS", env.review], ["PI_ANSWER_TOKENS", env.answer]]) {
		if (value === undefined) delete process.env[key!];
		else process.env[key!] = value;
	}
	const ctx = { model: { api, compat }, abort: async () => { aborts++; } };
	const message = (output: number, stopReason: string) => ({ role: "assistant", usage: { output }, stopReason,
		content: [{ type: "thinking", thinking: "", thinkingSignature: "unchanged-opaque-state" }] });
	return { prompts, message, get tools() { return tools; }, get thinking() { return thinking; }, get aborts() { return aborts; },
		request: (payload: unknown = {}) => handlers.get("before_provider_request")!({ payload }, ctx),
		turn: (value: unknown) => handlers.get("turn_end")!({ message: value }, ctx),
		end: (value: unknown) => handlers.get("message_end")!({ message: value }, ctx) };
}

test("one cumulative review budget, native state unchanged, one final-answer allowance", () => {
	const s = setup();
	assert.equal(s.request().max_output_tokens, 100);
	s.turn(s.message(30, "toolUse"));
	assert.equal(s.request().max_output_tokens, 70);
	const capped = s.message(70, "length");
	const original = structuredClone(capped);
	s.turn(capped);
	assert.deepEqual(capped, original);
	assert.equal(s.request().max_output_tokens, 50);
	assert.equal(s.prompts.length, 1);
	assert.deepEqual(s.tools, []);
	assert.equal(s.thinking, "minimal");
	s.turn(s.message(12, "stop"));
	assert.throws(() => s.request(), /finished/);
	assert.equal(s.aborts, 1);
	assert.equal(s.prompts.length, 1);
});

test("uses each provider's supported output-token field", () => {
	assert.deepEqual(setup("openai-responses").request({ keep: true }), { keep: true, max_output_tokens: 100 });
	assert.deepEqual(
		setup("openai-responses", { supportsMaxOutputTokens: false }).request({ keep: true }),
		{ keep: true },
	);
	assert.deepEqual(setup("openai-completions").request({ keep: true }), { keep: true, max_tokens: 100 });
	assert.deepEqual(setup("openai-completions").request({ max_completion_tokens: 900 }), { max_completion_tokens: 100 });
	assert.deepEqual(setup("anthropic-messages").request({ keep: true }), { keep: true, max_tokens: 100 });
	assert.deepEqual(setup("google-generative-ai").request({ config: { keep: true } }), {
		config: { keep: true, maxOutputTokens: 100 },
	});
	assert.deepEqual(setup("google-vertex").request({ config: { keep: true } }), {
		config: { keep: true, maxOutputTokens: 100 },
	});
});

test("omits unsupported Codex output cap without changing other payload fields", () => {
	assert.deepEqual(setup("openai-codex-responses").request({ keep: true }), { keep: true });
	assert.deepEqual(
		setup("openai-codex-responses", { supportsMaxOutputTokens: true }).request({ keep: true }),
		{ keep: true, max_output_tokens: 100 },
	);
});

test("second truncation remains length-stopped but is explicitly incomplete", () => {
	const s = setup();
	s.turn(s.message(100, "length"));
	const result = s.end(s.message(50, "length"));
	assert.equal(result.message.stopReason, "length");
	assert.match(result.message.errorMessage, /incomplete/);
	assert.equal(result.message.content[0].thinkingSignature, "unchanged-opaque-state");
	s.turn(result.message);
	assert.throws(() => s.request(), /finished/);
	assert.equal(s.prompts.length, 1);
});
