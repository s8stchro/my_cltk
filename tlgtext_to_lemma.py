
# python3.6 -m venv venv
# source venv/bin/activate
# pip install cltk
def imcalem_tlg_authors():
    # import the files
    TLG_file_to_convert = input("Give the adress of the TLG-file to be converted: ")
    new_file = input("Give the adress of the new file: ")
    # the name of the new file without extension
    import os
    bare_filename = os.path.splitext(new_file)[0]
    # transform the BETA code TLG-file into a utf file
    from cltk.corpus.utils.importer import CorpusImporter
    corpus_importer = CorpusImporter('greek')
    from cltk.corpus.greek.tlgu import TLGU
    t = TLGU()
    t.convert(TLG_file_to_convert, new_file)
    # apply encoding NFC to the utf text
    import unicodedata
    # write the NFC text to file
    with open(new_file, 'r') as f:
        normf = f.read()
    # replace underscores with space
    normf = normf.replace('_', ' ')
    with open(bare_filename+'_norm.txt', 'w+') as f:
        f.write(unicodedata.normalize('NFC', normf))
    # replace the apostrophs with a sign that will not be eliminated during the process of cleaning up the text
    with open(bare_filename+'_norm.txt', 'r') as f:
        noapf = f.read()
    noapf = noapf.replace('\'', '$')
    # write the text with the new apostroph sign to file
    with open(bare_filename+'_norm_apostr.txt', 'w+') as f:
        f.write(noapf)
    # clean-up the text
    from cltk.corpus.utils.formatter import tlg_plaintext_cleanup
    with open(bare_filename+'_norm_apostr.txt', 'r') as f:
        clf = f.read()
    clf = tlg_plaintext_cleanup(clf.lower(), rm_punctuation=True, rm_periods=True)
    # remove brackets, paragraph signs
    clf = clf.replace('(', '').replace(')', '').replace('§','')
    # restore apostrophe
    clf = clf.replace('$', '’')
    # replace grave with acute accent
    clf = clf.replace('ὰ', 'ά').replace('ὲ', 'έ').replace('ὴ', 'ή').replace('ὶ', 'ί').replace('ὸ', 'ό').replace('ὼ', 'ώ').replace('ὺ', 'ύ').replace('ἂ', 'ἄ').replace('ἒ', 'ἔ').replace('ἢ', 'ἤ').replace('ἲ', 'ἴ').replace('ὂ', 'ὄ').replace('ὢ', 'ὤ').replace('ὒ', 'ὔ').replace('ἃ', 'ἅ').replace('ἓ', 'ἕ').replace('ἣ', 'ἤ').replace('ἳ', 'ἵ').replace('ὃ', 'ὅ').replace('ὣ', 'ὥ').replace('ὓ', 'ὕ')

    with open(bare_filename+'_clean.txt', 'w+') as f:
        f.write(clf)
    # lemmatize the text
    from cltk.stem.lemma import LemmaReplacer
    lemmatizer = LemmaReplacer('greek')
    lemf = lemmatizer.lemmatize(clf)
    # write lemmatized text to file
    with open(bare_filename+'_lemmata.txt', 'w+') as f:
        for item in lemf:
            f.write('%s ' % item)
    # write unique lemmata to file
    with open(bare_filename+'_lemmata.txt', 'r') as f:
        lemf = f.read()
    uniqlemf = lemf.split()
    uniqlemf = set(uniqlemf)
    uniqlemf = list(uniqlemf)
    with open(bare_filename+'_lemmata_unique.txt', 'w+') as f:
        for item in uniqlemf:
            f.write('%s\n' % item)
