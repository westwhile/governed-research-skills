# -*- coding: utf-8 -*-
"""
Multi-source citation downloader with format conversion.
Sources: PubMed (NCBI E-utilities), CrossRef (REST API), arXiv (Atom API).
Outputs: .nbib (PubMed only), .ris, .bib, .enw.
Secure citation-file export is Windows-only. On non-Windows platforms the CLI
fails closed before path, network, conversion, or write operations. Any item
or batch error produces a non-zero CLI exit.

Usage:
  python format-converter.py --pmid 28344011 --output ABSOLUTE_OUTPUT_DIR
  python format-converter.py --pmid 28344011,10645439 --format ris --output ABSOLUTE_OUTPUT_DIR
  python format-converter.py --doi 10.1038/nature14539 --format bib --output ABSOLUTE_OUTPUT_DIR
  python format-converter.py --arxiv 1706.03762 --format ris --output ABSOLUTE_OUTPUT_DIR
  python format-converter.py --query "TB-Profiler AND Bioinformatics[Journal]" --output ABSOLUTE_OUTPUT_DIR
  python format-converter.py --input refs.txt --output ABSOLUTE_OUTPUT_DIR
  python format-converter.py --input refs.txt --format ris --output ABSOLUTE_OUTPUT_DIR
  python format-converter.py --interactive --output ABSOLUTE_OUTPUT_DIR

refs.txt format:
  PMID:28344011
  DOI:10.1038/nature14539
  ARXIV:1706.03762
  QUERY:TB-Profiler AND Bioinformatics[Journal]
  AUTHOR:Dheda TITLE:drug-resistant tuberculosis
  # Lines starting with # are comments
"""

import os
import hashlib
import re
import stat
import sys
import time
import json
import argparse
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from urllib.parse import quote, urlencode

if os.name == "nt":
    import ctypes
    import msvcrt
    from ctypes import wintypes

from converters import (
    convert_from_medline,
    convert_from_crossref,
    convert_from_arxiv,
    get_extension,
)

EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CROSSREF_BASE = "https://api.crossref.org/works"
ARXIV_BASE = "https://export.arxiv.org/api/query"
DELAY = 0.5

WINDOWS_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}
SAFE_COMPONENT_PATTERN = re.compile(r"[^A-Za-z0-9._-]+")

if os.name == "nt":
    _GENERIC_WRITE = 0x40000000
    _FILE_READ_ATTRIBUTES = 0x00000080
    _DELETE = 0x00010000
    _CREATE_NEW = 1
    _OPEN_EXISTING = 3
    _FILE_ATTRIBUTE_DIRECTORY = 0x00000010
    _FILE_ATTRIBUTE_NORMAL = 0x00000080
    _FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
    _FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
    _FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
    _FILE_DISPOSITION_INFO_CLASS = 4
    _INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

    class _FILE_DISPOSITION_INFO(ctypes.Structure):
        _fields_ = [("DeleteFile", wintypes.BOOL)]

    class _BY_HANDLE_FILE_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("dwFileAttributes", wintypes.DWORD),
            ("ftCreationTime", wintypes.FILETIME),
            ("ftLastAccessTime", wintypes.FILETIME),
            ("ftLastWriteTime", wintypes.FILETIME),
            ("dwVolumeSerialNumber", wintypes.DWORD),
            ("nFileSizeHigh", wintypes.DWORD),
            ("nFileSizeLow", wintypes.DWORD),
            ("nNumberOfLinks", wintypes.DWORD),
            ("nFileIndexHigh", wintypes.DWORD),
            ("nFileIndexLow", wintypes.DWORD),
        ]

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _CreateFileW = _kernel32.CreateFileW
    _CreateFileW.argtypes = (
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.c_void_p,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    )
    _CreateFileW.restype = wintypes.HANDLE
    _GetFinalPathNameByHandleW = _kernel32.GetFinalPathNameByHandleW
    _GetFinalPathNameByHandleW.argtypes = (
        wintypes.HANDLE,
        wintypes.LPWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
    )
    _GetFinalPathNameByHandleW.restype = wintypes.DWORD
    _GetFileInformationByHandle = _kernel32.GetFileInformationByHandle
    _GetFileInformationByHandle.argtypes = (
        wintypes.HANDLE,
        ctypes.POINTER(_BY_HANDLE_FILE_INFORMATION),
    )
    _GetFileInformationByHandle.restype = wintypes.BOOL
    _SetFileInformationByHandle = _kernel32.SetFileInformationByHandle
    _SetFileInformationByHandle.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    )
    _SetFileInformationByHandle.restype = wintypes.BOOL
    _CloseHandle = _kernel32.CloseHandle
    _CloseHandle.argtypes = (wintypes.HANDLE,)
    _CloseHandle.restype = wintypes.BOOL


