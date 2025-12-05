from typing import List, Tuple
from surface_triangulation.ui.services.io_service import IOService

class InputParserService:
    """Service to handle parsing of tuples from files or text inputs."""

    def __init__(self, io_service: IOService) -> None:
        self.io_service = io_service
    
    def parse_text_tuples(self, raw: str, tuple_size: int) -> List[Tuple[int, ...]]:
        results = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue

            tokens = line.replace(",", " ").split()
            if len(tokens) != tuple_size:
                continue

            try:
                results.append(tuple(int(t) for t in tokens))
            except ValueError:
                # Ignore lines that cannot be converted
                pass

        return results

    def load_list_from_tab(self, tab, tuple_size: int):
        idx = tab.currentIndex()

        # File tab
        if idx == 0:
            path = tab.file_input.selected_file()
            if tuple_size == 2:
                return self.io_service.load_edges(path)
            else:
                return self.io_service.load_vertices(path)

        # Text tab
        else:
            return self.parse_text_tuples(tab.text_input.toPlainText(), tuple_size)
