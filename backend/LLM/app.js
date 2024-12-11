import { ollamaOCR, DEFAULT_OCR_SYSTEM_PROMPT } from "ollama-ocr";

async function runOCR() {
  const text = await ollamaOCR({
    filePath: "./test/images/handwriting.jpg",
    systemPrompt: DEFAULT_OCR_SYSTEM_PROMPT,
  });
  console.log(text);
}