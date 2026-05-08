const uploadPortal =
    document.getElementById(
        "sequenceUpload"
    );


uploadPortal.addEventListener(
    "change",
    function(event) {

        const uploadedFile =
            event.target.files[0];

        if (!uploadedFile) return;

        const genomeReader =
            new FileReader();

        genomeReader.onload =
            function(loadEvent) {

                document.getElementById(
                    "geneInput"
                ).value =
                    loadEvent.target.result;
            };

        genomeReader.readAsText(
            uploadedFile
        );
    }
);


async function translateGenome() {

    const nucleotidePayload =
        document.getElementById(
            "geneInput"
        ).value;


    if (!nucleotidePayload.trim()) {

        alert(
            "Please provide a nucleotide sequence."
        );

        return;
    }


    const relay = await fetch(
        "/translate",
        {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({

                sequence:
                    nucleotidePayload
            })
        }
    );


    const decodedGenome =
        await relay.json();


    document.getElementById(
        "proteinOutput"
    ).innerText =
        decodedGenome.protein_chain;


    document.getElementById(
        "rnaOutput"
    ).innerText =
        decodedGenome.clean_sequence;


    document.getElementById(
        "baseCount"
    ).innerText =
        decodedGenome.base_count;


    document.getElementById(
        "codonCount"
    ).innerText =
        decodedGenome.codon_count;
}