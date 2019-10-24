Competitive Grammar Writing in Python
=====================================

This repository is a derivation of [Competitive Grammar Writing in Python
](https://github.com/anoopsarkar/cgw.git)

This task involves writing or creating weighted context-free grammars
in order to parse English sentences and utterances. The vocabulary
is fixed. 

## Notation

A context-free grammar (CFG) is defined using the following building blocks:

* $N$, a set of non-terminal symbols (these symbols do not appear in the input)
* $S$, one non-terminal from $N$ called the start symbol. All derivations in a CFG start from $S$
* $V$, a vocabulary of words called terminal symbols. $N$ and $V$ are disjoint
* Rules of the form: $A \rightarrow \alpha$ where $A \in N$ and $\alpha \in (N \cup V)^\ast$.
* Weights or frequencies or probabilities can be associated with each rule in a CFG.
* A probabilistic CFG is defined as a group of conditional probabilities $P(\alpha \mid A)$: one for each non-terminal $A$

A context-free grammar that is in extended Chomsky Normal Form
(eCNF) iff the right hand side of each CFG rule is either one
non-terminal, or two non-terminals, or one terminal symbol.

This is a grammar in a formal sense. Just like we can write a
grammar for the syntax of Python, for instance. In this exercise
we will try to write a grammar for a fragment of English.

A derivation of this CFG starts with a string (called a sentential
form) containing the start symbol $S$ and then replaces the
non-terminals in that string recursively with the right hand side
of a rule (if there are multiple right hand sides for the same
non-terminal we pick one of them) until only terminal symbols are
left in the string. This sequence of terminal symbols is a valid
string in the (formal) language generated by the CFG.

## The Data

Initial versions of the context-free grammar files are provided to you:

* `S1.gr`: the default grammar file contains a context-free grammar in eCNF.
* `S2.gr`: the default backoff grammar file.
* `Vocab.gr`: the vocabulary file contains rules of the type `A -> a` where `A` is a non-terminal that represents the part of speech and `a` is a word (also called a terminal symbol).

Here is a fragment of `S1.gr`. Each line is a weighted context-free
grammar rule. First column is the weight, second column is the
left-hand side non-terminal of the CFG rule and the rest of the
line is the right-hand side of the CFG rule:

    1   S1   NP VP
    1   S1   NP _VP
    1   _VP  VP Punc
    20  NP   Det Nbar
    1   NP   Proper

The non-terminal `VP` is used to keep the grammar in eCNF. The
probability of a particular rule is obtained by normalizing the
weights for each left-hand side non-terminal in the grammar. For
example, for rule `NP -> Det Nbar` the conditional probability
`P(Det Nbar | NP)` is $\frac{20}{20+1}$.

The grammars in `S1.gr` and `S2.gr` are connected via the following rules in `S1.gr`:

    99 TOP  S1
    1  TOP  S2
    1  S2   Misc

## Other files

* `allowed_words.txt`: This file contains all the words that are allowed. You should make sure that your grammar generates sentences using exactly the words in this file. It does not specify the part of speech for each word, so you can choose to model the ambiguity of words in terms of part of speech in the `Vocab.gr` file.
* `example-sentences.txt`: This file contains example sentences that you can use as a starting point for your grammar development. Only the first two sentences of this file can be parsed using the default `S1.gr` grammar. The rest are parsed with the backoff `S2.gr` grammar. 
* `unseen.tags`: Used to deal with unknown words. You should not have to use this file during parsing, but the parser provided to you can optionally use this file in order to deal with unknown words in the input. 

## The Parser and Generator

You are given a parser that takes sentences as input and produces
parse trees and also a generator which generates a random sample
of sentences from the weighted grammar. Parsing and generating will
be useful steps in your grammar development strategy. You can learn
the various options for running the parser and generator using the
following command.

The parser has several options to speed up parsing, such as beam
size and pruning. Most likely you will not need to use those options
(unless your grammars are huge).

    python2 pcfg_parse_gen.py -h

### Parsing input

The parser provided to you reads in the grammar files and a set of
input sentences. It prints out the single most probable parse tree
for each sentence (using the weights assigned to each rule in the
input context-free grammar). 

For example given the input sentence `Arthur is the king` the parser
will return the most probable derivation of the sentence which uses
the following rules (shown with their probabilities) from the grammar
files:

    99/100 TOP    -> S1
    1/2    S1     -> NP _VP
    1/21   NP     -> Proper
    1/9    Proper -> Arthur
    1      _VP    -> VP Punc
    1      VP     -> VerbT NP
    1/6    VerbT  -> is
    20/21  NP     -> Det Nbar
    1/9    Det    -> the
    10/11  Nbar   -> Noun
    1/21   Noun   -> king

There might be many other derivations for this input string but the
derivation (which is just a list of CFG rules that fit together to
derive the input string) shown above is the most probable one
returned by the Python program provided to you using an algorithm
called the CKY algorithm which returns the argmax derivation for
any input string.

The probability of the derivation is simply the product of the
probabilities of the rules used in that derivation. For this
derivation the probability is:

<p>$ \frac{99}{100} \times \frac{1}{2} \times \frac{1}{21} \times \frac{1}{9} \times 1 \times 1 \times \frac{1}{6} \times \frac{20}{21} \times \frac{1}{9} \times \frac{10}{11} \times \frac{1}{21} $</p> 

The derivation can be written down as a parse tree by simply linking
the non-terminals together. The following tree is simply another
(more graphical) way to represent the derivation shown above.

    (TOP (S1 (NP (Proper Arthur) ) 
             (_VP (VP (VerbT is) 
                      (NP (Det the) 
                          (Nbar (Noun king) ))) 
                  (Punc .))) )

The parser also reports the negative
cross-entropy score for the whole set of sentences. Assume the
parser gets a text of $n$ sentences to parse: $s_1, s_2, \ldots,
s_n$ and we write $|s_i|$ to denote the length of each sentence
$s_i$. The probability assigned to each sentence by the parser is
$P(s_1), P(s_2), \ldots, P(s_n)$. The negative cross entropy is the
average log probability score (bits per word) and is defined as
follows:

<p>$\textrm{score}(s_1, \ldots, s_n) = \frac{ \log P(s_1) + \log P(s_2) + \ldots + \log P(s_n) }{ |s_1| + |s_2| + \ldots + |s_n| }$</p> 

We keep the value as negative cross entropy so that higher scores
are better. 

    python2 pcfg_parse_gen.py -i -g "*.gr" < example_sentences.txt
    #loading grammar files: S1.gr, S2.gr, Vocab.gr
    #reading grammar file: S1.gr
    #reading grammar file: S2.gr
    #reading grammar file: Vocab.gr

    ... skipping the parse trees ...

    #-cross entropy (bits/word): -10.0502

### Generating output

In order to aid your grammar development you can also generate
sentences from the weighted grammar to test if your grammar is
producing grammatical sentences with high probability. The following
command samples 20 sentences from the `S1.gr,Vocab.gr` grammar
files. 

    python2 pcfg_parse_gen.py -o 20 -g S1.gr,Vocab.gr
    #loading grammar files: S1.gr, Vocab.gr
    #reading grammar file: S1.gr
    #reading grammar file: Vocab.gr
    every pound covers this swallow
    no quest covers a weight
    Uther Pendragon rides any quest
    the chalice carries no corner .
    any castle rides no weight
    Sir Lancelot carries the land .
    a castle is each land
    every quest has any fruit .
    no king carries the weight
    that corner has every coconut
    the castle is the sovereign
    the king has this sun
    that swallow has a king
    another story rides no story
    this defeater carries that sovereign
    each quest on no winter carries the sovereign .
    another king has no coconut through another husk .
    a king rides another winter
    that castle carries no castle
    every horse covers the husk .

## Instruction for TA and Graders

1. TA get all team submission under this directory, and run
``` sh generate_sentence.sh'```
this will generate sample.txt under all team submission.
2. TA copy all_sentences.cvs into google sheets (one for each grader) [e.g.](https://docs.google.com/spreadsheets/d/1Ynq4jlBpU8j06uMp04A-q7XsSh8yW_mtDpBND4qF500/edit?usp=sharing),
and let graders assign grammaticality from 0 to 2 (where 2 is grammatical)
    * ``` python get_all_input.py [n_grader]```
    * import {CGW-grader0.txt}s under current directory to different googlesheet.
    * ong sentences will overflow, so select all and set Format > Text wrapping > Clip
    * Grader select first column (team column) and hide column before start grading

3. TA get all the sentences universally judged to be grammatical by graders,
and use each grammar to parse grammatical sentences that is not produced by itself.
    * Export googlesheet back into {CGW-grader0.txt}s (seperator tab)
    * ``` python get_other_and_precision.py [n_grader]```
    * ``` sh parse_other.sh```
    * ``` python get_recall_and_negative_entropy.py [n_grader]```

4. TA manuelly input 4 metrics to googlesheet [e.g.](https://docs.google.com/spreadsheets/d/1xzLW4FH5X0vAWXHr4-0Oi4gEtHuVwyYysQ2m1kkLjQQ/edit?usp=sharing).
    * Precision  =sum(grammaticality)/ (2* num sentences)
    * Recall = num of parsed other sentences/ (num of other sentences)
    * F1 = 2*((Precision*Recall)/(Precision+Recall))
    * negative entropy = score generated by 3

## Acknowledgements

The idea for this task and the original data files are taken from the following paper: 

> Jason Eisner and Noah A. Smith. [Competitive Grammar Writing](http://aclweb.org/anthology/W/W08/W08-0212.pdf). In Proceedings of the ACL Workshop on Issues in Teaching Computational Linguistics, pages 97-105, Columbus, OH, June 2008.

