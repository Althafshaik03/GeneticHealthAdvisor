from utils.fasta_converter import parse_fasta, parse_fastq
from io import StringIO

def convert_fasta_to_csv(lines, compute_properties=True):
    file_like = StringIO("\n".join(lines))
    return parse_fasta(file_like, compute_properties)

def convert_fastq_to_csv(file_obj, compute_properties=True):
    content = StringIO(file_obj.read().decode("utf-8"))
    return parse_fastq(content, compute_properties)
