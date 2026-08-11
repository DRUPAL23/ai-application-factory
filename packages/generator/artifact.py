from dataclasses import dataclass
from io import BytesIO
from pathlib import PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile


@dataclass(frozen=True)
class Artifact:
    project_name: str
    files: list[dict[str, str]]

    def zip_bytes(self) -> bytes:
        buffer = BytesIO()
        with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
            root = self.project_name.replace("/", "-")
            for item in self.files:
                path = PurePosixPath(item["path"])
                if path.is_absolute() or ".." in path.parts:
                    raise ValueError(f"Unsafe artifact path: {path}")
                archive.writestr(f"{root}/{path.as_posix()}", item["content"])
        return buffer.getvalue()

    def manifest(self) -> dict:
        return {
            "project": self.project_name,
            "file_count": len(self.files),
            "files": [item["path"] for item in self.files],
        }