def safe_filename_component(value, label, max_length=60):
    """Convert an untrusted identifier into one portable filename component."""
    raw = value.strip()
    if not raw:
        raise ValueError(f"Empty {label}")

    component = SAFE_COMPONENT_PATTERN.sub("_", raw)
    component = re.sub(r"\.{2,}", "_", component)
    component = re.sub(r"_+", "_", component).strip(" ._")
    changed = component != raw
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:10]
    if not component:
        component = f"id-{digest}"
        changed = True
    if changed or len(component) > max_length:
        base_limit = max(1, max_length - len(digest) - 1)
        component = component[:base_limit].rstrip(" ._") or "id"
        component = f"{component}-{digest}"
    component = component[:max_length].rstrip(" .")
    if component.upper() in WINDOWS_RESERVED_NAMES:
        component = f"_{component}"[:max_length]

    if (
        not component
        or component in {".", ".."}
        or ".." in component
        or "/" in component
        or "\\" in component
        or ":" in component
        or component.endswith((" ", "."))
        or component.upper() in WINDOWS_RESERVED_NAMES
    ):
        raise ValueError(f"Unable to derive a safe filename component for {label}")
    return component


def resolve_output_path(output_dir, filename):
    """Resolve one output filename and prove it remains directly under output_dir."""
    root = os.path.realpath(os.path.abspath(output_dir))
    if not os.path.isabs(root) or not os.path.isdir(root):
        raise ValueError("Output directory must be an existing absolute directory")
    if (
        not filename
        or filename in {".", ".."}
        or os.path.isabs(filename)
        or os.path.splitdrive(filename)[0]
        or re.match(r"^[A-Za-z]:", filename)
        or "/" in filename
        or "\\" in filename
        or ":" in filename
    ):
        raise ValueError("Output filename must be one safe path component")

    candidate = os.path.realpath(os.path.abspath(os.path.join(root, filename)))
    try:
        common = os.path.commonpath([root, candidate])
    except ValueError as exc:
        raise ValueError("Output path is not on the approved output volume") from exc
    if (
        os.path.normcase(common) != os.path.normcase(root)
        or os.path.normcase(os.path.dirname(candidate)) != os.path.normcase(root)
    ):
        raise ValueError("Resolved output path escapes the approved output directory")
    return candidate


def build_output_target(output_dir, source, identifier, fmt):
    """Create a safe filename and a containment-checked resolved output path."""
    component = safe_filename_component(identifier, source)
    ext = get_extension(fmt)
    if not re.fullmatch(r"\.[A-Za-z0-9]+", ext):
        raise ValueError(f"Unsafe output extension for format {fmt}")
    filename = f"{source}-{component}{ext}"
    return filename, resolve_output_path(output_dir, filename)


def _validate_output_filename(filename):
    reserved_stem = filename.split(".", 1)[0].upper() if filename else ""
    if (
        not filename
        or filename in {".", ".."}
        or os.path.isabs(filename)
        or os.path.splitdrive(filename)[0]
        or re.match(r"^[A-Za-z]:", filename)
        or "/" in filename
        or "\\" in filename
        or ":" in filename
        or filename.endswith((" ", "."))
        or any(ord(character) < 32 for character in filename)
        or reserved_stem in WINDOWS_RESERVED_NAMES
    ):
        raise ValueError("Output filename must be one safe path component")


