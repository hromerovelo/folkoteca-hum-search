/***
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
**/

//
// Created by Hilda Romero-Velo on March 2024.
//
#include <iostream>
#include "utils_time.hpp"
#include <fstream>
#include <cstring>

using namespace std;

string launchCommand(string command)
{
    // Execute command.
    int exitCode = system(command.c_str());
    if (exitCode != 0)
    {
        cerr << "Error executing command: " << strerror(errno) << endl;
        return "ERROR";
    }

    return "";
}

bool fileExists(const string &filename)
{
    ifstream file(filename);
    return file.good();
}

int main(int argc, char **argv)
{
    if (argc < 3)
    {
        cout << "Usage: " << argv[0] << " [-c|-d|-r] query_file" << endl;
        cout << "    This program computes a BLAST alignment" << endl;
        cout << "    for a given query against the Folkoteca database." << endl;
        cout << "    Arg 1: [-c|-d|-r]     Type of search: -c, chromatic; -d, diatonic; -r, rhythm." << endl;
        cout << "    Arg 2: query_file     Query file. WAV for chromatic and diatonic search. MIDI for rhythm search." << endl;
        return 1;
    }

    // Parse command-line arguments.
    std::string search_feature = argv[1];
    std::string query_file = argv[2];

    // Check if the first argument is a valid search_feature.
    if (search_feature != "-c" && search_feature != "-d" && search_feature != "-r")
    {
        std::cerr << "Error: Invalid search feature. Types of search: -c, chromatic; -d, diatonic; -r, rhythm." << std::endl;
        return 1;
    }

    // Scores feature files.
    string chromatic_db = "features_blast_db/chromatic_db";
    string diatonic_db = "features_blast_db/diatonic_db";
    string rhythm_db = "features_blast_db/rhythm_db";
    string db = "";

    // Query in single format files.
    string chromatic_query_file = "queries/chromatic_sf_query.fasta";
    string diatonic_query_file = "queries/diatonic_sf_query.fasta";
    string rhythm_query_file = "queries/rhythm_sf_query.fasta";
    string query_sf_file = "";

    string flag = "";
    string query = "";

    // Perform corresponding action based on the search_feature.
    if (search_feature == "-c")
    {
        flag = "-c";
        db = chromatic_db;
        query_sf_file = chromatic_query_file;
    }
    else if (search_feature == "-d")
    {
        flag = "-d";
        db = diatonic_db;
        query_sf_file = diatonic_query_file;
    }
    else if (search_feature == "-r")
    {
        flag = "-r";
        db = rhythm_db;
        query_sf_file = rhythm_query_file;
    }

    string featurescommand = "bash extractQueryFeaturesToFasta.sh " + flag + " " + query_file;
    string cleancommand = "bash cleanFiles.sh";

    uint64_t searcht1 = util::time::user::now();
    query = launchCommand(featurescommand);
    uint64_t searcht2 = util::time::user::now();

    if (query == "ERROR")
    {
        system(cleancommand.c_str());
        return EXIT_FAILURE;
    }

    string resultsfile = "queries/results.txt";
    string timesfile = "queries/times.txt";

    string blastcommand = "blastp -query " + query_sf_file + " -db " + db + " -word_size 2 -matrix IDENTITY -max_target_seqs 1 -comp_based_stats 0 -evalue 1e5 -outfmt 4 -out " + resultsfile;

    uint64_t blastt1 = util::time::user::now();
    string score = launchCommand(blastcommand);
    uint64_t blastt2 = util::time::user::now();

    auto time = util::time::duration_cast<util::time::milliseconds>(searcht2 - searcht1);
    auto blasttime = util::time::duration_cast<util::time::milliseconds>(blastt2 - blastt1);

    if (score == "ERROR" || !fileExists(resultsfile))
    {
        system(cleancommand.c_str());
        return EXIT_FAILURE;
    }
    else
    {
        /* Print in shell */
        cout << endl;
        cout << "------- *** -------" << endl;
        cout << endl;
        cout << "Results at: " << resultsfile << endl;
        cout << "Process time: " << time << " milliseconds." << endl;
        cout << "Blast time: " << blasttime << " milliseconds." << endl;
        cout << endl;
        cout << "------- *** -------" << endl;
        cout << endl;

        system(cleancommand.c_str());
        return EXIT_SUCCESS;
    }
}