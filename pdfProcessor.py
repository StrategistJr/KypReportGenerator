import os
import PyPDF2  # Or use another PDF library like Tika
import openai

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

def process_pdf_and_get_openai_response(pdf_path, prompt):
    """Processes a single PDF, gets an OpenAI response, and returns it."""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

        response = openai.Completion.create(
            engine="text-davinci-003",  # Or another suitable model
            prompt=f"{prompt}\n\n{text}",
            max_tokens=150,  # Adjust as needed
        )
        return response.choices[0].text.strip()

    except Exception as e:
        return f"Error processing PDF or OpenAI API: {e}"


# Example usage:
pdf_file_paths = [  # List of PDF file paths
    "/path/to/pdf1.pdf",  # Replace with actual paths
    "/path/to/pdf2.pdf",
    "/path/to/pdf3.pdf",
    # ... add more paths dynamically as needed
]
user_prompt = "Summarize the key information in this document."  # Your prompt

for pdf_file_path in pdf_file_paths:
    openai_response = process_pdf_and_get_openai_response(pdf_file_path, user_prompt)

    if isinstance(openai_response, str) and openai_response.startswith("Error"):
        print(openai_response)
    else:
        print(openai_response)

        # Save the response to a file:
        txt_filename = os.path.splitext(os.path.basename(pdf_file_path))[0].replace(" ", "_") + ".txt"
        txt_path = os.path.join(os.path.dirname(pdf_file_path), txt_filename)
        try:
            with open(txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(openai_response)
            print(f"OpenAI response saved to: {txt_path}")
        except Exception as e:
            print(f"Error saving to text file: {e}")

    print("-" * 20)  # Separator between files