def _resolve_output_root(output_dir):
    supplied = os.path.expanduser(os.fspath(output_dir))
    if not os.path.isabs(supplied):
        raise ValueError("Output directory must be an existing absolute directory")
    try:
        supplied_state = os.lstat(supplied)
    except OSError as exc:
        raise ValueError("Output directory must be an existing absolute directory") from exc
    if stat.S_ISLNK(supplied_state.st_mode) or (
        os.name == "nt"
        and bool(
            getattr(supplied_state, "st_file_attributes", 0)
            & stat.FILE_ATTRIBUTE_REPARSE_POINT
        )
    ):
        raise ValueError("Output directory must not be a symlink or reparse point")
    root = os.path.abspath(supplied)
    if not os.path.isabs(root) or not stat.S_ISDIR(supplied_state.st_mode):
        raise ValueError("Output directory must be an existing absolute directory")
    return root


if os.name == "nt":
    def _windows_final_path(handle):
        size = 32768
        buffer = ctypes.create_unicode_buffer(size)
        length = _GetFinalPathNameByHandleW(handle, buffer, size, 0)
        if length == 0:
            raise ctypes.WinError(ctypes.get_last_error())
        if length >= size:
            size = length + 1
            buffer = ctypes.create_unicode_buffer(size)
            length = _GetFinalPathNameByHandleW(handle, buffer, size, 0)
            if length == 0 or length >= size:
                raise ctypes.WinError(ctypes.get_last_error())
        value = buffer.value
        if value.startswith("\\\\?\\UNC\\"):
            return "\\\\" + value[8:]
        if value.startswith("\\\\?\\"):
            return value[4:]
        return value


    def _set_windows_delete_disposition(handle):
        info = _FILE_DISPOSITION_INFO(True)
        if not _SetFileInformationByHandle(
            handle,
            _FILE_DISPOSITION_INFO_CLASS,
            ctypes.byref(info),
            ctypes.sizeof(info),
        ):
            raise ctypes.WinError(ctypes.get_last_error())


    def _close_windows_handle(handle):
        if not _CloseHandle(handle):
            raise ctypes.WinError(ctypes.get_last_error())


    def _open_windows_output_root(root):
        handle = _CreateFileW(
            root,
            _FILE_READ_ATTRIBUTES | _DELETE,
            0,
            None,
            _OPEN_EXISTING,
            _FILE_FLAG_BACKUP_SEMANTICS | _FILE_FLAG_OPEN_REPARSE_POINT,
            None,
        )
        if handle == _INVALID_HANDLE_VALUE:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            information = _BY_HANDLE_FILE_INFORMATION()
            if not _GetFileInformationByHandle(handle, ctypes.byref(information)):
                raise ctypes.WinError(ctypes.get_last_error())
            if not (information.dwFileAttributes & _FILE_ATTRIBUTE_DIRECTORY):
                raise ValueError("Output root handle is not a directory")
            if information.dwFileAttributes & _FILE_ATTRIBUTE_REPARSE_POINT:
                raise ValueError("Output directory must not be a reparse point")
            final_root = _windows_final_path(handle)
            if os.path.normcase(os.path.normpath(final_root)) != os.path.normcase(os.path.normpath(root)):
                raise ValueError("Opened output directory handle does not match the approved path")
            return handle, final_root
        except BaseException:
            _close_windows_handle(handle)
            raise


    def _close_created_windows_file(handle, delete):
        cleanup_error = None
        if delete:
            try:
                _set_windows_delete_disposition(handle)
            except BaseException as exc:
                cleanup_error = exc
        if not _CloseHandle(handle) and cleanup_error is None:
            cleanup_error = ctypes.WinError(ctypes.get_last_error())
        if cleanup_error is not None:
            raise cleanup_error


    def _write_windows_text_exclusive(root, filename, content):
        root_handle, final_root = _open_windows_output_root(root)
        try:
            candidate = os.path.join(final_root, filename)
            handle = _CreateFileW(
                candidate,
                _GENERIC_WRITE | _DELETE,
                0,
                None,
                _CREATE_NEW,
                _FILE_ATTRIBUTE_NORMAL | _FILE_FLAG_OPEN_REPARSE_POINT,
                None,
            )
            if handle == _INVALID_HANDLE_VALUE:
                raise ctypes.WinError(ctypes.get_last_error())

            transferred = False
            try:
                final_path = _windows_final_path(handle)
                final_parent = os.path.normcase(os.path.normpath(os.path.dirname(final_path)))
                approved_root = os.path.normcase(os.path.normpath(final_root))
                if final_parent != approved_root:
                    _close_created_windows_file(handle, delete=True)
                    handle = None
                    raise ValueError("Opened output handle escapes the approved output directory")
                try:
                    file_fd = msvcrt.open_osfhandle(handle, os.O_WRONLY | os.O_BINARY)
                except BaseException:
                    _close_created_windows_file(handle, delete=True)
                    handle = None
                    raise
                transferred = True
            finally:
                if not transferred and handle is not None:
                    _close_created_windows_file(handle, delete=True)

            stream = os.fdopen(file_fd, "w", encoding="utf-8")
            try:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            except BaseException:
                cleanup_error = None
                try:
                    _set_windows_delete_disposition(msvcrt.get_osfhandle(stream.fileno()))
                except BaseException as exc:
                    cleanup_error = exc
                finally:
                    stream.close()
                if cleanup_error is not None:
                    raise cleanup_error
                raise
            stream.close()
        finally:
            _close_windows_handle(root_handle)


