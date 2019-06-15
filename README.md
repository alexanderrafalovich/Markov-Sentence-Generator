# Markov-Sentence-Generator
Generates new sentences from a traning text using a [Markov chain](https://en.wikipedia.org/wiki/Markov_chain)

#Usage

The project comes preloaded with some text form "On the German Ideology" by Karl Marx.

Just run `python generateMarkov.py --generate` to output new text to the console. Since this is meant to be shown in a gallery setting, there is a delay between each generated sentence.

To use your own text:

1. Put your text in `./bin/data/writing-1.txt`
2. Remove all paragraphs, double spaces, parenthesis, and other gramattical markings except `,` `;` `:` `.` `!` `?`
3. Run4 `python generateMarkov.py --build` to build the dictionary and matrix.
4. Run `python generateMarkov.py --generate` to generate your new sentences.

You may also wish to modify the delay, or pull it out into a cli variable. Im short on time so havent done it yet, if you do feel free to provide a pull request for that or any other cool features you create.
