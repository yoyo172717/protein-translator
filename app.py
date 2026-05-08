from flask import Flask, render_template, request, jsonify
import re

# IMPORTANT: must be named "app" for deployment platforms like Vercel
app = Flask(__name__)


# RNA Codon Table
GENETIC_MAP = {

    "UUU": "F", "UUC": "F",
    "UUA": "L", "UUG": "L",

    "CUU": "L", "CUC": "L",
    "CUA": "L", "CUG": "L",

    "AUU": "I", "AUC": "I",
    "AUA": "I", "AUG": "M",

    "GUU": "V", "GUC": "V",
    "GUA": "V", "GUG": "V",

    "UCU": "S", "UCC": "S",
    "UCA": "S", "UCG": "S",

    "CCU": "P", "CCC": "P",
    "CCA": "P", "CCG": "P",

    "ACU": "T", "ACC": "T",
    "ACA": "T", "ACG": "T",

    "GCU": "A", "GCC": "A",
    "GCA": "A", "GCG": "A",

    "UAU": "Y", "UAC": "Y",
    "UAA": "STOP", "UAG": "STOP",

    "CAU": "H", "CAC": "H",
    "CAA": "Q", "CAG": "Q",

    "AAU": "N", "AAC": "N",
    "AAA": "K", "AAG": "K",

    "GAU": "D", "GAC": "D",
    "GAA": "E", "GAG": "E",

    "UGU": "C", "UGC": "C",
    "UGA": "STOP", "UGG": "W",

    "CGU": "R", "CGC": "R",
    "CGA": "R", "CGG": "R",

    "AGU": "S", "AGC": "S",
    "AGA": "R", "AGG": "R",

    "GGU": "G", "GGC": "G",
    "GGA": "G", "GGG": "G"
}


@app.route("/")
def landing():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def decode_sequence():

    payload = request.get_json()

    if not payload or "sequence" not in payload:
        return jsonify({"error": "No sequence provided"}), 400

    raw_sequence = payload["sequence"]

    # Clean input (keep only valid nucleotide characters)
    nucleotide_stream = re.sub(
        r"[^ATUGCatugc]",
        "",
        raw_sequence
    ).upper()

    # Convert DNA -> RNA
    rna_stream = nucleotide_stream.replace("T", "U")

    codon_frames = []
    amino_chain = []

    # Read in groups of 3
    for index in range(0, len(rna_stream), 3):

        codon = rna_stream[index:index + 3]

        if len(codon) != 3:
            continue

        codon_frames.append(codon)

        amino = GENETIC_MAP.get(codon, "?")

        if amino == "STOP":
            amino_chain.append("*")
            break

        amino_chain.append(amino)

    return jsonify({

        "clean_sequence": rna_stream,
        "codons": codon_frames,
        "protein_chain": "".join(amino_chain),
        "base_count": len(rna_stream),
        "codon_count": len(codon_frames)
    })


# Local-only run (ignored by Vercel/Render)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
