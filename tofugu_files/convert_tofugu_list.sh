#!/bin/bash

# First argument is input file
if [[ $# -ne 1 ]]; then
	echo """\
$0:
A tool to convert copy/paste source files from the Tofugu site's pitch
tables to more pretty graphics for humans.

Incorrect usage:
	$0 <input_filename.list>
	
Format example:
	LH 	名 	な
	LHH 	水 	みず
	LHHH 	会社 	かいしゃ
	LHHHH 	大学 	だいがく
	LHHHHH 	中国語 	ちゅうごくご
	<pitch>\\t<unique name>\\t<phonetics>
	
	Input is proccessed with bash's \`read\` so spacing is not critical."""
	
	exit
fi

SRC="$1"
MODIFY_SET=(ゃ ゅ ょ ぁ ぃ ぅ ぇ ぉ) # these characters don't count towards a mora length
MARU='○'

IND=0
PFX="1-"
while read INPUT; do
	IND=$(($IND+1))
	#echo "$INPUT"
	ARGS=($INPUT)
	CODE=${ARGS[0]}
	NAME=${ARGS[1]}
	KANA=${ARGS[2]}
	
	# Compute core word length
	KANA_TMP=$KANA
	for MiniMora in ${MODIFY_SET[@]}; do
		KANA_TMP=$(sed "s/$MiniMora//g" <<< $KANA_TMP)
	done
	MORA_LENGTH=${#KANA_TMP}
	# first find the length of the word, count the LH stuff
	if [[ ${CODE:0:1} == 'H' ]]; then # 頭高
		DOWN_STEP=1
	else
		CODE_TMP="${CODE:1}"
		CODE_TMP=${CODE_TMP%H*}
		DOWN_STEP=$((${#CODE_TMP}+2)) # downstep location
		if [[ $DOWN_STEP -gt $MORA_LENGTH ]]; then
			DOWN_STEP=0
		fi
	fi

	# Lad when tofugu assumes more mora in their code (or a particle)
	DELTA=$(($MORA_LENGTH-${#CODE}))
	if [[ $DELTA -eq -1 ]]; then
		KANA="$KANA$MARU"
	elif [[ $DELTA -ne 0 ]]; then
		echo "WARNING: Length error in line $IND: '$INPUT'" >&2
	fi
	
	#echo $DOWN_STEP/$MORA_LENGTH
	echo ${PFX}${IND}-$NAME:$KANA:$DOWN_STEP/$MORA_LENGTH
done < "$SRC"



