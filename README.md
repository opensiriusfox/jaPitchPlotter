# jaPitchPlotter
A tool to produce SVGs of Japanese pitch accent patterns

## About
This tool is designed to produce simple SVG images of Japanese pitch accent
patterns. If you want to dig into the specifics about what they are, do like I
do and learn from [Dogen at Patreon](https://www.patreon.com/dogen).

The tool is designed to take in three strings describing a given word or phrase
and the corresponding pitch accent patterns. The tool generally makes few
assumptions about language, and relies upon you, the user to describe the
pattern. It generally assumes that a small "y" kana (やゆよ) in either katakana
or in hiragana is lumped with the prior kana, even if this doesn't make any
sense. If you write るょ then the tool will quite happily keep going. Other than
that it does assume that a small tsu (as in けっこう) is it's own mora.

The three strings are a key (or a name) for internal use. This can be a number
if you want. Secondly the phonetics of the word or phrase in either katakana or
hiragana, and finally a code representing the pitch accent of the phonetic
phrase. Examples are given in the 'example_codes.txt' file in this repository
separated by colons.

## Examples
Note by default the examples assume you do not change the default option of
dropping the final point indicating the difference between a heiban (平板) and
odaka (尾高) word. This is easily overridden by using the named variable
`includeFinalOpen=True` in the parseToneString call.

| Phonetics | Code | Result |
| :---: | :---: | :--- |
| べんきょう | `0/4` | 4 mora 平板 |
| べんきょうになる　| `0/4,1/2` | 4 mora 平板 connected to particle and 2 mora 頭高 |
| べんきょうになる　| `0/4,*1/2` | disconnected line between particle and second word |
| でんしゃは | `2/3` | 3 mora 中高 with marked particle |
| べんきょうして | `0/4*,*0/2` | disconnected line, no implied particle |

In short rules are:

+ <downstep location\>/<length of word\>
+ commas separating groups
+ trailing \* to drop an implied particle
+ leading \* to remove a connecting line
+ no whitespace tolerance (BUG!)

## Misc

Example images are available in the examples directory. Color, font, spacing,
padding, size, and plot styles are configurable. I personally use Inkscape to
convert SVG to other formats when needed. A handy bash command to do this for
is:
```bash
for SVG_FILE in examples/*.svg; do
    PNG_FILE="${SVG_FILE/.svg/.png}"
    inkscape --export-png="${PNG_FILE}" "${SVG_FILE}"
done
```

Send me your bugs (gently).

-Luke ([@siriusfox](https://twitter.com/siriusfox))


## Tofugu Examples
I did a small extension where I took the material from the [Tofugu Pronunciation Article](https://www.tofugu.com/japanese/japanese-pronunciation/) and wrote a simple parser to generate graphics showing the pattern rather than using their LH letter convention to show pitch. The examples are available in tofugu_examples and tofugu_files. [2018-05-23]
