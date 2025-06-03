from docling.document_converter import DocumentConverter

source = "data/tu-van-tuyen-sinh/Thong-tin-tuyen-sinh-2025.pdf"
converter = DocumentConverter()
result = converter.convert(source)

print("=" * 40)
print(result.document.export_to_markdown())

with open("result.md", "w", encoding="utf-8") as f:
    f.write(result.document.export_to_markdown())