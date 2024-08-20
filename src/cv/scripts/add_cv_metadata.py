from pdfrw import PdfReader, PdfWriter

def main():
    """
    write some metadata
    """
    filepath = "../../../../main.pdf"
    trailer = PdfReader(filepath)
    trailer.Info.Title = """Arjun Savel's CV"""
    trailer.Info.Author = 'Arjun Savel'
    trailer.Info.Subject = 'PhD Candidate in Astronomy at UMD, College Park'
    PdfWriter(filepath, trailer=trailer).write()
    
if __name__ == '__main__':
    main()
