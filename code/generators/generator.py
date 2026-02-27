# Main module for generating melodies and rhythms using Melody/Note objects
import random
from core.music import Key, Note, Melody, SCALES
from core.models import Phrase, Section, Piece

# Generate a random chromatic melody
def generate_random_notes(length=8, key: Key = Key("c", "major")) -> Melody:
    """
    Generate a random chromatic melody.

    Args:
        length (int): Number of notes in the melody.
        key: Key object representing the key to display the melody in.

    Returns: A Melody object containing the generated notes and the associated key.
        
    """
    # Random scale degrees from chromatic scale
    degrees = [random.choice(SCALES["chromatic"]) for _ in range(length)]
    
    # Create Note objects and convert to pitch
    notes = [Note(degree=int(d.replace("b","").replace("s","") if d[0] in "bs" else int(d)), 
                  pitch=key.degree_to_pitch(d)) for d in degrees]
    
    return Melody(notes = notes, key = key)

# Generate a melody by randomly moving in 2nds and 3rds within the scale
def generate_notes(num_notes=4, key: Key = Key("c", "major")) -> Melody:
    """
    Generate a melody by randomly moving in 2nds and 3rds within the scale.

    Args:
        num_notes (int): Number of notes to generate in the melody.
        key: Key object representing the key of the melody.

    Returns:
        
    """
    intervals = [-2, -1, 0, 1, 2]  # only 2nds and 3rds
    melody_notes = []
    current_idx = 0
    scale = key.get_scale_pitches()

    for _ in range(num_notes):
        val = random.choice(intervals)
        current_idx = (current_idx + val) % len(scale)
        note = Note(degree=current_idx+1, pitch=scale[current_idx])
        melody_notes.append(note)

    return Melody(notes = melody_notes, key = key)

# Helper function to convert rhythm symbols to beat values
def rhythm_to_values(rhythm):
    """
    Convert rhythm symbols to beat values.

    Args:
        rhythm (list): List of rhythm symbols (e.g., ["q", "e", "h"]).

    Returns:
        
    """
    rhythm_to_val = {
        "l": 16,
        "b": 8,
        "w": 4,
        "h": 2,
        "q": 1,
        "e": 0.5,
        "s": 0.25,
        "t": 0.125,
        "x": 0.0625
    }
    return [rhythm_to_val[dur] for dur in rhythm]

# Generate a rhythm pattern based on the time signature and allowed rhythm values
def generate_rhythm(bars=1, time_sig="4/4", values=["q"]):
    """
    Generate a rhythm pattern based on the time signature and allowed rhythm values.

    Args:
        bars (int): Number of bars to generate.
        time_sig (str): Time signature in the format "quantity/value" (e.g., "4/4", "3/4", "6/8").
        values (list): List of rhythm symbols (e.g., ["q", "e", "h"]) that can be used in the rhythm pattern.

    Returns: A list of rhythm values corresponding to the generated rhythm pattern.
        
    """
    quantity, unit = map(int, time_sig.split("/"))
    notes_per_bar = int(quantity * (4 / unit))
    rhythm = []
    values = rhythm_to_values(values)

    for _ in range(bars):
        tot = 0
        while tot < notes_per_bar:
            choices = [v for v in values if tot + v <= notes_per_bar]
            val = random.choice(choices)
            rhythm.append(val)
            tot += val

    return rhythm


# Generate a single phrase for all voices
def generate_phrase(label, key: Key, bars=4, voice_configs=None, time_sig="4/4") -> Phrase:
    """
    Generate a single musical phrase containing one melody per voice.

    Args:
        label: Label for the phrase (e.g., "a1", "b1").
        key: Key object representing the key for the phrase.
        bars: Number of bars in the phrase.
        voice_configs: List of voice configuration dicts, each with keys:
            "name" (str), "clef" (str), and "rhythm_values" (list of str).
        time_sig: Time signature string (e.g., "4/4").

    Returns: A Phrase object containing one Melody per voice.
    """
    if voice_configs is None:
        voice_configs = [{"name": "voiceOne", "clef": "treble", "rhythm_values": ["q"]}]

    melodies = []
    for voice_config in voice_configs:
        rhythm = generate_rhythm(bars=bars, time_sig=time_sig, values=voice_config["rhythm_values"])
        melody = generate_notes(num_notes=len(rhythm), key=key)
        melody.add_rhythm(rhythm)
        melodies.append(melody)

    return Phrase(melodies=melodies, label=label, bars=bars)


