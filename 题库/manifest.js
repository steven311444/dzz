/* 内容清单：题库 / 音频 / 教材，按"年级 + 教材版本"组织
 * 每新增一个年级/地区题包，在 banks 里追加一条，并把真实题目放进对应目录 */
window.CONTENT_MANIFEST = {
  banks: {
    "五沪": {
      label: "五年级·沪教版",
      grade: 5,
      textbook: "沪教版",
      region: "sh",
      files: {
        oral: "题库/五年级/沪教版/oral.json",
        vertical: "题库/五年级/沪教版/vertical.json",
        step: "题库/五年级/沪教版/step.json",
        text: "题库/五年级/沪教版/text.json"
      }
    }
  },
  audio: {
    "五沪": { base: "英语音频/", pattern: "w{aid:3}.mp3" }
  },
  textbooks: {}
};
