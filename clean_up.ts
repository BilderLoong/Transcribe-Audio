#!/usr/bin/env bun

import * as fs from "fs";
import * as path from "path";

function cleanUpDir(dir: string) {
  const endsWithConditions = [".vtt", ".txt", ".json", ".srt", ".tsv"];
  const containsString = "en";
  const notContainsString = "non_word_level";

  fs.readdirSync(dir).forEach((file) => {
    const filePath = path.join(dir, file);
    const fileName = path.parse(file).name;

    if (
      endsWithConditions.some((ext) => file.endsWith(ext)) &&
      (!fileName.includes(notContainsString) ||
        fileName.includes(containsString))
    ) {
      fs.unlinkSync(filePath);
      console.log(`Removed file: ${file}`);
    }
  });
}
const directoryPath = process.argv[2];
cleanUpDir(directoryPath);
