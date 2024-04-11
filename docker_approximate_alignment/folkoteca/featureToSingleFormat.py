"""
BSD 2-Clause License

Copyright (c) 2023, Hilda Romero-Velo
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
"""

"""
  Created by Hilda Romero-Velo on December 2023.
"""

import argparse
import dictionaries
import pretty_midi
import fractions

RATIOS_NUMS = [
    fractions.Fraction(1, 2),
    fractions.Fraction(1, 1),
    fractions.Fraction(2, 1),
    fractions.Fraction(1, 4),
    fractions.Fraction(4, 1),
    fractions.Fraction(1, 8),
    fractions.Fraction(1, 16),
    fractions.Fraction(1, 32),
    fractions.Fraction(8, 1),
    fractions.Fraction(1, 64),
    fractions.Fraction(3, 2),
    fractions.Fraction(3, 1),
    fractions.Fraction(6, 1),
    fractions.Fraction(12, 1),
    fractions.Fraction(3, 4),
    fractions.Fraction(3, 8),
    fractions.Fraction(16, 1),
    fractions.Fraction(24, 1),
    fractions.Fraction(3, 16),
    fractions.Fraction(32, 1),
    fractions.Fraction(3, 32),
    fractions.Fraction(3, 64),
    fractions.Fraction(1, 6),
    fractions.Fraction(2, 3),
    fractions.Fraction(1, 24),
    fractions.Fraction(8, 3),
    fractions.Fraction(1, 96),
    fractions.Fraction(48, 1),
    fractions.Fraction(32, 3),
    fractions.Fraction(64, 1),
    fractions.Fraction(1, 3),
    fractions.Fraction(4, 3),
    fractions.Fraction(1, 12),
    fractions.Fraction(1, 48),
    fractions.Fraction(16, 3),
    fractions.Fraction(96, 1),
    fractions.Fraction(64, 3),
]


def extract_chromatic(filepath):
    chromatic_feature = ""
    with open(filepath, "r", encoding="utf8") as f:
        for line in f:
            try:
                step = int(line.strip().replace("+", ""))
                if step != 0:
                    chromatic_feature += str(step) + ";"
            except ValueError:
                continue
    return chromatic_feature


def extract_diatonic(filepath):
    diatonic_feature = ""
    with open(filepath, "r", encoding="utf8") as f:
        for line in f:
            try:
                step = int(line.strip().replace("+", ""))
                if step != 1:
                    diatonic_feature += str(step) + ";"
            except ValueError:
                continue
    return diatonic_feature


def extract_rhythm(midifilepath):
    data = pretty_midi.PrettyMIDI(midifilepath)
    durations = []
    ratios = []

    for instrument in data.instruments:
        numNotes = len(instrument.notes)
        for idx, note in enumerate(instrument.notes):
            durations.append(note.get_duration())
            if idx < numNotes - 1:
                ratios.append(
                    data.time_to_tick(instrument.notes[idx + 1].get_duration())
                    / data.time_to_tick(note.get_duration())
                )
    res = ""
    for r in ratios:
        closest_r = min(RATIOS_NUMS, key=lambda x: abs(x - r))
        res = res + str(closest_r) + ";"
    return res


def to_single_notation(data, dictionary):
    values = data.split(";")
    values.pop()
    result = ""
    for v in values:
        try:
            result += dictionary[v.replace("r", "")]
        except:
            result += " "
    return result


def process_chromatic(filepath):
    chromatic_features = extract_chromatic(filepath)
    chromatic_query = to_single_notation(chromatic_features, dictionaries.CHROMATIC_DIC)
    print(chromatic_query)


def process_diatonic(filepath):
    diatonic_features = extract_diatonic(filepath)
    diatonic_query = to_single_notation(diatonic_features, dictionaries.DIATONIC_DIC)
    print(diatonic_query)


def process_rhythm(midifilepath):
    rhythm_feature = extract_rhythm(midifilepath)
    rhythm_query = to_single_notation(rhythm_feature, dictionaries.RHYTHM_DICT)
    print(rhythm_query)


parser = argparse.ArgumentParser(
    description="Query processing. Humdrum Kern to single format notation.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-c",
    "--chromatic",
    action="store",
    help="Convert query chromatic features to single format. Kern analysis needed.",
)
parser.add_argument(
    "-d",
    "--diatonic",
    action="store",
    help="Convert query diatonic features to single format. Kern analysis needed.",
)
parser.add_argument(
    "-r",
    "--rhythm",
    action="store",
    help="Convert query rhythm to single format. MIDI file needed.",
)

args = parser.parse_args()

if args.chromatic != None:
    process_chromatic(args.chromatic)

if args.diatonic != None:
    process_diatonic(args.diatonic)

if args.rhythm != None:
    process_rhythm(args.rhythm)
