# Higher-level musical structures: Phrase, Section, Piece


class Phrase:
    """
    A musical phrase consisting of one or more melodies (one per voice/part).

    Attributes:
        melodies: List of Melody objects, one per voice (same order as voice configs).
        label: Optional descriptive label (e.g., "a1", "b2").
        bars: Number of bars in the phrase.
    """
    def __init__(self, melodies, label=None, bars=4):
        """
        Initialization function for Phrase class.

        Args:
            melodies: List of Melody objects (one per voice/part).
            label: Optional label for the phrase (e.g., "a1", "b2").
            bars: Number of bars in the phrase.
        """
        self.melodies = melodies  # list of Melody objects (one per voice)
        self.label = label
        self.bars = bars

    def __repr__(self):
        return f"Phrase({self.label}, bars={self.bars}, voices={len(self.melodies)})"


class Section:
    """
    A musical section consisting of a sequence of phrases.

    Attributes:
        phrases: List of Phrase objects that make up the section.
        label: Label for the section (e.g., "A", "B", "verse", "chorus").
    """
    def __init__(self, phrases, label=None):
        """
        Initialization function for Section class.

        Args:
            phrases: List of Phrase objects making up the section.
            label: Label for the section (e.g., "A", "B").
        """
        self.phrases = phrases
        self.label = label

    def __repr__(self):
        return f"Section({self.label}, phrases={len(self.phrases)})"


class Piece:
    """
    A complete musical piece with a defined form.

    Attributes:
        sections: Dictionary mapping section labels to Section objects.
        form: List of section labels defining the playback order (e.g., ["A", "A", "B", "A"]).
        key: Key object representing the global key of the piece.
        time_sig: Time signature string (e.g., "4/4", "3/4").
        tempo: Tempo in BPM.
        title: Title of the piece.
    """
    def __init__(self, sections, form, key, time_sig="4/4", tempo=120, title="Untitled"):
        """
        Initialization function for Piece class.

        Args:
            sections: Dictionary mapping section labels to Section objects.
            form: List of section labels (e.g., ["A", "A", "B", "A"]).
            key: Key object for the piece.
            time_sig: Time signature string (e.g., "4/4").
            tempo: Tempo in BPM.
            title: Title of the piece.
        """
        self.sections = sections
        self.form = form
        self.key = key
        self.time_sig = time_sig
        self.tempo = tempo
        self.title = title

    def get_ordered_sections(self):
        """
        Returns Section objects in the order defined by the form.

        Returns: A list of Section objects ordered according to the form.
        """
        return [self.sections[label] for label in self.form]

    def __repr__(self):
        return f"Piece('{self.title}', form={self.form}, key={self.key})"
