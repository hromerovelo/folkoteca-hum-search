: '
BSD 2-Clause License

Copyright (c) 2024, Hilda Romero-Velo
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 '

: '
 # Created by Hilda Romero-Velo on March 2024.
 '

#!/bin/bash
usage="Program to extract chromatic (-c) and diatonic (-d) features from a given WAV file or rhythm (-r) feature from a MIDI file. Please, provide the path to the WAV/MIDI file being analysed."

# Default variables.
feature=""
input_file=""

# Process command line arguments.
while [[ $# -gt 0 ]]; do
    case "$1" in
    -c | --chromatic)
        feature="chromatic"
        shift
        ;;
    -d | --diatonic)
        feature="diatonic"
        shift
        ;;
    -r | --rhythm)
        feature="rhythm"
        shift
        ;;
    *)
        if [ -z "$input_file" ]; then
            input_file="$1"
        else
            echo "Error: Invalid argument: $1" >&2
            echo $usage
            exit 1
        fi
        shift
        ;;
    esac
done

# Check if at least one feature is specified.
if [ -z "$feature" ]; then
    echo "Error: You must specify one of the following options: -c (chromatic) or -d (diatonic) or -r (rhythm)" >&2
    echo $usage
    exit 1
fi

# Check if file name is specified.
if [ -z "$input_file" ]; then
    echo "Error: You must specify a file name after the feature option" >&2
    echo $usage
    exit 1
fi

# Check if file exists.
if [ ! -f "$input_file" ]; then
    echo "ERROR: '$input_file' file does not exist."
    exit 1
fi

# Extract file extension.
extension="${input_file##*.}"

# Extract the base name (filename without path).
basename=$(basename "$input_file")

# Remove the extension to get the name of the file.
filename="${basename%.*}"

# Check file extension
case "$feature" in
chromatic | diatonic)
    ## echo "Checking file extension..."
    # Check if file extension is ".wav".
    if [ "$extension" != "wav" ]; then
        echo "ERROR: File '$input_file' is not a WAV file."
        exit 1
    fi
    ;;
rhythm)
    ## echo "Checking file extension..."
    # Check if file extension is ".mid".
    if [ "$extension" != "mid" ]; then
        echo "ERROR: File '$input_file' is not a MIDI file."
        exit 1
    fi
    ;;
*)
    echo "Unknown feature: $feature" >&2
    exit 1
    ;;
esac

## echo "File extension checked."

# Create a temporary directory.
dir=$PWD

chmod +w $dir

mkdir -p tmpq
temp_dir="$dir/tmpq"

mkdir -p queries
queries_dir="$dir/queries"

# Check if temporary directory was created successfully.
if [ ! -d "$temp_dir" ]; then
    echo "ERROR: Failed to create temporary directory."
    exit 1
fi

# Check if queries directory was created successfully.
if [ ! -d "$queries_dir" ]; then
    echo "ERROR: Failed to create queries directory."
    exit 1
fi

## echo "Temporary directory created: $temp_dir"

if [ "$feature" = "rhythm" ]; then
    rhythm_sf_query="$queries_dir/rhythm_sf_query.fasta"
    echo ">${filename}" >$rhythn_sf_query
    python3 featureToSingleFormatBlast.py -r $input_file >>$rhythm_sf_query
    ## echo "Rhythm analysis computed. Rhythm single format query available at: $rhythm_sf_query"
else
    # Use basic-pitch to convert WAV to MIDI file.
    basic-pitch "${temp_dir}/" "$input_file"

    # Generated MIDI filename.
    midi_filename="${filename}_basic_pitch.mid"

    # Check if the MIDI file was generated successfully.
    if [ ! -f "$temp_dir/$midi_filename" ]; then
        echo "ERROR: Failed to generate $midi_filename MIDI file."
        exit 1
    fi
    midi_file="$temp_dir/$midi_filename"
    ## echo "MIDI file generated: $midi_file"

    # MIDI file to **kern format.
    mid2hum $midi_file >"$temp_dir/query_kern.krn"

    # Check if the **kern file was generated successfully.
    if [ ! -f "$temp_dir/query_kern.krn" ]; then
        echo "ERROR: Failed to generate *Kern file."
        exit 1
    fi
    kern_file="$temp_dir/query_kern.krn"
    ## echo **kern file generated: $kern_file"

    # Clean **kern file.
    kern_file_wor="$temp_dir/query_kern_wor.krn"
    humsed '/r/d' $kern_file >$kern_file_wor
    kern_file_cleaned="$temp_dir/query_kern_cleaned.krn"
    humsed '/-/d' $kern_file_wor >$kern_file_cleaned

    # Check if **kern file was cleaned successfully.
    if [ ! -f "$kern_file_cleaned" ]; then
        echo "ERROR: Failed to clean *Kern file."
        exit 1
    fi
    ## echo **kern file cleaned: $kern_file_cleaned"

    if [ "$feature" = "diatonic" ]; then
        # Diatonic analysis
        diatonic_analysis_file="$temp_dir/query_diatonic_analysis.txt"
        mint -d $kern_file_cleaned >$diatonic_analysis_file

        # Check if diatonic analysis file was generated successfully.
        if [ ! -f "$diatonic_analysis_file" ]; then
            echo "ERROR: Failed to generate diatonic analysis file."
            exit 1
        fi
        ## echo "Diatonic analysis file generated: $diatonic_analysis_file"

        diatonic_sf_query="$queries_dir/diatonic_sf_query.fasta"
        echo ">${filename}" >$diatonic_sf_query
        python3 featureToSingleFormatBlast.py -d $diatonic_analysis_file >>$diatonic_sf_query
        ## echo "Diatonic analysis computed. Diatonic single format query available at: $diatonic_sf_query"
    else
        # Chromatic analysis.
        semits_file="$temp_dir/query_semits.sem"
        chromatic_analysis_file="$temp_dir/query_chromatic_analysis.txt"
        semits -x $kern_file_cleaned >$semits_file

        # Check if semits file was generated successfully.
        if [ ! -f "$semits_file" ]; then
            echo "ERROR: Failed to generate semits file."
            exit 1
        fi
        ## echo "Semits file generated: $semits_file"

        xdelta -s ^= $semits_file >$chromatic_analysis_file

        # Check if chromatic analysis file was generated successfully.
        if [ ! -f "$chromatic_analysis_file" ]; then
            echo "ERROR: Failed to generate chromatic analysis file."
            exit 1
        fi
        ## echo "Chromatic analysis file generated: $chromatic_analysis_file"

        chromatic_sf_query="$queries_dir/chromatic_sf_query.fasta"
        echo ">${filename}" >$chromatic_sf_query
        python3 featureToSingleFormatBlast.py -c $chromatic_analysis_file >>$chromatic_sf_query
        ## echo "Chromatic analysis computed. Chromatic single format query available at: $chromatic_sf_query"

    fi
fi
