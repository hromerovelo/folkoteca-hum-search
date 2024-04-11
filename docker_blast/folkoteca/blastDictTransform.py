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

DIATONIC_DIC = {
    "a": "A",
    "b": "C",
    "c": "D",
    "d": "E",
    "e": "F",
    "f": "G",
    "g": "H",
    "h": "I",
    "i": "K",
    "j": "L",
    "k": "M",
    "l": "N",
    "m": "P",
    "n": "Q",
    "o": "R",
    "p": "S",
    "q": "T",
    "r": "V",
    "s": "W",
    "t": "Y",
    "\n": "\n",
}

CHROMATIC_DIC = {
    "s": "A",
    "k": "C",
    "a": "D",
    "r": "E",
    "C": "F",
    "x": "G",
    "F": "H",
    "w": "I",
    "f": "K",
    "v": "L",
    "B": "M",
    "q": "N",
    "p": "P",
    "j": "Q",
    "n": "R",
    "g": "S",
    "i": "T",
    "m": "V",
    "G": "W",
    "b": "Y",
}

RHYTHM_DIC = {
    "B": "A",
    "C": "C",
    "A": "D",
    "¤": "E",
    "D": "F",
    "E": "G",
    "J": "H",
    "N": "I",
    "G": "K",
    "[": "L",
    "]": "M",
    "╝": "N",
    "I": "P",
    "F": "Q",
    "O": "R",
    "n": "S",
    "K": "T",
    "ㅖ": "V",
    "{": "W",
    "Ù": "Y",
}


def featureToProteinBlast(text, dictionary):
    translated_text = ""
    for char in text:
        if char in dictionary:
            translated_text += dictionary[char]
        else:
            translated_text += "j"
    return translated_text


if __name__ == "__main__":
    diatonic_line = ""
    featureToProteinBlast(diatonic_line)
