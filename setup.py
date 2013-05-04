from modules.document_builder import DocumentBuilder
from modules.invertedindex_builder import InvertedIndexBuilder


def main():
    # Build documents after scraping
    sb = DocumentBuilder()
    sb.build_documents()

    # Create inverted index of terms
    ind = InvertedIndexBuilder()

if __name__ == '__main__':
    main()
