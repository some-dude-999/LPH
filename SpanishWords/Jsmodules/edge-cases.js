// Edge Cases Only - Words with Latin characters in Chinese column
// For testing edge case rendering (ATM, DNA, WhatsApp, etc.)

// Act-level metadata for edge cases
export const __actMeta = {
  actNumber: 0,
  actName: "Edge Cases",
  wordColumns: ["spanish", "english", "chinese", "pinyin", "portuguese"],
  translations: {"english": {"index": 1, "display": "English"}, "chinese": {"index": 2, "display": "\u4e2d\u6587"}, "portuguese": {"index": 4, "display": "Portugu\u00eas"}},
  defaultTranslation: "english"
};

export const p1_26_clothing = {
  meta: {
    wordpack: 26,
    english: "Clothing",
    chinese: "衣服",
    pinyin: "Yīfu",
    portuguese: "Roupas"
  },
  words: [
    ["camiseta", "t-shirt", "T恤", "T xù", "camiseta"],
    ["camiseta sin mangas", "sleeveless t-shirt", "无袖T恤", "wú xiù T xù", "camiseta sem mangas"],
    ["una camiseta nueva", "a new t-shirt", "一件新T恤", "yī jiàn xīn T xù", "uma camiseta nova"]
  ]
};

export const p4_131_materials = {
  meta: {
    wordpack: 131,
    english: "Materials",
    chinese: "材料",
    pinyin: "Cáiliào",
    portuguese: "Materiais"
  },
  words: [
    ["camiseta de algodón", "cotton t-shirt", "棉质T恤", "mián zhì T xù", "camiseta de algodão"]
  ]
};

export const p5_167_fashion__style = {
  meta: {
    wordpack: 167,
    english: "Fashion & Style",
    chinese: "时尚与风格",
    pinyin: "Shíshàng yǔ Fēnggé",
    portuguese: "Moda e Estilo"
  },
  words: [
    ["en la pasarela", "on the catwalk", "在T台上", "zài T tái shàng", "na passarela"]
  ]
};

export const p6_182_telecommunications = {
  meta: {
    wordpack: 182,
    english: "Telecommunications",
    chinese: "电信",
    pinyin: "Diànxìn",
    portuguese: "Telecomunicações"
  },
  words: [
    ["WhatsApp", "WhatsApp", "WhatsApp应用", "W h a t s A p p yìng yòng", "WhatsApp"],
    ["por WhatsApp", "by WhatsApp", "通过WhatsApp", "tōng guò W h a t s A p p", "por WhatsApp"],
    ["en WhatsApp", "on WhatsApp", "在WhatsApp上", "zài W h a t s A p p shàng", "no WhatsApp"]
  ]
};

export const p7_233_cryptocurrency__terms = {
  meta: {
    wordpack: 233,
    english: "Cryptocurrency Terms",
    chinese: "加密货币术语",
    pinyin: "Jiāmì Huòbì Shùyǔ",
    portuguese: "Termos de Criptomoeda"
  },
  words: [
    ["el nft", "the nft", "NFT", "N F T", "o nft"],
    ["un nft", "an nft", "一个NFT", "yí gè N F T", "um NFT"]
  ]
};