def write_text_exclusive(output_dir, filename, content):
    """Create and write one citation through a contained exclusive handle."""
    if os.name != "nt":
        raise OSError(
            "Secure citation export is unavailable on non-Windows platforms"
        )
    if not isinstance(content, str):
        raise TypeError("Citation content must be text")
    _validate_output_filename(filename)
    root = _resolve_output_root(output_dir)
    _write_windows_text_exclusive(root, filename, content)
    return os.path.join(root, filename)


# ── PubMed ──────────────────────────────────────────────────────

def esearch(query, max_results=5):
    params = {"db": "pubmed", "term": query, "retmax": max_results, "retmode": "xml"}
    url = f"{EUTILS_BASE}/esearch.fcgi?{urlencode(params)}"
    try:
        with urlopen(url, timeout=30) as resp:
            xml_data = resp.read().decode("utf-8")
        root = ET.fromstring(xml_data)
        id_list = root.find("IdList")
        if id_list is not None:
            return [e.text for e in id_list.findall("Id")]
        return []
    except Exception as e:
        print(f"  ESearch error: {e}")
        return []


def efetch_medline(pmid, retries=1):
    params = {"db": "pubmed", "id": pmid, "rettype": "medline", "retmode": "text"}
    url = f"{EUTILS_BASE}/efetch.fcgi?{urlencode(params)}"
    for attempt in range(retries):
        try:
            with urlopen(url, timeout=30) as resp:
                return resp.read().decode("utf-8")
        except Exception as e:
            if attempt == retries - 1:
                print(f"  EFetch error for PMID {pmid}: {e}")
                return None
            time.sleep(DELAY * (attempt + 1))


