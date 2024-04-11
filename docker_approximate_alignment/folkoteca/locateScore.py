"""
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
"""

"""
  Created by Hilda Romero-Velo on March 2024.
"""

import argparse
import scores_range

# Scores range files.
chromatic_scores_range_file = "scores_texts/chromatic_scores_range.pk1"
diatonic_scores_range_file = "scores_texts/diatonic_scores_range.pk1"
rhythm_scores_range_file = "scores_texts/rhythm_scores_range.pk1"


parser = argparse.ArgumentParser(
    description="Score location. Position in text needed.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-c",
    "--chromatic",
    action="store",
    help="Locate score by chromatic feature. Position in text needed.",
)
parser.add_argument(
    "-d",
    "--diatonic",
    action="store",
    help="Locate score by diatonic feature. Position in text needed.",
)
parser.add_argument(
    "-r",
    "--rhythm",
    action="store",
    help="Locate score by rhythm feature. Position in text needed.",
)

args = parser.parse_args()

if args.chromatic != None:
    scores_range_data = scores_range.ScoresRange.read_from_file(
        chromatic_scores_range_file
    )
    print(
        scores_range_data.get_value(scores_range_data.find_closest(int(args.chromatic)))
    )

if args.diatonic != None:
    scores_range_data = scores_range.ScoresRange.read_from_file(
        diatonic_scores_range_file
    )
    print(
        scores_range_data.get_value(scores_range_data.find_closest(int(args.diatonic)))
    )

if args.rhythm != None:
    scores_range_data = scores_range.ScoresRange.read_from_file(
        rhythm_scores_range_file
    )
    print(scores_range_data.get_value(scores_range_data.find_closest(int(args.rhythm))))