# Generate a section consisting of multiple phrases
def generate_section(label, key: Key, num_phrases=2, bars_per_phrase=4,
                     voice_configs=None, time_sig="4/4") -> Section:
    """
    Generate a musical section consisting of multiple phrases.

    Args:
        label: Label for the section (e.g., "A", "B").
        key: Key object representing the key for the section.
        num_phrases: Number of phrases in the section.
        bars_per_phrase: Number of bars per phrase.
        voice_configs: List of voice configuration dicts (see generate_phrase).
        time_sig: Time signature string (e.g., "4/4").

    Returns: A Section object containing the generated phrases.
    """
    phrases = []
    for i in range(num_phrases):
        phrase = generate_phrase(
            label=f"{label}{i + 1}",
            key=key,
            bars=bars_per_phrase,
            voice_configs=voice_configs,
            time_sig=time_sig
        )
        phrases.append(phrase)

    return Section(phrases=phrases, label=label)


# Generate a full musical piece using a defined form
def generate_piece(title, key: Key, form_def, form_order, voice_configs=None,
                   time_sig="4/4", tempo=120) -> Piece:
    """
    Generate a complete musical piece using a defined form with distinct sections.

    Each entry in form_def specifies how to generate one unique section (e.g., "A"
    or "B"). The form_order list controls the playback order, allowing repetition
    (e.g., ["A", "A", "B", "A"] for AABA form).

    Args:
        title: Title of the piece.
        key: Key object representing the global key of the piece.
        form_def: Dictionary mapping section labels to their generation parameters.
            Each value is a dict with optional keys:
                "num_phrases" (int, default 2): number of phrases in the section.
                "bars_per_phrase" (int, default 4): bars per phrase.
                "rhythm_values" (list of str): allowed rhythm symbols for this section.
                "voice_overrides" (list of dicts): per-voice config overrides for this section.
        form_order: List of section labels defining playback order (e.g., ["A", "A", "B", "A"]).
        voice_configs: Default voice configuration list used for all sections unless
            overridden via form_def "voice_overrides".
        time_sig: Time signature string (e.g., "4/4").
        tempo: Tempo in BPM.

    Returns: A Piece object with all sections generated and arranged in the given form.
    """
    if voice_configs is None:
        voice_configs = [{"name": "voiceOne", "clef": "treble", "rhythm_values": ["q"]}]

    sections = {}
    for label, params in form_def.items():
        num_phrases = params.get("num_phrases", 2)
        bars_per_phrase = params.get("bars_per_phrase", 4)
        rhythm_values = params.get("rhythm_values", None)
        voice_overrides = params.get("voice_overrides", None)

        # Build the voice configs for this section, applying any overrides
        section_voices = []
        for vc in voice_configs:
            merged = dict(vc)
            if rhythm_values:
                merged["rhythm_values"] = rhythm_values
            section_voices.append(merged)

        if voice_overrides:
            for i, override in enumerate(voice_overrides):
                if i < len(section_voices):
                    section_voices[i].update(override)

        section = generate_section(
            label=label,
            key=key,
            num_phrases=num_phrases,
            bars_per_phrase=bars_per_phrase,
            voice_configs=section_voices,
            time_sig=time_sig
        )
        sections[label] = section

    return Piece(
        sections=sections,
        form=form_order,
        key=key,
        time_sig=time_sig,
        tempo=tempo,
        title=title
    )