def download_pubmed(pmid, output_dir, fmt, retries=1):
    """Download citation by PMID. Returns (success, filename_or_error)."""
    pmid = pmid.strip()
    if not pmid:
        return False, "Empty PMID"

    try:
        filename, filepath = build_output_target(output_dir, "pubmed", pmid, fmt)
    except ValueError as exc:
        return False, str(exc)

    print(f"  Downloading PMID: {pmid}")
    time.sleep(DELAY)
    nbib_text = efetch_medline(pmid, retries=retries)

    if not nbib_text or not nbib_text.strip():
        return False, f"PMID {pmid} not found or empty response"

    content = convert_from_medline(nbib_text, fmt)
    try:
        write_text_exclusive(output_dir, filename, content)
    except (OSError, ValueError) as exc:
        return False, f"Output file error for PMID {pmid}: {exc}"

    # Extract title for display
    for line in nbib_text.split("\n"):
        if line.startswith("TI  -"):
            print(f"  Title: {line[5:].strip()[:100]}")
            break

    print(f"  Saved: {filename} (format: {fmt})")
    return True, filename


def search_pubmed(query, output_dir, fmt, retries=1):
    print(f"  Searching: {query[:80]}...")
    time.sleep(DELAY)
    pmids = esearch(query)
    if not pmids:
        return False, f"No results for query: {query[:60]}"
    pmid = pmids[0]
    print(f"  Found PMID: {pmid}")
    return download_pubmed(pmid, output_dir, fmt, retries=retries)


# ── CrossRef ────────────────────────────────────────────────────

