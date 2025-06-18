# OpenDutchFrameNetLexicon

This repository contain the Open Dutch Lexicon with FrameNet1.7 annotations. licensed un der the MIT open source license. The lexicon is created from different subprojects following different approaches and applied on different texts:

1. SoNaR Propbank corpus enriched with FN1.7 annotations [1]: [Github](https://github.com/cltl/FrameNet_annotations_on_SoNaR), [Documentation](https://github.com/cltl/FrameNet_annotations_on_SoNaR/blob/master/report/DutchFNannotations.pdf)
2. the RBN-Wordnet alignment [2]: [Github](https://github.com/cltl/Dutch_FrameNet_Lexicon)[Documentation](https://github.com/cltl/Dutch_FrameNet_Lexicon/blob/master/documentation/dfn_classes.pdf)
3. DataToText Corpus (Wikidata and reference texts) enriched with FN1.7 annnotations [3]

The input lexicons are json files located in the data folder. At macro level, the structure of each lexicon has to be as follows:

* LU-name: lemma:pos
* lemma: lexical entry form
* pos: part of speech in upper case, i.e. NOUN, VERB, ADJ, etc..
* frames: list of frames associated with the entry, where each frame has one or more annotations obtained from the different input directories.

The annotations can differ in structure depending on the input. They should have:

* project: name of the project that created the annotation
* annotator: name of the annotator or annotation process
* mentions: pointers to the identifiers and possibly offsets for the tokens in the text that were associated with the frame.

The "merge_lexicons.py" script combines the input lexicons. The main function lets you specify which lexicons to merge. Statistics on the merging of all 6 input lexicons is provided here:

* fe_lexicon.json 1179 input, 0 overlap, 1179 added
* lexicon-manual.json 958 input, 400 overlap, 558 added
* lexicon-system.json 689 input, 176 overlap, 513 added
* A2.json 1246 input, 0 overlap, 1246 added
* A1.json 1246 input, 1246 overlap, 0 added
* rbn_dfn_1_2.json 951 input, 51 overlap, 900 added

The merged lexicon [odfn_lexicons_v1.json](../data/odfn_lexicons_v1.json) has 4396 unique entries in total with 1828 frames associated, 959 of which are frame elements derived from "fe_lexicon.json".The avrage polysemy (frames per entry) is 2.4 and 2,596 entries have a single frame.  In total 20,707 annotations of these frames have been stored, of which 7,026 frames have a single annotation. The [stats.json](stats.json) file provides further statistics.

## Acknowledgement
This works was funded through "Understanding language by machines" project (NWO-2013-Vossen-Spinoza ) and the "Framing Situations in the Dutch Language" project (NWO-VC.GW17.083).

## Contact
* Piek Vossen (piek.vossen@vu.nl)
* Pia Sommerauer (pia.sommerauer@vu.nl)

## References:

[1] P. Vossen, A. Fokkens, I. Maks, and C. V. Son, “Open Dutch FrameNet,” in Proceedings of the International FrameNet Workshop, Miyazaki, Japan, 2018.

```@inproceedings{Vos:Fok:Mak:Son:18,
address = {Miyazaki, Japan},
author = {Piek Vossen and Antske Fokkens and Isa Maks and Chantal Van Son},
booktitle = {{Proceedings of the International FrameNet Workshop}},
title = {{Open Dutch FrameNet}},
url = {http://lrec-conf.org/workshops/lrec2018/W5/pdf/6_W5.pdf},
year = {2018},
bdsk-url-1 = {http://lrec-conf.org/workshops/lrec2018/W5/pdf/6_W5.pdf}}
```

[2] M. Postma, L. Remijnse, F. Ilievski, A. Fokkens, S. Titarsolej, and P. Vossen, “Combining conceptual and referential annotation to study variation in framing,” in Proceedings of the international framenet workshop 2020: towards a global, multilingual framenet, Marseille, France, 2020, p. 31–40.

```@inproceedings{postma-etal-2020-combining,
address = {Marseille, France},
author = {Postma, Marten and Remijnse, Levi and Ilievski, Filip and Fokkens, Antske and Titarsolej, Sam and Vossen, Piek},
booktitle = {Proceedings of the International FrameNet Workshop 2020: Towards a Global, Multilingual FrameNet},
date-modified = {2022-01-16 09:57:57 +0100},
isbn = {979-10-95546-58-0},
keywords = {dfn},
language = {English},
month = may,
pages = {31--40},
publisher = {European Language Resources Association},
title = {Combining Conceptual and Referential Annotation to Study Variation in Framing},
url = {https://www.aclweb.org/anthology/2020.framenet-1.5},
year = {2020},
bdsk-url-1 = {https://www.aclweb.org/anthology/2020.framenet-1.5}}
```

[3] L. Remijnse, P. Vossen, A. Fokkens, and S. Titarsolej, Introducing Frege to Fillmore: a FrameNet dataset that captures both sense and reference, 2022, LREC.

```@proceedings{dfn-lrec2022,
author = {Levi Remijnse and Piek Vossen and Antske Fokkens and Sam Titarsolej},
booktitle = {Proceedings of the 13th Language Resources and Evaluation Conference, Marseille, June, 2022},
title = {Introducing Frege to Fillmore: A FrameNet Dataset that Captures both Sense and Reference},
url = {http://www.lrec-conf.org/proceedings/lrec2022/pdf/2022.lrec-1.5.pdf},
year = {2022},
bdsk-url-1 = {http://www.lrec-conf.org/proceedings/lrec2022/pdf/2022.lrec-1.5.pdf}}```


