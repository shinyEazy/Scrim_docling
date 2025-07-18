import os
from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat

def parse_xlsx_to_markdown(input_dir="data/cong-nghiep", output_dir="output"):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    converter = DocumentConverter()
    
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist")
        return
    
    xlsx_files = list(input_path.glob("*.xlsx"))
    
    if not xlsx_files:
        print(f"No XLSX files found in '{input_dir}'")
        return
    
    print(f"Found {len(xlsx_files)} XLSX files to process")
    
    for xlsx_file in xlsx_files:
        try:
            print(f"Processing: {xlsx_file.name}")
            
            result = converter.convert(str(xlsx_file))
            
            markdown_content = result.document.export_to_markdown()
            
            output_filename = xlsx_file.stem + ".md"
            output_path = Path(output_dir) / output_filename

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"✓ Converted '{xlsx_file.name}' to '{output_filename}'")
            
        except Exception as e:
            print(f"✗ Error processing '{xlsx_file.name}': {str(e)}")
    
    print(f"\nConversion complete! Markdown files saved to '{output_dir}'")

def main():
    input_directory = "data/cong-nghiep"
    output_directory = "output/cong-nghiep"
    
    print("XLSX to Markdown Parser using Docling")
    print("=" * 40)
    
    parse_xlsx_to_markdown(input_directory, output_directory)

if __name__ == "__main__":
    main()