def download_crossref(doi, output_dir, fmt, retries=1):
    """Download citation by DOI from CrossRef. Returns (success, filename_or_error)."""
    doi = doi.strip()
    if not doi:
        return False, "Empty DOI"

    try:
        filename, filepath = build_output_target(output_dir, "crossref", doi, fmt)
    except ValueError as exc:
        return False, str(exc)

    print(f"  Downloading DOI: {doi}")
    time.sleep(DELAY)
    url = f"{CROSSREF_BASE}/{quote(doi, safe='')}"
    for attempt in range(retries):
        try:
            with urlopen(url, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            break
        except Exception as e:
            if attempt == retries - 1:
                return False, f"CrossRef API error for DOI {doi}: {e}"
            time.sleep(DELAY * (attempt + 1))

    content = convert_from_crossref(data, fmt)
    try:
        write_text_exclusive(output_dir, filename, content)
    except (OSError, ValueError) as exc:
        return False, f"Output file error for DOI {doi}: {exc}"

    msg = data.get("message", data)
    title = msg.get("title", [])
    if title:
        print(f"  Title: {title[0][:100]}")

    print(f"  Saved: {filename} (format: {fmt})")
    return True, filename


# ── arXiv ───────────────────────────────────────────────────────

def download_arxiv(arxiv_id, output_dir, fmt, retries=1):
    """Download citation by arXiv ID. Returns (success, filename_or_error)."""
    arxiv_id = arxiv_id.strip()
    if not arxiv_id:
        return False, "Empty arXiv ID"

    try:
        filename, filepath = build_output_target(output_dir, "arxiv", arxiv_id, fmt)
    except ValueError as exc:
        return False, str(exc)

    print(f"  Downloading arXiv: {arxiv_id}")
    time.sleep(DELAY)
    params = {"id_list": arxiv_id, "max_results": 1}
    url = f"{ARXIV_BASE}?{urlencode(params)}"
    for attempt in range(retries):
        try:
            with urlopen(url, timeout=30) as resp:
                xml_data = resp.read().decode("utf-8")
            break
        except Exception as e:
            if attempt == retries - 1:
                return False, f"arXiv API error for ID {arxiv_id}: {e}"
            time.sleep(DELAY * (attempt + 1))

    root = ET.fromstring(xml_data)
    content = convert_from_arxiv(root, fmt)
    if not content:
        return False, f"arXiv ID {arxiv_id}: no entry found in response"

    try:
        write_text_exclusive(output_dir, filename, content)
    except (OSError, ValueError) as exc:
        return False, f"Output file error for arXiv ID {arxiv_id}: {exc}"

    print(f"  Saved: {filename} (format: {fmt})")
    return True, filename


# ── Input parsing ───────────────────────────────────────────────

def parse_input_line(line):
    """Parse a single input line into (type, value)."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None, None

    upper = line.upper()
    if upper.startswith("PMID:"):
        return "pmid", line[5:].strip()
    if upper.startswith("DOI:"):
        return "doi", line[4:].strip()
    if upper.startswith("ARXIV:"):
        return "arxiv", line[6:].strip()
    if upper.startswith("QUERY:"):
        return "query", line[6:].strip()
    if upper.startswith("AUTHOR:"):
        parts = line.split("TITLE:", 1)
        author = parts[0][7:].strip()
        title = parts[1].strip() if len(parts) > 1 else ""
        return "author_title", (author, title)

    # Default: free-text search query
    return "query", line


def process_entry(entry_type, value, output_dir, fmt, retries=1):
    if entry_type == "pmid":
        return download_pubmed(value, output_dir, fmt, retries=retries)
    elif entry_type == "doi":
        return download_crossref(value, output_dir, fmt, retries=retries)
    elif entry_type == "arxiv":
        return download_arxiv(value, output_dir, fmt, retries=retries)
    elif entry_type == "author_title":
        author, title = value
        query_parts = []
        if author:
            query_parts.append(f"{author}[Author]")
        if title:
            query_parts.append(f"{title}[Title]")
        query = " AND ".join(query_parts) if query_parts else ""
        if not query:
            return False, "Empty author and title"
        return search_pubmed(query, output_dir, fmt, retries=retries)
    elif entry_type == "query":
        return search_pubmed(value, output_dir, fmt, retries=retries)
    return False, f"Unknown entry type: {entry_type}"


def process_file(input_file, output_dir, fmt, retries=1):
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        return 0, 0, [f"File not found: {input_file}"]

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    success, failed, errors = 0, 0, []
    for i, line in enumerate(lines, 1):
        entry_type, value = parse_input_line(line)
        if entry_type is None:
            continue
        print(f"\n[Line {i}] Processing: {line.strip()[:60]}")
        ok, result = process_entry(entry_type, value, output_dir, fmt, retries=retries)
        if ok:
            success += 1
        else:
            failed += 1
            errors.append(f"Line {i}: {result}")
    return success, failed, errors


def interactive_mode(output_dir, fmt, retries=1):
    print(f"Interactive mode (format: {fmt}) - enter references (one per line, empty line to finish):")
    print("Formats: PMID:12345 | DOI:10.xxx | ARXIV:2301.xxx | AUTHOR:Name TITLE:keywords | QUERY:...")
    print("-" * 60)

    success, failed, errors = 0, 0, []
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            break
        entry_type, value = parse_input_line(line)
        if entry_type is None:
            continue
        ok, result = process_entry(entry_type, value, output_dir, fmt, retries=retries)
        if ok:
            success += 1
        else:
            failed += 1
            errors.append(result)
    return success, failed, errors


# ── Main ────────────────────────────────────────────────────────

def self_test():
    """Run self-check on format converter pipeline."""
    print("FORMAT CONVERTER SELF-TEST")
    print("-" * 40)

    # 1. Module import check
    try:
        from converters import convert_from_medline, convert_from_crossref, convert_from_arxiv
        print("  [OK] Module imports")
    except Exception as e:
        print(f"  [FAIL] Module imports: {e}")
        return

    # 2. PubMed endpoint (known PMID: 28344011)
    pmid = "28344011"
    print(f"  Testing PubMed (PMID {pmid})...")
    try:
        import time
        time.sleep(0.5)
        nbib_text = efetch_medline(pmid)
        if nbib_text and nbib_text.strip():
            ris_content = convert_from_medline(nbib_text, "ris")
            bib_content = convert_from_medline(nbib_text, "bib")
            enw_content = convert_from_medline(nbib_text, "enw")
            if ris_content.strip() and bib_content.strip() and enw_content.strip():
                print(f"  [OK] PubMed endpoint (RIS: {len(ris_content)}B, BibTeX: {len(bib_content)}B, ENW: {len(enw_content)}B)")
            else:
                print(f"  [FAIL] PubMed conversion produced empty output")
        else:
            print(f"  [FAIL] PubMed returned empty response for PMID {pmid}")
    except Exception as e:
        print(f"  [FAIL] PubMed endpoint: {e}")

    # 3. CrossRef endpoint (known DOI)
    doi = "10.1038/nature14539"
    print(f"  Testing CrossRef (DOI {doi})...")
    try:
        from urllib.request import urlopen
        import json
        time.sleep(0.5)
        url = f"https://api.crossref.org/works/{quote(doi, safe='')}"
        with urlopen(url, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        ris_content = convert_from_crossref(data, "ris")
        bib_content = convert_from_crossref(data, "bib")
        enw_content = convert_from_crossref(data, "enw")
        if ris_content.strip() and bib_content.strip() and enw_content.strip():
            print(f"  [OK] CrossRef endpoint (RIS: {len(ris_content)}B, BibTeX: {len(bib_content)}B, ENW: {len(enw_content)}B)")
        else:
            print(f"  [FAIL] CrossRef conversion produced empty output")
    except Exception as e:
        print(f"  [FAIL] CrossRef endpoint: {e}")

    print("-" * 40)
    print("Self-test complete.")


def main():
    parser = argparse.ArgumentParser(
        description="Windows-only citation downloader with format conversion (.nbib/.ris/.bib)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --pmid 28344011 --output ABSOLUTE_OUTPUT_DIR
  %(prog)s --pmid 28344011,10645439 --format ris --output ABSOLUTE_OUTPUT_DIR
  %(prog)s --doi 10.1038/nature14539 --format bib --output ABSOLUTE_OUTPUT_DIR
  %(prog)s --doi 10.1038/nature14539,10.1038/s41586-020-2649-2 --format ris --output ABSOLUTE_OUTPUT_DIR
  %(prog)s --arxiv 1706.03762 --format bib --output ABSOLUTE_OUTPUT_DIR
  %(prog)s --arxiv 1706.03762,2302.13971 --format ris --output ABSOLUTE_OUTPUT_DIR
  %(prog)s --query "TB-Profiler AND Bioinformatics[Journal]" --output ABSOLUTE_OUTPUT_DIR
  %(prog)s --input refs.txt --output ABSOLUTE_OUTPUT_DIR
  %(prog)s --input refs.txt --format ris --output ABSOLUTE_OUTPUT_DIR
  %(prog)s --interactive --output ABSOLUTE_OUTPUT_DIR

refs.txt format:
  PMID:28344011
  DOI:10.1038/nature14539
  ARXIV:1706.03762
  QUERY:TB-Profiler AND Bioinformatics[Journal]
  AUTHOR:Dheda TITLE:drug-resistant tuberculosis
  # Lines starting with # are comments
        """,
    )
    parser.add_argument("--pmid", help="PMID(s), comma-separated")
    parser.add_argument("--doi", help="DOI(s), comma-separated")
    parser.add_argument("--arxiv", help="arXiv ID(s), comma-separated")
    parser.add_argument("--author", help="Author name for PubMed search")
    parser.add_argument("--title", help="Title keywords for PubMed search")
    parser.add_argument("--query", help="PubMed search query")
    parser.add_argument("--input", help="Input file with references")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument(
        "--format", choices=["nbib", "ris", "bib", "enw"], default="nbib",
        help="Output format: nbib (default, MEDLINE), ris (EndNote/Zotero), bib (BibTeX/LaTeX), enw (EndNote tagged)",
    )
    parser.add_argument(
        "--output",
        help="Existing absolute output directory explicitly approved by the user; Windows-only and required for any export",
    )
    parser.add_argument("--version", action="version", version="format-converter 1.0.0")
    parser.add_argument("--test", action="store_true", help="Run self-test on format converter pipeline")
    parser.add_argument("--retry", type=int, default=1, help="Retry count for HTTP calls")
    parser.add_argument("--preflight", action="store_true", help="Run connectivity check on API endpoints")

    args = parser.parse_args()

    if os.name != "nt":
        parser.error(
            "citation-file export is supported only on Windows; "
            "non-Windows platforms fail closed because no native writer has been verified"
        )

    if args.test:
        self_test()
        return

    if args.preflight:
        import sys as _sys
        _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from preflight import check_endpoints
        results = check_endpoints()
        # Print report
        print("PRE-FLIGHT REPORT")
        all_ok = True
        for name, info in results.items():
            status = "OK" if info["ok"] else "FAIL"
            detail = f"({info['time']:.1f}s)" if info["ok"] else f"({info['error']})"
            print(f"  {name:25s}: {status} {detail}")
            if not info["ok"]:
                all_ok = False
        reachable = sum(1 for v in results.values() if v["ok"])
        total = len(results)
        print(f"  {reachable}/{total} endpoints reachable.")
        if not all_ok:
            print("  Affected: format-converter downloads for unreachable endpoints (MCP tools unaffected).")
            _sys.exit(1)
        return

    if not any([args.pmid, args.doi, args.arxiv, args.author, args.query, args.input, args.interactive]):
        parser.error("Specify at least one input method")

    if not args.output:
        parser.error("--output is required for citation export; provide an existing absolute user-approved directory")

    expanded_output = os.path.expanduser(args.output)
    if not os.path.isabs(expanded_output):
        parser.error("--output must be an absolute path")

    output_dir = os.path.realpath(expanded_output)
    if not os.path.isdir(output_dir):
        parser.error("--output must name an existing directory; the converter will not create it")

    fmt = args.format
    print(f"Output directory: {output_dir}")
    print(f"Format: {fmt}")
    print("=" * 60)

    total_success, total_failed, all_errors = 0, 0, []

    def handle_list(ids_str, handler, retries=1):
        nonlocal total_success, total_failed
        ids = [x.strip() for x in ids_str.split(",") if x.strip()]
        for item_id in ids:
            print(f"\nProcessing: {item_id}")
            ok, result = handler(item_id, output_dir, fmt, retries=retries)
            if ok:
                total_success += 1
            else:
                total_failed += 1
                all_errors.append(result)

    # --pmid
    if args.pmid:
        handle_list(args.pmid, download_pubmed, retries=args.retry)

    # --doi
    if args.doi:
        if fmt == "nbib":
            print("Warning: CrossRef does not provide .nbib (MEDLINE) format. Falling back to .ris")
            fmt = "ris"
        handle_list(args.doi, download_crossref, retries=args.retry)

    # --arxiv
    if args.arxiv:
        if fmt == "nbib":
            print("Warning: arXiv does not provide .nbib (MEDLINE) format. Falling back to .ris")
            fmt = "ris"
        handle_list(args.arxiv, download_arxiv, retries=args.retry)

    # --author / --title / --query
    if args.author or args.title or args.query:
        if args.query:
            query = args.query
        else:
            query_parts = []
            if args.author:
                query_parts.append(f"{args.author}[Author]")
            if args.title:
                query_parts.append(f"{args.title}[Title]")
            query = " AND ".join(query_parts)
        print(f"\nProcessing search: {query}")
        ok, result = search_pubmed(query, output_dir, fmt, retries=args.retry)
        if ok:
            total_success += 1
        else:
            total_failed += 1
            all_errors.append(result)

    # --input
    if args.input:
        print(f"\nProcessing file: {args.input}")
        s, f, e = process_file(args.input, output_dir, fmt, retries=args.retry)
        total_success += s
        total_failed += f
        all_errors.extend(e)

    # --interactive
    if args.interactive:
        s, f, e = interactive_mode(output_dir, fmt, retries=args.retry)
        total_success += s
        total_failed += f
        all_errors.extend(e)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print(f"  Success: {total_success}")
    print(f"  Failed:  {total_failed}")
    if all_errors:
        print("  Errors:")
        for err in all_errors:
            print(f"    - {err}")
    print(f"  Output:  {output_dir}")
    print("=" * 60)
    if total_failed or all_errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
