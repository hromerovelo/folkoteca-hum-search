# folkoteca-hum-search

We provide two docker images to conduct hummed queries in the [Folkoteca Galega](https://folkotecagalega.gal/pezas) dataset. These searches can be undertaken via three different musical characteristics: chromatic distance, diatonic distance or rhythm ratio. One approach performs an Approximate Alignment to compare the given query with the prepared corpus over a specified feature. Meanwhile, the other technique uses [BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi) to handle the alignment process.

In order to obtain the chromatic and diatonic distances from the input query, the [Basic Pitch](https://github.com/spotify/basic-pitch) library is used to convert the WAV audio file into a MIDI file. The [Humdrum Toolkit](https://www.humdrum.org/) is then used to extract those features. When performing a rhythmic search, a MIDI file must be provided, so Basic Pitch is no longer required.


## Download and set up

Clone `folkoteca-hum-search` repository:

```shell
git clone https://github.com/hromerovelo/folkoteca-hum-search.git
```

Generate the corresponding docker image for each alignment algorithm:

```shell
docker build -t folkoteca-hum-search:approximate docker_approximate_alignment/
docker build -t folkoteca-hum-search:blast docker_blast/
```

Run a container for each generated image:

```shell
docker run -d -p 2222:22 --name folkoteca-approximate-alignment-search folkoteca-hum-search:approximate
docker run -d -p 2223:22 --name folkoteca-blast-search folkoteca-hum-search:blast
```

Connect to the desired running container through SSH (with "user" and password "user"):

```shell
ssh user@localhost -p 2222
```

Access `folkoteca/` folder:

```shell
cd folkoteca/
```


## Approximate Alignment Search

You can run queries over the folkoteca corpus using the Approximate Alignment method:

```shell
./alignment-search -h
```

```plaintext
OUTPUT
------
Usage: ./alignment-search [-c|-d|-r] query_file
    This program computes an aprroximate alignment
    between a provided text file and a given query.
    Arg 1: [-c|-d|-r]     Type of search: -c, chromatic; -d, diatonic; -r, rhythm.
    Arg 2: query_file     Query file. WAV for chromatic and diatonic search. MIDI for rhythm search.
```

Example of usage:

```shell
./alignment-search -c audio_query.wav
```

*Results are displayed at command line.


## BLAST Search

You can run queries over the folkoteca corpus using the BLAST Alignment method:

```shell
./blast-search -h
```

```plaintext
OUTPUT
------
Usage: ./blast-search [-c|-d|-r] query_file
    This program computes a BLAST alignment for a given query against the Folkoteca database.
    Arg 1: [-c|-d|-r]     Type of search: -c, chromatic; -d, diatonic; -r, rhythm.
    Arg 2: query_file     Query file. WAV for chromatic and diatonic search. MIDI for rhythm search.
```

Example of usage:

```shell
./blast-search -d audio_query.wav
```

*Results are available at `queries/results.txt` directory.
