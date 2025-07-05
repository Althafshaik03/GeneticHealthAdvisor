import pandas as pd

def parse_fasta(file, compute_properties=False):
    parsed_dict = {}
    seq_id, seq_cont = None, []

    for line in file:
        line = line.strip()
        if line.startswith(">"):
            if seq_id:
                parsed_dict[seq_id] = "".join(seq_cont)
            seq_id = line[1:]
            seq_cont = []
        else:
            seq_cont.append(line)
    if seq_id:
        parsed_dict[seq_id] = "".join(seq_cont)

    df = pd.DataFrame(parsed_dict.items(), columns=["Name", "Sequence"])
    if compute_properties:
        df["Length"] = df["Sequence"].apply(len)
        df["GC(%)"], df["Melting Temp"], df["MW (g/mol)"] = zip(*df["Sequence"].apply(calc_properties))
    return df

def parse_fastq(file, compute_properties=False):
    parsed_dict = {}
    while True:
        header = file.readline().strip()
        if not header:
            break
        sequence = file.readline().strip()
        file.readline()  # '+'
        file.readline()  # quality
        parsed_dict[header[1:]] = sequence

    df = pd.DataFrame(parsed_dict.items(), columns=["Name", "Sequence"])
    if compute_properties:
        df["Length"] = df["Sequence"].apply(len)
        df["GC(%)"], df["Melting Temp"], df["MW (g/mol)"] = zip(*df["Sequence"].apply(calc_properties))
    return df

def calc_properties(sequence):
    num_a = sequence.upper().count("A")
    num_t = sequence.upper().count("T")
    num_c = sequence.upper().count("C")
    num_g = sequence.upper().count("G")
    num_n = sequence.upper().count("N")

    try:
        gc_percent = 100 * (num_g + num_c) / (num_a + num_t + num_c + num_g + num_n)
    except ZeroDivisionError:
        gc_percent = 0

    mw = ((num_a * 313.2) + (num_t * 304.2) + (num_g * 329.2) + (num_c * 289.2) + (num_n * 303.7) - 61.96)
    temp_melt = (
        (num_a + num_t) * 2 + (num_g + num_c) * 4
        if len(sequence) < 14 else
        64.9 + 41 * ((num_g + num_c - 16.4) / (num_a + num_t + num_c + num_g))
    )
    return round(gc_percent, 1), round(temp_melt, 1), round(mw, 2)
