# OpenDutchFrameNetLexicon

This repository contains the [Open Dutch Lexicon with FrameNet1.7 annotations, version 0.1](https://github.com/cltl/OpenDutchFrameNetLexicon/blob/main/data/odfn_lexicon_v0.1.json), licensed under the MIT open source license. You are free to use this lexicon but please ackonwledge us and make reference to our papers (see below). The lexicon is created from different subprojects following different approaches and applied on different texts:

1. SoNaR Propbank corpus enriched with FN1.7 annotations [paper 1]: [Github](https://github.com/cltl/FrameNet_annotations_on_SoNaR), [Documentation](https://github.com/cltl/FrameNet_annotations_on_SoNaR/blob/master/report/DutchFNannotations.pdf)
2. the RBN-Wordnet alignment [paper 2]: [Github](https://github.com/cltl/Dutch_FrameNet_Lexicon)[Documentation](https://github.com/cltl/Dutch_FrameNet_Lexicon/blob/master/documentation/dfn_classes.pdf)
3. DataToText Corpus (Wikidata and reference texts) enriched with FN1.7 annnotations [paper 3]

The input lexicons are json files located in the data folder. At macro level, the structure of each lexicon has to be as follows:

* LU-name: lemma:pos
* lemma: lexical entry form
* pos: part of speech in upper case, i.e. NOUN, VERB, ADJ, etc..
* frames: list of frames associated with the entry, where each frame has one or more annotations obtained from the different input directories.

```
    "bekogelen:VERB": {
        "lemma": "bekogelen",
        "pos": "VERB",
        "frames": {
            "fn17-cause_harm": {
                "annotations": [
                    {
                        "project": "DutchFrameNet",
                        "status": "manual",
                        "annotator": "oeaiRXKhTEAKGvM_2dK5ODSckESTVTqe",
                        "timestamp": "2022-03-02T19:59:10UTC",
                        "reftype": "type",
                        "mention": [
                            {
                                "doc": "7b2c4500-4e14-483d-bd01-3f50c13ac2c9.naf",
                                "term": "t160",
                                "tokens": [
                                    {
                                        "token_id": "w160",
                                        "sent": "9",
                                        "offset": "956",
                                        "length": "10"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }
```

The annotations can differ in terms of additional attributed depending on the input lexicon from which they were drawn. Please refer to the documentation of each subproject for an explanation. At the entry level, additional attributes can have been imported from the RBN dicitonary as shown here:

```
        "incorporated_fe": null,
        "lu_type": "singleton",
        "lexemes": [
            {
                "POS": "N",
                "breakBefore": "false",
                "headword": "false",
                "name": "kennis",
                "order": "1"
            }
        ],
        "optional_lu_attrs": {
            "FN_EN_LU_ID": "161",
            "Method": "Iteration-2_ODWN",
            "RBN_LU_ID": "r_n-19311",
            "RBN_matching_relation": "equivalence"
        }
```

At the annotation level all annotations at least have:

* project: name of the project that created the annotation
* annotator: name of the annotator or annotation process
* mentions: pointers to the identifiers and possibly offsets for the tokens in the text that were associated with the frame.

Especially the mentions can have slightly different structures depending on the source of the data. An example of an annotation is shown here:

```
            "fn17-awareness": {
                "annotations": [
                    {
                        "project": "DutchFrameNet",
                        "status": "manual",
                        "annotator": "MDeQ-tjzSSVIj52tFw6-louRoCd7EmPc",
                        "timestamp": "2023-02-07T15:46:52UTC",
                        "reftype": "type",
                        "mention": [
                            {
                                "doc": "20bdaf3b-4bbc-4c29-a0f7-82850102b5c4.naf",
                                "term": "t233",
                                "tokens": [
                                    {
                                        "token_id": "w233",
                                        "sent": "12",
                                        "offset": "1449",
                                        "length": "6"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "status": "manual",
                        "timestamp": null,
                        "project": "RBN_DFN_mapping",
                        "definition": "die je weet omdat je ze geleerd hebt"
                    }
                ]
```

Typically the mentions have references to text corpora created in the DutchFrameNet project (Framing situations in the Dutch Language) and the SoNaR frame annotation project. Mentions contain the token identifiers to find the occurrences in the source text.

For the DutchFrameNet, the NAF files with the original text can be found here: [DFN DATA RELEASE TO B ADDED](). For the SoNaR annotations, we refer to the SoNaR corpus that can be obtained [here](https://opensonar.ivdnt.org).


## Scripts

There are a few scripts given in this repository:

1. For obtaining the entries and annotations from the "Framing situations in the Dutch language" project (the DFN corpus). 
   * extract_frame_element_lexicon_from_naf_corpus.py
   * extract_frame_lexicon_from_naf_corpus
2. For merging input lexicons into a single JSON file:
   * merge_lexicons.py
3. For obtaining statistics on the merged lexicon:
   * get_statistics.py

The scripts for extracting the DFN corpus lexicon under 1) require access to the annotated texts in the NAF format. This corpus was compiled using the Multilingual Wiki Event Pipeline (MWEP). The source code, instructions, and documentation can be found here:

* MWEP: [Github](https://github.com/cltl/multilingual-wiki-event-pipeline)

The extracted corpus contains structured data for event instances and texts that are grounded to these events, so-called **reference texts**. Reference texts can be annotated using the MWEP Annotation Tool. The tool source code and instructions can be found here:

* MWEP annotation tool: [Github](https://github.com/cltl/FrameNet-annotation-tool)

You can create your own corpus using this code and annotate the texts with FrameNet frames. Using the scripts you can extract a lexicon from these annotations.

The "merge_lexicons.py" script combines several input lexicons. The input lexicons for the current release can be found in this Github in de **data** folder. The main function lets you specify which lexicons to merge. Statistics on the merging of all 6 input lexicons is provided here:

* fe_lexicon.json 1179 input, 0 overlap, 1179 added
* lexicon-manual.json 958 input, 400 overlap, 558 added
* lexicon-system.json 689 input, 176 overlap, 513 added
* A2.json 1246 input, 0 overlap, 1246 added
* A1.json 1246 input, 1246 overlap, 0 added
* rbn_dfn_1_2.json 951 input, 51 overlap, 900 added

The merged lexicon [odfn_lexicons_v1.json](../data/odfn_lexicons_v1.json) has 4,396 unique entries with 10,222 frame associations, 7115 of these are frames and 3107 are frame elements. The average polysemy (frames per entry) is 2.4 and 2,596 entries have a single frame. The frame associations cover 959 unique frames and 869 unique frame elements (derived from "fe_lexicon.json"). A frame or frame element that is associated with a lexical entry can have one or more annotations. These annotations can be alignments with wthe open Dutch ordnet or the Reference Bestand Nederlands (RBN) or word tokens in corpora that were annotated. In total 20,707 annotations of these frames have been stored, of which 7,026 frames have a single annotation. The [stats.json](stats.json) file provides further statistics.

## Acknowledgement
This works was funded through "Understanding language by machines" project (NWO-2013-Vossen-Spinoza ) and the "Framing Situations in the Dutch Language" project (NWO-VC.GW17.083).

## Contact
* Piek Vossen (piek.vossen@vu.nl)
* Pia Sommerauer (pia.sommerauer@vu.nl)

## References:

When using our code and or our data please make reference to our papers:

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


