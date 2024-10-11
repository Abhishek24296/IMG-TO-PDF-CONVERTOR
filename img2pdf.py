from PIL import Image
import os
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel
from rich.align import Align

# Initialize the Rich console
console = Console()

def show_help_menu():
    """Displays the help menu inside a rectangular box with a centered title."""
    help_text = """
    [bold green]Description:[/bold green] This program converts all images from a specified folder into a single PDF file.
    
    [bold green]Supported Image Formats:[/bold green] .png, .jpg, .jpeg
    
    [bold green]Output:[/bold green] The converted PDF will be saved in a subfolder named 'IMG PDFs' inside the image folder.
    
    [bold green]Features:[/bold green]
    1. [cyan]Progress Bar:[/cyan] Displays the progress of image-to-PDF conversion.
    2. [cyan]Custom PDF Name:[/cyan] You can specify a custom name for the output PDF.
    3. [cyan]Help Menu:[/cyan] Shows this information before the program runs.

    [bold magenta]Press Enter to start the image-to-PDF conversion...[/bold magenta]
    """
    
    # Display the help menu with a centered title inside a rectangular panel
    console.print(Panel(
        Align.center(help_text),  # Center the help text within the panel
        title="Image to PDF Converter Help Menu",  # Title at the top
        title_align="center",  # Center-align the title
        border_style="bright_blue",
        expand=False
    ))

def show_summary(output_pdf_path, image_files):
    """Displays a summary after the conversion with the same design as the help menu."""
    summary_text = f"""
    [bold green]Total Images Processed:[/bold green] {len(image_files)}
    
    [bold green]PDF Location:[/bold green] {output_pdf_path}
    
    [bold magenta]Press Enter to close the program...[/bold magenta]
    """
    
    # Display the summary with the same panel design
    console.print(Panel(
        Align.center(summary_text),  # Center the summary text within the panel
        title="Conversion Summary",  # Title at the top
        title_align="center",  # Center-align the title
        border_style="bright_blue",
        expand=False
    ))

# Show the help menu in a rectangle
show_help_menu()

# Wait for the user to press Enter to proceed
input()

# Folder where your images are stored
image_folder = r''  # Put the path of your image folder

# Create a subfolder for the output PDFs if it doesn't exist
output_folder = os.path.join(image_folder, "IMG PDFs")
os.makedirs(output_folder, exist_ok=True)

# Ask the user for the desired PDF file name
output_pdf_name = console.input("[bold cyan]Enter the name for the output PDF (without extension): [/bold cyan]")
output_pdf_path = os.path.join(output_folder, f"{output_pdf_name}.pdf")

# List to hold all image file paths
image_files = []

# Loop through all files in the folder and add image files to the list
for file_name in os.listdir(image_folder):
    if file_name.endswith(('.png', '.jpg', '.jpeg')):  # Include supported image formats
        image_files.append(os.path.join(image_folder, file_name))

# Check if there are any images to convert
if not image_files:
    console.print("[bold red]No images found in the folder.[/bold red]")
else:
    # Open the images and convert to RGB (necessary for PDF conversion)
    image_list = []
    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), 
                  TextColumn("[progress.completed]{task.completed}/{task.total}")) as progress:
        task = progress.add_task("[cyan]Converting images to PDF...", total=len(image_files))

        for img_path in image_files:
            image = Image.open(img_path).convert('RGB')
            image_list.append(image)
            progress.update(task, advance=1)

    # Save the first image and append the rest as pages in the PDF
    image_list[0].save(output_pdf_path, save_all=True, append_images=image_list[1:])

    console.print(f"[bold green]PDF created successfully and saved as {output_pdf_path}[/bold green]")

    # Show summary and wait for user to close the program
    show_summary(output_pdf_path, image_files)
    input()  # Wait for the user to press Enter to close the program
