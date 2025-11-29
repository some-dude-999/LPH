// Edge Cases Only - Words with Latin characters in Chinese column
// For testing edge case rendering (ATM, DNA, WhatsApp, etc.)

// Act-level metadata for edge cases
export const __actMeta = {
  actNumber: 0,
  actName: "Edge Cases",
  wordColumns: ["english", "chinese", "pinyin", "spanish", "portuguese"],
  translations: {"chinese": {"index": 1, "display": "\u4e2d\u6587"}, "spanish": {"index": 3, "display": "Espa\u00f1ol"}, "portuguese": {"index": 4, "display": "Portugu\u00eas"}},
  defaultTranslation: "chinese"
};

export const p2_69_money__banking = {
  meta: {
    wordpack: 69,
    english: "Money & Banking",
    chinese: "Money & Banking",
    pinyin: "Money & Banking",
    portuguese: "Money & Banking"
  },
  words: [
    ["ATM machine", "ATM机", "A T M jī", "Cajero automático", "Caixa eletrônico"],
    ["find ATM", "查找 ATM", "chá zhǎo A T M", "encontrar cajero automático", "encontrar caixa eletrônico"]
  ]
};

export const p4_117_biology__basics = {
  meta: {
    wordpack: 117,
    english: "Biology Basics",
    chinese: "Biology Basics",
    pinyin: "Biology Basics",
    portuguese: "Biology Basics"
  },
  words: [
    ["DNA test", "DNA测试", "D N A cè shì", "Prueba de ADN", "Teste de ADN"],
    ["DNA sequence", "DNA序列", "D N A xù liè", "Secuencia de ADN", "Sequência de DNA"]
  ]
};

export const p5_139_everyday__medical = {
  meta: {
    wordpack: 139,
    english: "Everyday Medical",
    chinese: "Everyday Medical",
    pinyin: "Everyday Medical",
    portuguese: "Everyday Medical"
  },
  words: [
    ["x-ray", "X射线", "X shè xiàn", "radiografía", "raio-x"],
    ["CT scan", "CT扫描", "C T sǎo miáo", "Tomografía computarizada", "Tomografia computadorizada"],
    ["chest x-ray", "胸部X光检查", "xiōng bù X guāng jiǎn chá", "radiografía de tórax", "radiografia de tórax"],
    ["x-ray results", "X射线结果", "X shè xiàn jié guǒ", "resultados de radiografías", "resultados de raios X"]
  ]
};

export const p5_143_sociology__basics = {
  meta: {
    wordpack: 143,
    english: "Sociology Basics",
    chinese: "Sociology Basics",
    pinyin: "Sociology Basics",
    portuguese: "Sociology Basics"
  },
  words: [
    ["collectivism vs", "集体主义 vs", "jí tǐ zhǔ yì v s", "colectivismo vs", "coletivismo vs"]
  ]
};
