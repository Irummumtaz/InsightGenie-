from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def draw_wrapped_text(c, text, x, y, max_width, line_height, footer_height, page_height):
    """Draw text with word wrapping, ensuring it does not overlap with footer."""
    lines = text.split('\n')
    for line in lines:
        words = line.split()
        line_buffer = ""
        for word in words:
            test_line = f"{line_buffer} {word}".strip()
            if c.stringWidth(test_line, "Helvetica", 12) <= max_width:
                line_buffer = test_line
            else:
                if y - line_height < footer_height + 10:
                    # Start a new page
                    c.showPage()
                    reset_page_header(c)
                    y = page_height - 60
                
                c.drawString(x, y, line_buffer)
                y -= line_height
                line_buffer = word
        
        if line_buffer:
            if y - line_height < footer_height + 10:
                c.showPage()
                reset_page_header(c)
                y = page_height - 60

            c.drawString(x, y, line_buffer)
            y -= line_height
    return y

def reset_page_header(c):
    """Re-add the title and line for a new page."""
    width, height = letter
    title = "My GENIE Insights"
    c.setFont("Helvetica", 12)
    title_x = width / 2 - c.stringWidth(title, "Helvetica-Bold", 16) / 2
    c.drawString(title_x, height - 30, title)
    c.line(left_margin, height - 35, width - right_margin, height - 35)

def generate_pdf_report(output_filename, plots_dir, query_history):
    c = canvas.Canvas(output_filename, pagesize=letter)
    global width, height, left_margin, right_margin, content_width
    width, height = letter
    left_margin = 40
    right_margin = 40
    content_width = width - left_margin - right_margin
    footer_height = 20

    reset_page_header(c)
    y_position = height - 60  # Start position below the title

    for entry in query_history:
        query = entry[0]
        response = entry[1]
        img_path = entry[2] if len(entry) > 2 else None

        # Add the query
        c.setFont("Helvetica-Bold", 14)
        y_position = draw_wrapped_text(c, "Query:", left_margin, y_position, content_width, 15, footer_height, height)
        c.setFont("Helvetica", 12)
        y_position = draw_wrapped_text(c, query, left_margin, y_position, content_width, 15, footer_height, height)
        y_position -= 10  # Space between query and response

        # Add the response
        c.setFont("Helvetica-Bold", 14)
        y_position = draw_wrapped_text(c, "Response:", left_margin, y_position, content_width, 15, footer_height, height)

        # Check if the response starts on a new page
        if y_position < footer_height + 15:  # Less than 15 points for response
            c.showPage()
            reset_page_header(c)
            y_position = height - 60  # Reset position for the new page

        # Ensure that the font is set to regular before the response
        c.setFont("Helvetica", 12)
        y_position = draw_wrapped_text(c, response, left_margin, y_position, content_width, 15, footer_height, height)

        # Check if the image file exists before adding
        if img_path and os.path.exists(img_path):
            image_height = 200  # Height of the image
            space_needed = image_height + 10  # Image height + additional space

            # Check if there is enough space for the image and some padding
            if y_position < footer_height + space_needed + 10:  # Check for footer space
                c.showPage()
                reset_page_header(c)
                y_position = height - 60  # Reset position for the new page

            # Draw padding before the image
            y_position -= 200  # Space before the image

            # Center the image
            image_x = (width - 380) / 2
            c.drawImage(img_path, image_x, y_position, width=380, height=image_height, preserveAspectRatio=True)
            y_position -= (image_height + 10)  # Space for the image plus extra padding

        y_position -= 10  # Space after the image

        if y_position < footer_height + 40:  # Ensuring footer space
            c.showPage()
            reset_page_header(c)
            y_position = height - 60  # Reset position for the new page

    add_footer(c, left_margin)  # Add footer on the last page
    c.save()

def add_footer(c, left_margin):
    """Draw the footer at the bottom of the page."""
    c.saveState()  # Save the current state of the canvas
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(left_margin, 10, "Generated Report - My GENIE Insights")
    c.restoreState()  # Restore the canvas to its previous state
